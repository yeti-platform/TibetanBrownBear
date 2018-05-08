<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Observables</h1>
    </div>
    <router-view />
    <table-filter v-if="!id" :filter-params="filterParams" detailComponent="ObservableDetails"></table-filter>
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

export default {
  components: {
    TableFilter
  },
  props: [
    'id'
  ],
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
