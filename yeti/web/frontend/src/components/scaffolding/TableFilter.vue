<template>
  <div class="">
    <input @keyup.enter='getElements()' v-model="searchQuery" class="form-control form-control-light w-100" type="text" placeholder="Filter query" aria-label="Search">
    <div class="table-responsive">
      <div v-if="loading">
        Loading...
      </div>
      <table v-else class="table table-hover table-compact table-sm table-yeti">
        <thead>
          <tr><th v-bind:key="field" v-for="field in filterParams.fields">{{field}}</th></tr>
        </thead>
        <tbody>
          <tr v-for="elt in elements"
              v-bind:key="elt.id"
              @click.exact="select(elt)"
              @click.shift.exact="selectMultiple(elt)"
              v-bind:class="{'selected': selectedElements.includes(elt.id)}">
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
  props: ['value', 'filterParams', 'detailComponent'],
  data () {
    return {
      elements: [],
      searchQuery: '',
      loading: true,
      selectedElements: []
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
          this.elements = response.data.map(function (elt) {
            elt.selected = false; return elt
          })
          this.loading = false
        })
        .catch(error => {
          console.log(error)
        })
    },
    getElements () {
      this.fetchElements()
    },
    select (elt) {
      this.selectedElements = [elt.id]
      this.$emit('input', [elt])
    },
    selectMultiple (elt, event) {
      if (!this.selectedElements.includes(elt.id)) {
        this.selectedElements.push(elt.id)
      } else {
        this.selectedElements.splice(this.selectedElements.indexOf(elt.id), 1)
      }
      this.$emit('input', this.elements.filter(elt => this.selectedElements.includes(elt.id)))
    },
    clearSelection () {
      console.log('clearing selection')
      this.selectedElements = []
    }
  },
  created () {
    this.getElements()
  }
}
</script>

<style lang="css">
.selected {
  font-weight: bold;
}

.table-yeti {
            user-select: none; /* CSS3 (little to no support) */
        -ms-user-select: none; /* IE 10+ */
       -moz-user-select: none; /* Gecko (Firefox) */
    -webkit-user-select: none; /* Webkit (Safari, Chrome) */
}
</style>
