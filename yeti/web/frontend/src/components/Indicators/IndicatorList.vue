<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">{{indicatorTypeHuman.plural}}</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link v-if="type" id="new-indicator" class="btn btn-sm btn-outline-secondary" :to="{name: 'NewIndicator', params: {type}}">{{"New " + indicatorTypeHuman.singular}}</router-link>
        </div>
      </div>
    </div>
    <table-filter :filter-params="filterParams" detailComponent="IndicatorDetails"/>
    <router-view />
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import { listFields } from './IndicatorFields.js'
import { indicatorTypes } from './IndicatorTypes.js'

export default {
  components: {
    TableFilter
  },
  props: ['type'],
  computed: {
    filterParams () {
      return {
        apiPath: `/indicators/filter/`,
        fields: listFields[this.type],
        queryKey: 'name',
        typeFilter: this.type
      }
    },
    indicatorTypeHuman () {
      return indicatorTypes[this.type]
    }
  }
}
</script>
