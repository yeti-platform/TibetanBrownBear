<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <button class="btn btn-sm btn-outline-secondary">+ New entity</button>
        </div>
      </div>
    </div>
    <table-filter :fields="fields" :apipath="apipath" :querykey='querykey'></table-filter>
  </div>
</template>

<script>
import TableFilter from '@/components/helpers/TableFilter'
export default {
  data () {
    return {
      fields: ['name'],
      apipath: `http://localhost:5000/api/entities/filter/`,
      querykey: 'name'
    }
  },
  components: {
    TableFilter
  },
  props: ['searchQuery']
}
</script>
