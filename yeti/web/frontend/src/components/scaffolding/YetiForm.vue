<template lang="html">
  <div>
    <form @submit="submitForm">
      <div v-for="field in fields" v-bind:key="field.name" class="form-group row">
        <label :for="field" class="col-sm-2 col-form-label">{{field.name}}</label>
        <div class="col-sm-10">
          <yeti-tagged-input v-if="field.type === 'tags' || field.type ==='list'"
                             v-model="object[field['name']]"
                             :autocompleteValues="field['autocompleteValues'] || []" />
          <input v-if="field.type === 'text'" class="form-control" :id="field['name']" v-model="object[field['name']]">
          <textarea v-if="field.type === 'code'" name="name" rows="8" cols="80" v-model="object[field['name']]"></textarea>
        </div>
      </div>
      <button type="submit" class="btn btn-primary" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save"}}</button>
      <pre>{{object}}</pre>
    </form>
    <div v-if="errors">
      <pre>{{errors}}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import YetiTaggedInput from '@/components/scaffolding/YetiTaggedInput'

const methods = {
  'PUT': axios.put,
  'POST': axios.post
}

export default {
  components: {
    YetiTaggedInput
  },
  props: {
    'fields': { default: () => [], type: Array },
    'apiPath': { type: String },
    'method': { default: 'POST', type: String },
    'object': { default: () => {}, type: Object },
    'onSaveCallback': Function
  },
  data () {
    return {
      saving: false,
      errors: '',
      tagForm: {}
    }
  },
  methods: {
    submitForm: function (e) {
      console.log('updating ' + this.apiPath + ' with ' + this.object)
      this.saving = true
      methods[this.method](this.apiPath, this.object)
        .then(response => {
          this.onSaveCallback(response)
        })
        .catch(error => {
          console.log(error.response.data)
          this.errors = error.response.data
        })
        .finally(() => {
          this.saving = false
        })
      e.preventDefault()
    }
  }
}
</script>

<style lang="css">
</style>
