<template>
    <table-filter :filter-params="filterParams" detailComponent="EntityDetails"/>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

const typeFields = {
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'family', type: 'list'}
  ],
  'actor': [
    {name: 'name', type: 'text'}
  ]
}

export default {
  components: {
    TableFilter
  },
  data () {
    return {
      defaultObjects: {
        'malware': {
          type: 'entity.malware',
          family: []
        },
        'actor': {
          type: 'entity.actor'
        }
      }
    }
  },
  props: ['id', 'type'],
  computed: {
    subTypeFields () {
      return typeFields[this.type]
    },
    filterParams () {
      return {
        apiPath: `http://localhost:5000/api/entities/filter/`,
        fields: typeFields[this.type],
        queryKey: 'name',
        typeFilter: this.type
      }
    }
  },
  methods: {
    navigateToNew (object) {
      this.$router.push({name: 'EntityDetails', params: {id: object.data.id}})
    }
  }
}
</script>
