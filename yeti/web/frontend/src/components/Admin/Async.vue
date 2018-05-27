<template>
  <div>
    <div class="row">
      <div id="tag-list" class="col-12">
        <p>Click on a line in the table to manipulate Async Jobs.</p>
        <table-filter ref="tagList" :filter-params="filterParams" :multiSelect="false"/>
      </div>
    </div>
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

const apiRoot = `http://localhost:5000/api/async/`

export default {
  components: {
    TableFilter
  },
  data () {
    return {
      filterParams: {
        apiPath: apiRoot + 'filter',
        fields: [
          {name: 'name', type: 'text'},
          {name: 'last_executed', type: 'datetime'},
          {name: 'period', type: 'text'},
          {name: 'enabled', type: 'text'}
        ],
        queryKey: 'name'
      },
      defaultApiPath: apiRoot,
    }
  }
}
</script>

<style lang="css">
</style>
