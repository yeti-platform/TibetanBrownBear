<template lang="html">
  <yeti-form apiPath="http://localhost:5000/api/indicators/"
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
        'regex': {
          type: 'indicator.regex',
          pattern: ''
        },
        'yara': {
          type: 'indicator.yara'
        }
      },
      defaultFields: {
        'regex': [
          {name: 'name', type: 'text'},
          {name: 'pattern', type: 'code'}
        ],
        'yara': [
          {name: 'name', type: 'text'}
        ]
      }
    }
  },
  props: ['type'],
  methods: {
    navigateToNew: function (data) {
      this.$router.push({name: 'IndicatorDetails', params: {id: data.id}})
    }
  }
}
</script>

<style lang="css">
</style>
