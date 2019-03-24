<template>
  <table-filter v-if="!id" :filter-params="filterParams" detailComponent="ObservableDetails"></table-filter>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

export default {
  components: {
    TableFilter
  },
  props: ['id'],
  data () {
    return {
      filterParams: {
        apiPath: `/observables/filter/`,
        fields: [
          { name: 'value', type: 'text' },
          { name: 'tags', type: 'tags' }
        ],
        queryKey: 'value'
      }
    }
  }
}
</script>
