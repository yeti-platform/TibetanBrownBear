<template lang="html">
  <form @submit="submitForm">
    <div v-for="field in fields" v-bind:key="field" class="form-group row">
      <label :for="field" class="col-sm-2 col-form-label">{{field}}</label>
      <div class="col-sm-10">
        <input class="form-control" :id="field" v-model="object[field]">
      </div>
    </div>
    <button type="submit" class="btn btn-primary" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save"}}</button>
    <pre>{{object}}</pre>
  </form>
</template>

<script>
import axios from 'axios'

const methods = {
  'PUT': axios.put,
  'POST': axios.post
}

export default {
  props: {
    'fields': { default: [], type: Array },
    'apiPath': { type: String },
    'method': { default: 'POST', type: String },
    'object': Object,
    'onSaveCallback': Function
  },
  data () {
    return {
      saving: false
    }
  },
  methods: {
    submitForm: function (e) {
      console.log('updating ' + this.apiPath + ' with ' + this.object)
      this.saving = true
      methods[this.method](this.apiPath, this.object)
        .then(response => {
          this.onSaveCallback(response)
          // this.$router.push({name: 'EntityDetails', params: {id: response.data.id}})
        })
        .catch(error => {
          console.log(error)
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
