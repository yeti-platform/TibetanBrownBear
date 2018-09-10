<template lang="html">
  <div>
    <form @submit="submitForm">
      <div v-for="field in fields" v-bind:key="field.name" class="form-group row">
        <label :for="field.name" class="col-sm-2 col-form-label">{{field.name}}</label>
        <div class="col-sm-10">
          <!-- plain text input -->
          <input v-if="field.type === 'text'" class="form-control" :id="field['name']" v-model="object[field['name']]">
          <!-- code input -->
          <textarea v-if="field.type === 'code'" :id="field['name']" rows="8" cols="80" v-model="object[field['name']]"></textarea>
          <!-- textarea -->
          <textarea v-if="field.type === 'longtext'" :id="field['name']" rows="8" cols="80" v-model="object[field['name']]"></textarea>
          <!-- datetime -->
          <datepicker v-if="field.type === 'datetime'" :id="field['name']" v-model="object[field['name']]"
                      :format="customFormatter"
                      :bootstrap-styling="true"
                      :typeable="true"
                      placeholder="Click to pick date">
          </datepicker>
          <!-- list-type input -->
          <yeti-list-input v-if="field.type === 'list'"
                           v-model="object[field['name']]"
                           :autocompleteVocab="field['vocab'] || []" />
          <!-- tag input -->
          <yeti-list-input v-if="field.type === 'tags'"
                           v-model="object[field['name']]"
                           displayKey="name"
                           :autocompleteVocab="field['vocab'] || []" />
        </div>
      </div>
      <button id="submit" type="submit" class="btn btn-primary" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save"}}</button>
      <pre>{{object}}</pre>
    </form>
    <div v-if="errors">
      <pre>{{errors}}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Datepicker from 'vuejs-datepicker'

import YetiListInput from '@/components/scaffolding/YetiListInput'

var moment = require('moment')

const methods = {
  'PUT': axios.put,
  'POST': axios.post
}

export default {
  components: {
    YetiListInput,
    Datepicker
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
    }
  }
}
</script>

<style lang="css">
</style>
