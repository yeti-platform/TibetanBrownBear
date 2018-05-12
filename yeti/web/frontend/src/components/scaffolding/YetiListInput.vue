<template>
  <vue-tags-input :tags="listItems"
                  v-model="item"
                  @tags-changed="processItems"
                  :autocomplete-items="filteredItems"/>
</template>

<script>
import VueTagsInput from '@johmun/vue-tags-input'

export default {
  components: {
    VueTagsInput
  },
  props: ['value', 'autocompleteValues', 'displayKey'],
  data () {
    return {
      listItems: [],
      item: '',
      formattedAutoCompleteValues: []
    }
  },
  methods: {
    processItems: function (listItems) {
      this.$emit('input', listItems.map(item => item.text))
      this.listItems = listItems
    },
    formatAutocompleteValues: function () {
      this.formattedAutoCompleteValues = this.autocompleteValues.map(value => Object({text: value}))
    },
    formatListItems: function () {
      if (this.displayKey) {
        this.listItems = this.value.map(item => Object({text: item[this.displayKey]}))
      } else {
        this.listItems = this.value.map(item => Object({text: item}))
      }
    }
  },
  computed: {
    filteredItems () {
      return this.formattedAutoCompleteValues.filter(validTag => new RegExp(this.item, 'i').test(validTag.text))
    }
  },
  mounted () {
    this.formatListItems()
    if (this.autocompleteValues) {
      this.formatAutocompleteValues()
    }
  }
}
</script>

<style lang="css">
</style>
