<template lang="html">
  <yeti-form apiPath="http://localhost:5000/api/entities/"
             :object="defaultObject"
             :fields="defaultFields"
             v-on:form-submit="navigateToNew"/>
</template>

<script>

import YetiForm from '@/components/scaffolding/YetiForm'

const defaultFields = {
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
      }
    }
  },
  props: ['type'],
  computed: {
    defaultFields () {
      return defaultFields[this.type]
    },
    defaultObject () {
      return this.defaultObjects[this.type]
    }
  },
  methods: {
    navigateToNew: function (data) {
      console.log(data)
      console.log(data.id)
      this.$router.push({name: 'EntityDetails', params: {id: data.id}})
    }
  }
}
</script>

<style lang="css">
</style>
