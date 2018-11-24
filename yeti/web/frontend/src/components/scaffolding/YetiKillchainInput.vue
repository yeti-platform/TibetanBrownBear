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
    <small>Current killchain: <code>{{this.killchainName}}</code></small>
  </div>
</template>

<script>
import axios from 'axios'
import VueTagsInput from '@johmun/vue-tags-input'

export default {
  props: ['value'],
  components: {
    VueTagsInput
  },
  data () {
    return {
      killchainName: 'lockheed-martin-cyber-kill-chain',
      listItems: [],
      item: '',
      autocompleteValues: []
    }
  },
  methods: {
    deletingPhase (event) {
      for (var i in this.killchainPhases) {
        if (this.killchainPhases[i].phase_name === event.tag.text) {
          this.killchainPhases.splice(i, 1)
          event.deleteTag()
        }
      }
    },
    addingPhase (event) {
      event.addTag()
      this.killchainPhases.push(Object({
        kill_chain_name: this.killchainName,
        phase_name: event.tag.text
      }))
      this.$emit('input', this.killchainPhases)
    },
    getKillchainPhases: function () {
      axios.get('settings/killchains/' + this.killchainName + '/').then(response => {
        if (response.status === 200) {
          this.autocompleteValues = response.data.map(item => Object({text: item.name}))
        }
      })
    }
  },
  computed: {
    filteredItems () {
      return (this.autocompleteValues || []).filter(item => new RegExp(this.item, 'i').test(item.text))
    }
  },
  mounted () {
    this.killchainPhases = (this.value || [])
    this.listItems = (this.value || []).map(item => Object({text: item['phase_name']}))
    this.getKillchainPhases()
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
