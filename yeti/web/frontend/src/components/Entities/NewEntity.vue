<template lang="html">
  <yeti-form apiPath="http://localhost:5000/api/entities/"
             :object="defaultObjects[type]"
             :fields="typeFields[type]"
             v-on:form-submit="navigateToNew"/>
</template>

<script>

import YetiForm from '@/components/scaffolding/YetiForm'
import { typeFields, defaultObjects } from './EntityFields.js'

export default {
  components: {
    YetiForm
  },
  data () {
    return {
      defaultObjects: defaultObjects,
      typeFields: typeFields
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
