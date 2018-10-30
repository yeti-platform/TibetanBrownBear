<template>
  <div>
    <form @submit="submitForm">
      <yeti-form-field v-bind:key="field.name" v-for="field in fields" :field="field" v-model="object[field['name']]"></yeti-form-field>
      <button id="submit" type="submit" class="btn btn-primary" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save changes"}}</button>
      <button id="cancel" @click="back()" class="btn btn-secondary" v-bind:class="{ disabled: saving }">Cancel</button>
      <pre class="json p-3">{{object}}</pre>
    </form>
    <div v-if="errors">
      <pre class="json p-3">{{errors}}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import YetiFormField from '@/components/scaffolding/YetiFormField'

var moment = require('moment')

const methods = {
  'PUT': axios.put,
  'POST': axios.post
}

export default {
  components: {
    YetiFormField
  },
  props: {
    'fields': { default: () => [], type: Array },
    'apiPath': { type: String },
    'method': { default: 'POST', type: String },
    'object': { default: () => {}, type: Object }
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
      this.saving = true
      methods[this.method](this.apiPath, this.object)
        .then(response => {
          this.$emit('form-submit', response.data)
        })
        .catch(error => {
          this.errors = error.response.data
        })
        .finally(() => {
          this.saving = false
        })
      e.preventDefault()
    },
    customFormatter (date) {
      return moment(date).format('YYYY-MM-DD HH:mm:ss ZZ')
    },
    back () {
      history.back()
    }
  }
}
</script>

<style lang="css">
textarea.code {
  font-family: 'Courier New', Courier, monospace;
}
</style>
