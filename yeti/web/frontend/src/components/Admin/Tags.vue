<template>
  <div>
    <p>Click on a tag name to do things. Right now, this does nothing. But it should definitely do something. What? Good question.</p>
    <table-filter :filter-params="filterParams"/>
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
        apiPath: `http://localhost:5000/api/tags/filter/`,
        fields: ['name', 'count', 'created_at', 'default_expiration'],
        querykey: 'name'
      }
    }
  }
}
</script>

<style lang="css">
</style>
