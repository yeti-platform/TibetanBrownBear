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
    <table-filter :filter-params="filterParams"></table-filter>
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

export default {
  components: {
    TableFilter
  },
  data () {
    return {
      filterParams: {
        apiPath: `http://localhost:5000/api/observables/filter/`,
        fields: [
          {name: 'value', type: 'text'},
          {name: 'tags', type: 'tags'}
        ],
        querykey: 'value'
      }
    }
  }
}
</script>
