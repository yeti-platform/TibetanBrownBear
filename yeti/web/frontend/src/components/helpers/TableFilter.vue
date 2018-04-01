<template>
  <div class="table-responsive">
    <table class="table table-hover table-sm">
      <thead>
        <tr><th>Value</th><th>IDNA</th></tr>
      </thead>
        <tr v-for="elt in elements" v-bind:key="elt.id">
          <td>{{elt.value}}</td><td>{{elt.idna}}</td>
        </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['searchQuery'],
  watch: {
    searchQuery: function () {
      // TODO implement timer
      this.getObservables()
    }
  },
  data () {
    return {
      elements: []
    }
  },
  methods: {
    fetchObservables () {
      const apipath = `http://localhost:5000/api/observables/`
      console.log('fetching data from ' + apipath)
      axios.get(apipath)
        .then(response => {
          this.elements = response.data
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
