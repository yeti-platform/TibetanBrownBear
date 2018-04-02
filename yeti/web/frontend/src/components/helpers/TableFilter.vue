<template>
  <div class="">
    <input @keyup.enter='getObservables()' v-model="searchQuery" class="form-control form-control-light w-100" type="text" placeholder="Filter query" aria-label="Search">
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
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      elements: [],
      searchQuery: ''
    }
  },
  methods: {
    fetchObservables () {
      const apipath = `http://localhost:5000/api/observables/`
      console.log('filtering ' + apipath + ' with ' + this.searchQuery)
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
