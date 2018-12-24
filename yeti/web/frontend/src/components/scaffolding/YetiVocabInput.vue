<template>
  <div>
    <vue-tags-input :tags="listItems"
                    v-model="item"
                    @before-adding-tag="addingPhase"
                    @before-deleting-tag="deletingPhase"
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
      item: '',
      autocompleteItems: [],
      vocabList: []
    }
  },
  methods: {
    deletingPhase (event) {
      for (var i in this.vocabList) {
        if (this.vocabList[i] === event.tag.text) {
          this.vocabList.splice(i, 1)
          event.deleteTag()
          this.$emit('input', this.vocabList)
        }
      }
    },
    addingPhase (event) {
      event.addTag()
      this.vocabList.push(event.tag.text)
      this.$emit('input', this.vocabList)
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
    },
    listItems () {
      if (this.displayKey) {
        return (this.vocabList || []).map(item => Object({text: item[this.displayKey]}))
      } else {
        return (this.vocabList || []).map(item => Object({text: item}))
      }
    }
  },
  mounted () {
    if (this.autocompleteVocab) {
      this.getValuesForVocab()
    }
  },
  watch: {
    'value': function (val) {
      this.vocabList = val
      if (val === undefined) {
        this.vocabList = []
      }
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
