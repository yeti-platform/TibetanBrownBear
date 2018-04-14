<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link class="btn btn-sm btn-outline-secondary" :to="'/entities/'+subType+'/new'">New {{subType}}</router-link>
        </div>
      </div>
    </div>

    <nav class="nav nav-pills flex-column flex-sm-row">
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/entities/malware">Malware</router-link>
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/entities/actor">Actors</router-link>
    </nav>

    <table-filter :filter-params="filterParams"/>

  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

const typeFields = {
  'malware': ['name', 'family'],
  'actor': ['name']
}

export default {
  components: {
    TableFilter
  },
  computed: {
    subType () {
      return this.$route.params.type
    },
    filterParams () {
      let type = this.$route.params.type
      return {
        apiPath: `http://localhost:5000/api/entities/filter/`,
        fields: typeFields[type],
        querykey: 'name',
        typeFilter: type
      }
    }
  }
}
</script>
