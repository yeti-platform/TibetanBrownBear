<template>
  <!-- Display details nicely -->
  <div v-if="!isEdit" id="detail">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{observable.value}} <small>{{observable.type}}</small></h3>
      {{observable.description || 'No description'}}
    </div>
    <router-link class="btn btn-sm btn-outline-secondary" :to="{name: 'ObservableEdit'}">Edit</router-link>
  </div>
  <!--  Edit form -->

  <yeti-form :object="observable"
             :fields="observableFields"
             :apiPath="this.defaultApiPath+$route.params.id+'/'"
             method='PUT'
             :onSaveCallback='toggleEdit'
             v-else
             />
</template>

<script>
import axios from 'axios'
import YetiForm from '@/components/scaffolding/YetiForm'
import Fields from '@/components/helpers/Fields'

const typeFields = {
  'hostname': [
    {name: 'value', type: 'text'},
    {name: 'tags', type: 'tags'}
  ]
}

export default {
  data () {
    return {
      loading: true,
      observable: {},
      error: {},
      defaultApiPath: `http://localhost:5000/api/observables/`
    }
  },
  components: {
    YetiForm,
    Fields
  },
  beforeRouteUpdate (to, from, next) {
    this.fetchInfo()
    next()
  },
  computed: {
    isEdit () {
      return this.$route.path.endsWith('edit')
    },
    observableType () {
      if (this.observable.type) {
        let arr = this.observable.type.split('.')
        return arr[arr.length - 1]
      }
    },
    observableFields () {
      return typeFields[this.observableType]
    }
  },
  methods: {
    fetchInfo () {
      console.log('Fetching info')
      axios.get(this.defaultApiPath + this.$route.params.id)
        .then(response => {
          if (response.status !== 200) {
            this.error = response.data
          } else {
            this.observable = response.data
          }
        })
        .catch(error => {
          console.log(error)
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
