<template>
  <div>
    <vue-tags-input :tags="selectedTags"
                    v-model="item"
                    @before-adding-tag="addItem"
                    @before-deleting-tag="removeItem"
                    :autocomplete-min-length="2"
                    :add-on-key="[13, 188, 186]"
                    :separators="[',', ';']"
                    :autocomplete-items="filteredItems"
                    ref="tagsInput"
                    :placeholder="placeholder"/>
    <small v-if="autocompleteUrl" class="form-text text-muted">Autocompleting from <code>{{autocompleteUrl}}</code></small>
  </div>
</template>

<script>
import axios from 'axios'
import VueTagsInput from '@johmun/vue-tags-input'

export default {
  components: {
    VueTagsInput
  },
  props: ['value', 'autocompleteUrl', 'displayKey', 'placeholder'],
  data () {
    return {
      selectedItems: [],
      selectedTags: [],
      item: '',
      autocompleteItems: []
    }
  },
  methods: {
    clearItems () {
      this.selectedItems = []
      this.$refs.tagsInput.tagsCopy = []
    },
    addItem (event) {
      for (var item of this.autocompleteItems) {
        if (item.name === event.tag.text) {
          this.selectedItems.push(item)
        }
      }
      console.log(this.selectedItems)
      this.$emit('input', this.selectedItems)
      event.addTag()
    },
    removeItem (event) {
      for (var i in this.selectedItems) {
        if (this.selectedItems[i].name === event.tag.text) {
          this.selectedItems.splice(i, 1)
          event.deleteTag()
        }
      }
    },
    getAutocompleteItems: function () {
      axios.get(this.autocompleteUrl).then(response => {
        if (response.status === 200) {
          this.autocompleteItems = response.data
        }
      })
    }
  },
  computed: {
    filteredItems () {
      return this.autocompleteItems.filter(item => new RegExp(this.item, 'i').test(item.name)).map(item => Object({text: item.name}))
    }
  },
  mounted () {
    if (this.autocompleteUrl) {
      this.getAutocompleteItems()
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
