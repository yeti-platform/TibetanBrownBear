<template>
  <!-- Display details nicely -->
  <div v-if="!edit" class="indicator-details">
    <div class="loading" v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{indicator.name}} <small>{{indicator.type}}</small></h3>
      {{indicator.description || 'No description'}}
      <pre>{{indicator.pattern}}</pre>
    </div>
    <router-link class="edit btn btn-sm btn-outline-secondary" :to="{name: 'IndicatorEdit', params: {id: id}}">Edit</router-link>
  </div>

  <!--  Edit form -->
  <!-- yeti-form should use emit instead of an onSaveCallback -->
  <yeti-form :object="indicator"
             :fields="indicatorFields"
             :apiPath="defaultApiPath+id+'/'"
             method='PUT'
             v-on:form-submit='toggleEdit'
             v-else
             />
</template>

<script>
import axios from 'axios'
import YetiForm from '@/components/scaffolding/YetiForm'
import Fields from '@/components/helpers/Fields'

const typeFields = {
  'regex': [
    {name: 'name', type: 'text'},
    {name: 'pattern', type: 'code'}
  ],
  'yara': [
    {name: 'name', type: 'text'}
  ]
}

export default {
  data () {
    return {
      loading: true,
      indicator: {},
      error: {},
      defaultApiPath: `http://localhost:5000/api/indicators/`
    }
  },
  props: { id: String, edit: Boolean },
  components: {
    YetiForm,
    Fields
  },
  beforeRouteUpdate (to, from, next) { // how do we test this?
    this.fetchInfo()
    next()
  },
  computed: {
    indicatorType () {
      if (this.indicator.type) {
        let arr = this.indicator.type.split('.')
        return arr[arr.length - 1]
      }
    },
    indicatorFields () {
      return typeFields[this.indicatorType]
    }
  },
  methods: {
    fetchInfo () {
      axios.get(this.defaultApiPath + this.id)
        .then(response => {
          if (response.status !== 200) {
            this.error = response.data
          } else {
            this.indicator = response.data
          }
        })
        .catch(error => { // how do we catch 404 errors?
          this.error = error
        })
        .finally(() => { this.loading = false })
    },
    toggleEdit () {
      this.$router.go(-1)
    }
  },
  mounted () {
    this.fetchInfo()
  }
}
</script>

<style lang="css">
</style>
