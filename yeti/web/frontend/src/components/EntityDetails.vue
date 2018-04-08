<template>
  <div id="detail">
    <div v-if="loading">
      Loading info on Entity {{ $route.params.id }}...
    </div>
    <div v-else>
      <h3>{{entity.name}} <small>{{entity.type}}</small></h3>
      {{entity.description || 'No description'}}
    </div>
  </div>
</template>

<script>
import axios from 'axios'

let defaultApiPath = `http://localhost:5000/api/entities/`

export default {
  data () {
    return {
      loading: true,
      entity: {},
      error: {}
    }
  },
  methods: {
    fetchInfo () {
      console.log('Fetching info')
      axios.get(defaultApiPath + this.$route.params.id)
        .then(response => {
          this.entity = response.data
        })
        .catch(error => {
          console.log(error)
          this.error = error
        })
        .finally(() => { this.loading = false })
    }
  },
  mounted () {
    this.fetchInfo()
  }

}
</script>

<style lang="css">
</style>
