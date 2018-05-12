<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">Indicators</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link v-if="type" id="new-entity" class="btn btn-sm btn-outline-secondary" :to="{name: 'NewIndicator', params: {type}}">{{"New " + type}}</router-link>
        </div>
      </div>
    </div>
    <nav class="nav nav-pills flex-column flex-sm-row">
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/indicators/regex">Regular expressions</router-link>
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/indicators/yara">Yara rules</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  props: ['type']
}
</script>
