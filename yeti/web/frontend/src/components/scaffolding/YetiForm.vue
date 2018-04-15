<template lang="html">
  <div>
    <form @submit="submitForm">
      <div v-for="field in fields" v-bind:key="field" class="form-group row">
        <label :for="field" class="col-sm-2 col-form-label">{{field}}</label>
        <div class="col-sm-10">
          <yeti-tagged-input v-if="field in taggedInputs" v-model="object[field]" :autocompleteValues="taggedInputs[field]"/>
          <input v-else class="form-control" :id="field" v-model="object[field]">
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

const taggedInputs = {
  family: ['trojan', 'etc'],
  tags: []
}

export default {
  components: {
    YetiTaggedInput
  },
  props: {
    'fields': { default: [], type: Array },
    'apiPath': { type: String },
    'method': { default: 'POST', type: String },
    'object': Object,
    'onSaveCallback': Function
  },
  data () {
    return {
      saving: false,
      errors: '',
      tagForm: {},
      taggedInputs: taggedInputs
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
