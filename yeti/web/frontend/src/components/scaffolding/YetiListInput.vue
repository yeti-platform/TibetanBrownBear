<template>
  <vue-tags-input :tags="tags"
                  v-model="tag"
                  @tags-changed="processTags"
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
      tags: [],
      tag: '',
      formattedAutoCompleteValues: []
    }
  },
  methods: {
    processTags: function (tags) {
      this.$emit('input', tags.map(tag => tag.text))
      this.tags = tags
    }
  },
  computed: {
    filteredItems () {
      return this.formattedAutoCompleteValues
        .filter(validTag => new RegExp(this.tag, 'i').test(validTag.text))
    }
  },
  mounted () {
    if (this.displayKey) {
      this.tags = this.value.map(tag => Object({text: tag[this.displayKey]}))
    } else {
      this.tags = this.value.map(tag => Object({text: tag}))
    }
    this.formattedAutoCompleteValues = this.autocompleteValues.map(value => Object({text: value}))
  }
}
</script>

<style lang="css">
</style>
