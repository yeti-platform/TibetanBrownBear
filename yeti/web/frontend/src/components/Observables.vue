<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Observables</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <button class="btn btn-sm btn-outline-secondary">Share</button>
          <button class="btn btn-sm btn-outline-secondary">Export</button>
        </div>
        <button class="btn btn-sm btn-outline-secondary dropdown-toggle">
          <span data-feather="calendar"></span>
          This week
        </button>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-hover table-sm">
        <thead>
          <tr><th>Value</th><th>IDNA</th></tr>
        </thead>
          <tr v-for="obs in observables" v-bind:key="obs.id">
            <td>{{obs.value}}</td><td>{{obs.idna}}</td>
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
