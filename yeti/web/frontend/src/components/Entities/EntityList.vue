<template>
  <div>
    <table-filter :filter-params="filterParams" detailComponent="EntityDetails"/>
    <router-view />
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import { typeFields } from './EntityFields.js'

export default {
  components: {
    TableFilter
  },
  props: ['type'],
  computed: {
    filterParams () {
      return {
        apiPath: `http://localhost:5000/api/entities/filter/`,
        fields: typeFields[this.type],
        queryKey: 'name',
        typeFilter: this.type
      }
    }
  }
}
</script>
