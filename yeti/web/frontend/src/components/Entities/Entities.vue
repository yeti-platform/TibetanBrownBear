<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link id="new-entity" class="btn btn-sm btn-outline-secondary" :to="{name: 'NewEntity', params: {type}}">{{"New " + type}}</router-link>
        </div>
      </div>
    </div>
    <nav class="nav nav-pills flex-column flex-sm-row">
      <router-link id="malware" class="flex-sm-fill text-sm-center nav-link" :to="{name: 'EntityList', params: {type: 'malware'}}">Malware</router-link>
      <router-link id="actor" class="flex-sm-fill text-sm-center nav-link" :to="{name: 'EntityList', params: {type: 'actor'}}">Actors</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

export default {
  components: {
    TableFilter,
    YetiForm
  },
  data () {
    return {}
  },
  props: ['type'],
  computed: {
  },
  methods: {
    // catch emitted event from new or save form
  }
}
</script>
