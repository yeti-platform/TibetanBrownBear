<template lang="html">
  <yeti-form apiPath="/entities/"
             :object="defaultObjects[type]"
             :fields="editFields[type]"
             v-on:form-submit="navigateToNew"/>
</template>

<script>

import YetiForm from '@/components/scaffolding/YetiForm'
import { editFields, defaultObjects } from './EntityFields.js'

export default {
  components: {
    YetiForm
  },
  data () {
    return {
      defaultObjects: defaultObjects,
      editFields: editFields
    }
  },
  props: ['type'],
  methods: {
    navigateToNew: function (data) {
      this.$router.push({name: 'EntityDetails', params: {id: data.id}})
    }
  }
}
</script>

<style lang="css">
</style>
