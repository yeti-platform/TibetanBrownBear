<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link class="btn btn-sm btn-outline-secondary" :to="'/entities/'+extractedSubtype+'/new'">New {{extractedSubtype}}</router-link>
        </div>
      </div>
    </div>

    <nav class="nav nav-pills flex-column flex-sm-row">
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/entities/malware">Malware</router-link>
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/entities/actor">Actors</router-link>
    </nav>

    <router-view/>

  </div>
</template>

<script>
import { generateRoutes } from '@/router/helpers'

const subComponents = [
  { name: 'malware', fields: ['name', 'family'] },
  { name: 'actor', fields: ['name'] }
]

let defaults = {
  apiPath: `http://localhost:5000/api/entities/`,
  typePrefix: 'entity.',
  querykey: 'name',
  onSaveCallback: function (response) {
    this.$router.push({name: 'EntityDetails', params: {id: response.data.id}})
  }
}

let routes = generateRoutes(subComponents, defaults)

export default {
  childrenRoutes: routes,
  props: ['searchQuery'],
  data () {
    return {
      subType: 'malware'
    }
  },
  computed: {
    extractedSubtype () {
      return this.$route.path.split('/').slice(-1)[0]
    }
  }
}
</script>
