<template lang="html">
  <form @submit="checkForm">
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
    'apipath',
    'type'
  ],
  data () {
    return {
      object: {'type': this.type}
    }
  },
  methods: {
    checkForm: function (e) {
      console.log('updating ' + this.apipath + ' with ' + this.object)
      axios.post(this.apipath, this.object)
        .then(response => {
          console.log('all good!')
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
