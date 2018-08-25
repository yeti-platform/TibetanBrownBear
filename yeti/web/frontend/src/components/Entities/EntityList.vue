<template>
  <div>
    <table-filter :filter-params="filterParams" detailComponent="EntityDetails"/>
    <router-view />
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

const typeFields = {
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'threat-actor': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'attack-pattern': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'}
  ],
  'tool': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'tool_version', type: 'text'}
  ],
  'intrusion-set': [
    {name: 'name', type: 'text'},
    {name: 'labels', type: 'list'},
    {name: 'first_seen', type: 'text'},
    {name: 'last_seen', type: 'text'}
  ]
}

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
