<template>
  <div class="">
    <input @keyup.enter='getElements()' v-model="searchQuery" class="form-control form-control-light w-100" type="text" placeholder="Filter query" aria-label="Search">
    <div class="table-responsive">
      <div v-if="loading">
        Loading...
      </div>
      <table v-else class="table table-hover table-compact table-sm">
        <thead>
          <tr><th v-bind:key="field" v-for="field in filterParams.fields">{{field}}</th></tr>
        </thead>
        <tbody>
          <tr v-for="elt in elements" v-bind:key="elt.id">
            <td v-bind:key="field" v-for="(field, index) in filterParams.fields">
              <router-link v-if="index === 0" :to="{ name: detailComponent, params: {id: elt.id}}">
                <fields :field="field" :value="elt[field]"/>
              </router-link>
              <fields v-if="index !== 0" :field="field" :value="elt[field]"/>
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
  props: ['filterParams', 'detailComponent'],
  data () {
    return {
      elements: [],
      searchQuery: '',
      loading: true
    }
  },
  watch: {
    // call again the method if the route changes
    '$route': 'getElements'
  },
  methods: {
    fetchElements () {
      console.log('filtering ' + this.filterParams.apiPath + ' with ' + this.filterParams.querykey + ':' + this.searchQuery)
      var params = {}
      params[this.filterParams.querykey] = this.searchQuery
      params['type'] = this.filterParams.typeFilter
      axios.post(this.filterParams.apiPath, params)
        .then(response => {
          this.elements = response.data
          this.loading = false
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
