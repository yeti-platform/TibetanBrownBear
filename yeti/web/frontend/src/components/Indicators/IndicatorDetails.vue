<template>
  <!-- Display details nicely -->
  <div v-if="!edit" id="detail">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{indicator.name}} <small>{{indicator.type}}</small></h3>
      {{indicator.description || 'No description'}}
      <pre>{{indicator.pattern}}</pre>
    </div>
    <button class="btn btn-sm btn-outline-secondary" @click="toggleEdit">Edit</button>
  </div>
  <!--  Edit form -->
  <yeti-form v-bind:object="indicator"
             v-bind:fields="['name', 'pattern']"
             v-bind:apiPath="this.defaultApiPath+$route.params.id+'/'"
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
      edit: false,
      defaultApiPath: `http://localhost:5000/api/indicators/`
    }
  },
  components: {
    YetiForm,
    Fields
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
      this.edit = !this.edit
    }
  },
  mounted () {
    this.fetchInfo()
  }
}
</script>

<style lang="css">
</style>
