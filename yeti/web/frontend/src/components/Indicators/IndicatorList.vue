<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <button v-if="type" class="btn btn-sm btn-outline-secondary" @click="() => {newIndicator = !newIndicator}">
            {{newIndicator ? "Cancel" : "New " + type}}
          </button>
        </div>
      </div>
    </div>
    <nav class="nav nav-pills flex-column flex-sm-row">
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/indicators/regex">Regular expressions</router-link>
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/indicators/yara">Yara rules</router-link>
    </nav>
    <router-view />
    <table-filter v-if="!id && type && !newIndicator" :filter-params="filterParams" detailComponent="IndicatorDetails"/>
    <yeti-form v-if="newIndicator"
               apiPath="http://localhost:5000/api/indicators/"
               :object="defaultObject"
               :fields="subTypeFields"
               :onSaveCallback='navigateToNew'/>
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

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
    TableFilter,
    YetiForm
  },
  data () {
    return {
      newIndicator: false,
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
      let type = this.type
      return {
        apiPath: `http://localhost:5000/api/indicators/filter/`,
        fields: typeFields[type],
        queryKey: 'name',
        typeFilter: type
      }
    },
    defaultObject () {
      return this.defaultObjects[this.type]
    }
  },
  methods: {
    navigateToNew (object) {
      this.newIndicator = false
      this.$router.push({name: 'IndicatorDetails', params: {id: object.data.id}})
    }
  }
}
</script>
