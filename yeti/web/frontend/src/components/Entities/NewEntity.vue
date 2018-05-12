<template lang="html">
  <yeti-form apiPath="http://localhost:5000/api/entities/"
             :object="defaultObjects[type]"
             :fields="defaultFields[type]"
             v-on:form-submit="navigateToNew"/>
</template>

<script>

import YetiForm from '@/components/scaffolding/YetiForm'

export default {
  components: {
    YetiForm
  },
  data () {
    return {
      defaultObjects: {
        malware: {
          type: 'entity.malware',
          family: []
        },
        actor: {
          type: 'entity.actor'
        }
      },
      defaultFields: {
        'malware': [
          {name: 'name', type: 'text'},
          {name: 'family', type: 'list'}
        ],
        'actor': [
          {name: 'name', type: 'text'}
        ]
      }
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
