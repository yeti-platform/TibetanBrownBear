<template>
  <div class="">
    <input id="filter" @keyup.enter='fetchElements()' v-model="searchQuery" class="form-control form-control-light w-100" type="text" placeholder="Filter query" aria-label="Search">
    <div class="table-responsive">
      <span v-if="loading" class="loading">
        <i class='fas fa-circle-notch fa-spin fa-3x m-3'></i>
      </span>
      <table id="table-filter" v-else class="table table-hover table-sm table-yeti">
        <thead>
          <tr><th v-bind:key="field['name']" v-for="field in filterParams.fields">{{field['name']}}</th></tr>
        </thead>
        <tbody>
          <tr v-for="elt in elements"
              v-bind:key="elt.id"
              @click.exact="select(elt)"
              @click.shift.exact="selectMultiple(elt)"
              v-bind:class="{'selected': selectedElements.includes(elt.id)}">
            <td class="align-middle" v-bind:key="field['name']" v-for="(field, index) in filterParams.fields">
              <router-link v-if="index === 0" :to="{ name: detailComponent, params: {id: elt.id}}">
                <fields :field="field" :elt="elt"/>
              </router-link>
              <fields v-if="index !== 0" :field="field" :elt="elt" />
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
    'value', // value is specified to be able to use v-bind directive on selected items
    'filterParams',
    'detailComponent',
    'autoRefresh'
  ],
  data () {
    return {
      elements: [],
      searchQuery: '',
      loading: true,
      selectedElements: [],
      timer: false
    }
  },
  watch: {
    // call again the method if the route changes
    '$route': 'fetchElements'
  },
  methods: {
    fetchElements () {
      console.log('fetching elements')
      let params = {}
      params[this.filterParams.queryKey] = this.searchQuery
      params['type'] = this.filterParams.typeFilter
      this.loading = true
      axios.post(this.filterParams.apiPath, params)
        .then(response => {
          this.elements = response.data.map(function (elt) {
            elt.selected = false; return elt
          })
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => { this.loading = false })
    },
    select (elt) {
      this.selectedElements = [elt.id]
      this.$emit('input', [elt])
    },
    selectMultiple (elt) {
      if (!this.selectedElements.includes(elt.id)) {
        this.selectedElements.push(elt.id)
      } else {
        this.selectedElements.splice(this.selectedElements.indexOf(elt.id), 1)
      }
      this.$emit('input', this.elements.filter(elt => this.selectedElements.includes(elt.id)))
    },
    clearSelection () {
      this.selectedElements = []
      this.$emit('input', [])
    }
  },
  created () {
    this.fetchElements()
    if (this.autoRefresh) {
      this.timer = setInterval(this.fetchElements, this.autoRefresh * 1000)
    }
  },
  beforeDestroy () {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }
}
</script>

<style lang="css">

.selected {
  background-color: #ffffe4;
}

</style>
