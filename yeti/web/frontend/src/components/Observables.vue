<template>
<div>
  <h1>List of observables</h1>
  <table>
    <tr><th>Value</th><th>IDNA</th></tr>
    <tr v-for="obs in observables" v-bind:key="obs.id">
      <td>{{obs.value}}</td><td>{{obs.idna}}</td>
    </tr>
  </table>
  <button @click="getObservables">Get observables</button>
</div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      observables: []
    }
  },
  methods: {
    fetchObservables () {
      const apipath = `http://localhost:5000/api/observables/`
      axios.get(apipath)
        .then(response => {
          this.observables = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    getObservables () {
      this.fetchObservables()
    }
  },
  created () {
    this.getObservables()
  }
}
</script>
