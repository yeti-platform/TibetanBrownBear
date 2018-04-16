<template>
  <!-- Display details nicely -->
  <div v-if="!isEdit" id="detail">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{indicator.name}} <small>{{indicator.type}}</small></h3>
      {{indicator.description || 'No description'}}
      <pre>{{indicator.pattern}}</pre>
    </div>
    <router-link class="btn btn-sm btn-outline-secondary" :to="{name: 'IndicatorEdit'}">Edit</router-link>
  </div>
  <!--  Edit form -->
  <yeti-form :object="indicator"
             :fields="['name', 'pattern']"
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

export default {
  data () {
    return {
      loading: true,
      indicator: {},
      error: {},
      defaultApiPath: `http://localhost:5000/api/indicators/`
    }
  },
  components: {
    YetiForm,
    Fields
  },
  computed: {
    isEdit () {
      return this.$route.path.endsWith('edit')
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
            this.indicator = response.data
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
