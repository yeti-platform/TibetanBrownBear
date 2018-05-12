<template>
    <table-filter :filter-params="filterParams" detailComponent="IndicatorDetails"/>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'

const typeFields = {
  'regex': [
    {name: 'name', type: 'text'},
    {name: 'pattern', type: 'code'}
  ],
  'yara': [
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
        'regex': {
          type: 'indicator.regex',
          pattern: ''
        },
        'yara': {
          type: 'indicator.yara'
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
        apiPath: `http://localhost:5000/api/indicators/filter/`,
        fields: typeFields[this.type],
        queryKey: 'name',
        typeFilter: this.type
      }
    }
  },
  methods: {
    navigateToNew (object) {
      this.$router.push({name: 'IndicatorDetails', params: {id: object.data.id}})
    }
  }
}
</script>
