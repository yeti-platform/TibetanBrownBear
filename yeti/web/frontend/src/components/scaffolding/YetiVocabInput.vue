<template>
  <div>
    <vue-tags-input :tags="listItems"
                    v-model="item"
                    @tags-changed="processItems"
                    :autocomplete-min-length="0"
                    :add-on-key="[13, 188, 186]"
                    :separators="[',', ';']"
                    :autocomplete-items="filteredItems" />
    <small v-if="autocompleteVocab" class="form-text text-muted">Autocompleting from <code>{{autocompleteVocab}}</code></small>
  </div>
</template>

<script>
import axios from 'axios'
import VueTagsInput from '@johmun/vue-tags-input'

export default {
  components: {
    VueTagsInput
  },
  props: ['value', 'autocompleteVocab', 'displayKey'],
  data () {
    return {
      listItems: [],
      item: '',
      autocompleteItems: []
    }
  },
  methods: {
    processItems: function (listItems) {
      this.$emit('input', listItems.map(item => item.text))
      this.listItems = listItems
    },
    formatListItems: function () {
      if (this.displayKey) {
        this.listItems = (this.value || []).map(item => Object({text: item[this.displayKey]}))
      } else {
        this.listItems = (this.value || []).map(item => Object({text: item}))
      }
    },
    getValuesForVocab: function () {
      axios.get('/settings/vocabs/' + this.autocompleteVocab + '/').then(response => {
        if (response.status === 200) {
          this.autocompleteItems = response.data.map(item => Object({text: item}))
        }
      })
    }
  },
  computed: {
    filteredItems () {
      return this.autocompleteItems.filter(validTag => new RegExp(this.item, 'i').test(validTag.text))
    }
  },
  mounted () {
    this.formatListItems()
    if (this.autocompleteVocab) {
      this.getValuesForVocab()
    }
  }
}
</script>

<style lang="css">
.vue-tags-input .input {
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.vue-tags-input .autocomplete .selected-item {
  background-color: #007bff;
}

.vue-tags-input .tag {
  background-color: #007bff !important;
  border-radius: .25rem !important;
  vertical-align: baseline;
  line-height: 1;
  text-align: center;
}

.vue-tags-input .deletion-mark {
  background-color: red !important;
}

</style>
