<template>
  <div class="">
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link class="btn btn-sm btn-outline-secondary" to="/entities/malware/new">New</router-link>
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
// import TableFilter from '@/components/helpers/TableFilter'
// import YetiForm from '@/components/scaffolding/YetiForm'
import { generateRoutes } from '@/router/helpers'

const subComponents = [
  { name: 'malware', fields: ['name', 'family'] },
  { name: 'actor', fields: ['name'] }
]

let defaults = {
  defaultApiPath: `http://localhost:5000/api/entities/filter/`,
  defaultTypePrefix: 'entity.',
  defaultQuerykey: 'name'
}
let routes = generateRoutes(subComponents, defaults)
console.log(routes)
export default {
  childrenRoutes: routes,
  props: ['searchQuery']
  // components: {
  //   TableFilter,
  //   YetiForm
  // }
}
</script>
