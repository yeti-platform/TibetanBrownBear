<template>
  <div>
    <div class="row">
      <div v-bind:class="[hasTagSelection ? 'col-8' : 'col-12' ]">
        <p>Click on a line in the table to edit tags.</p>
        <table-filter ref="tagList" :filter-params="filterParams" v-model="selectedTags" :multiSelect="false"/>
      </div>
      <div class="col-4" v-if="selectedTags.length > 0">
        <yeti-form :object="selectedTags[0]"
                   :fields="['name', 'default_expiration']"
                   :apiPath="defaultApiPath+selectedTags[0].id+'/'"
                   method='PUT'
                   :onSaveCallback='clearSelection'
                   />
      </div>
    </div>
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

const apiRoot = `http://localhost:5000/api/tags/`

export default {
  components: {
    TableFilter,
    YetiForm
  },
  data () {
    return {
      filterParams: {
        apiPath: apiRoot + 'filter/',
        fields: ['name', 'count', 'created_at', 'default_expiration'],
        querykey: 'name'
      },
      defaultApiPath: apiRoot,
      selectedTags: []
    }
  },
  computed: {
    hasTagSelection () {
      return this.selectedTags.length > 0
    }
  },
  methods: {
    clearSelection (response) {
      this.selectedTags = []
      this.$refs.tagList.clearSelection()
    }
  }
}
</script>

<style lang="css">
</style>
