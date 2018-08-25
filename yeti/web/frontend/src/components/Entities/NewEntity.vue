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
        'malware': {
          type: 'malware',
          labels: []
        },
        'threat-actor': {
          type: 'threat-actor',
          labels: []
        },
        'attack-pattern': {
          type: 'attack-pattern',
          labels: []
        },
        'tool': {
          type: 'tool',
          labels: []
        },
        'intrusion-set': {
          type: 'intrusion-set',
          labels: []
        },
      },
      defaultFields: {
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
          {name: 'labels', type: 'list'}
        ],
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
