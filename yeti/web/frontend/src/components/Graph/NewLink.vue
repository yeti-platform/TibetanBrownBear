<template>
  <div class="new-link">
    New relationship
    <form @submit="addLink">
      <yeti-autocomplete-input
        autocompleteUrl="entities"
        displayKey="name"
        v-model="entities"
      />
      <button id="submit" type="submit" class="btn btn-primary" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save"}}</button>
    </form>
  </div>
</template>

<script>
import YetiAutocompleteInput from '@/components/scaffolding/YetiAutocompleteInput'
import axios from 'axios'
import { relationships } from './StixRelationships.js'

export default {
  components: {
    YetiAutocompleteInput
  },
  props: ['sourceEntity'],
  data () {
    return {
      entities: [],
      saving: false
    }
  },
  methods: {
    addLink: function (e) {
      e.preventDefault()
      this.saving = true

      var links = []
      for (var entity of this.entities) {
        let linkType = relationships[this.sourceEntity.type][entity.type]
        if (linkType === undefined) {
          console.log('Wrong datatype')
          this.saving = false
          return
        }
        links.push({
          target: entity,
          link_type: linkType[0],
          stix_rel: null
        })
      }

      axios.post('entities/' + this.sourceEntity.id + '/addlink/', links)
        .then(response => {
          console.log('OK!')
          this.entities = []
          this.$emit('links-added', response.data)
        })
        .catch(error => {
          this.errors = error.response.data
        })
        .finally(() => {
          this.saving = false
        })
    }
  }
}
</script>

<style>

</style>
