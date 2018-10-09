<template>
  <div class="new-link mb-2">
    <a href="#" class="btn btn-light" @click="toggleForm" v-if="!displayForm">Add relationships</a>
    <form @submit="addLink" class="form" v-if="displayForm">
      <div class="form-group mb-2">
        <yeti-autocomplete-input
          autocompleteUrl="entities"
          displayKey="name"
          v-model="entities"
          ref="relInput"
          placeholder="Search entities..."
        />
      </div>
      <button id="submit" type="submit" class="btn btn-primary" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save"}}</button>
      <a href="#" class="btn btn-secondary" @click="toggleForm">Cancel</a>
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
      saving: false,
      displayForm: false
    }
  },
  methods: {
    toggleForm (e) {
      this.displayForm = !this.displayForm
    },
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
          this.$emit('links-added', response.data)
          this.entities = []
          this.$refs.relInput.clearItems()
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
