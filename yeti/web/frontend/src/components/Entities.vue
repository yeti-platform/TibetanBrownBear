<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <button class="btn btn-sm btn-outline-secondary">New entity</button>
        </div>
      </div>
    </div>
    <table-filter :fields="fields" :apipath="apipathFilter" :querykey='querykey'></table-filter>
    <yeti-form :fields="fields" :apipath="apipathUpdate" :type="type"/>
  </div>
</template>

<script>
import TableFilter from '@/components/helpers/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'
export default {
  data () {
    return {
      fields: ['name', 'family'],
      type: 'entities.malware',
      apipathFilter: `http://localhost:5000/api/entities/filter/`,
      apipathUpdate: `http://localhost:5000/api/entities/`,
      querykey: 'name'
    }
  },
  components: {
    TableFilter,
    YetiForm
  },
  props: ['searchQuery']
}
</script>
