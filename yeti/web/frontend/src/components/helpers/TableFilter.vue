<template>
  <div class="">
    <input @keyup.enter='getObservables()' v-model="searchQuery" class="form-control form-control-light w-100" type="text" placeholder="Filter query" aria-label="Search">
    <div class="table-responsive">
      <table class="table table-hover table-compact table-sm">
        <thead>
          <tr><th>Value</th><th>Tags</th></tr>
        </thead>
        <tbody>
          <tr v-for="elt in elements" v-bind:key="elt.id">
            <td>{{elt.value}}</td>
            <td>
              <span v-for="tag in elt.tags"
                    v-bind:key="tag.name"
                    class="badge m-1"
                    v-bind:class="{'badge-secondary': !tag.fresh, 'badge-primary': tag.fresh}">
                {{tag.name}}
              </span>
            </td>
          </tr>
        </tbody>
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
      searchQuery: '',
      apipath: `http://localhost:5000/api/observables/filter/`
    }
  },
  methods: {
    fetchObservables () {
      console.log('filtering ' + this.apipath + ' with ' + this.searchQuery)
      var params = {
        value: this.searchQuery
      }
      axios.post(this.apipath, params)
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
