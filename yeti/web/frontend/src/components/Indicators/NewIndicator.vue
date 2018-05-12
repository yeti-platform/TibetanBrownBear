<template lang="html">
  <yeti-form apiPath="http://localhost:5000/api/indicators/"
             :object="defaultObject"
             :fields="defaultFields"
             v-on:form-submit="navigateToNew"/>
</template>

<script>

import YetiForm from '@/components/scaffolding/YetiForm'

const defaultFields = {
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
    YetiForm
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
      this.$router.push({name: 'IndicatorDetails', params: {id: data.id}})
    }
  }
}
</script>

<style lang="css">
</style>
