<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link v-if="type" id="new-entity" class="btn btn-sm btn-outline-secondary" :to="{name: 'NewEntity', params: {type}}">{{"New " + type}}</router-link>
        </div>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  props: ['type']
}
</script>
