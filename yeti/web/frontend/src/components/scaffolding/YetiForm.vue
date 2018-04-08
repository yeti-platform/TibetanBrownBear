<template lang="html">
  <form @submit="submitForm">
    <div v-for="field in fields" v-bind:key="field" class="form-group row">
      <label :for="field" class="col-sm-2 col-form-label">{{field}}</label>
      <div class="col-sm-10">
        <input class="form-control" :id="field" v-model="object[field]">
      </div>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    <pre>{{object}}</pre>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  props: [
    'fields',
    'apiPath',
    'type'
  ],
  data () {
    return {
      object: {'type': this.type}
    }
  },
  methods: {
    submitForm: function (e) {
      console.log('updating ' + this.apiPath + ' with ' + this.object)
      axios.post(this.apiPath, this.object)
        .then(response => {
          this.$router.push({name: 'EntityDetails', params: {id: response.data.id}})
        })
        .catch(error => {
          console.log(error)
        })
      e.preventDefault()
    }
  }
}
</script>

<style lang="css">
</style>
