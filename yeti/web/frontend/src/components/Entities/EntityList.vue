<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">{{entityTypeHuman.plural}}</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link v-if="type" id="new-entity" class="btn btn-sm btn-outline-secondary" :to="{name: 'NewEntity', params: {type}}">{{"New " + entityTypeHuman.singular}}</router-link>
        </div>
      </div>
    </div>
    <table-filter :filter-params="filterParams" detailComponent="EntityDetails"/>
    <router-view />
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import { listFields } from './EntityFields.js'
import { entityTypes } from './EntityTypes.js'

export default {
  components: {
    TableFilter
  },
  props: ['type'],
  computed: {
    filterParams () {
      return {
        apiPath: `/entities/filter/`,
        fields: listFields[this.type],
        queryKey: 'name',
        typeFilter: this.type
      }
    },
    entityTypeHuman () {
      return entityTypes[this.type]
    }
  }
}
</script>
