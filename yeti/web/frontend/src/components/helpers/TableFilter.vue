<template>
  <div class="">
    <input @keyup.enter='getElements()' v-model="searchQuery" class="form-control form-control-light w-100" type="text" placeholder="Filter query" aria-label="Search">
    <div class="table-responsive">
      <table class="table table-hover table-compact table-sm">
        <thead>
          <tr><th v-bind:key="field" v-for="field in fields">{{field}}</th></tr>
        </thead>
        <tbody>
          <tr v-for="elt in elements" v-bind:key="elt.id">
            <td v-bind:key="field" v-for="field in fields">
              <fields :field="field" :value="elt[field]"/>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Fields from '@/components/helpers/Fields'

export default {
  components: {
    Fields
  },
  props: [
    'apipath',
    'fields'
  ],
  data () {
    return {
      elements: [],
      searchQuery: ''
    }
  },
  methods: {
    fetchElements () {
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
    getElements () {
      this.fetchElements()
    }
  },
  created () {
    this.getElements()
  }
}
</script>
