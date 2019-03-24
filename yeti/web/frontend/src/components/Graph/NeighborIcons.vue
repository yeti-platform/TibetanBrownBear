<template>
  <div class='neighbor-icons'>
    <div v-for="type in Object.keys(countByType)" v-bind:key="type" class="float-left mr-3 neighbor-icon-single">
      <type-to-icon :type="type"></type-to-icon>
      <span class="badge badge-pill badge-light"> {{countByType[type]}}</span>
    </div>
  </div>

</template>

<script>
import TypeToIcon from '@/components/scaffolding/TypeToIcon'

export default {
  components: {
    TypeToIcon
  },
  props: {
    entity: Object,
    neighbors: { type: Object, default: function () { return { edges: [], vertices: [] } } }
  },
  data () {
    return {
      countByType: {}
    }
  },
  methods: {
    countNeighborsByType () {
      let count = {}
      let relevantIds = new Set(
        (this.neighbors.edges)
          .filter(edge => edge.source_ref === this.entity.id || edge.target_ref === this.entity.id)
          .map(edge => edge.source_ref === this.entity.id ? edge.target_ref : edge.source_ref)
      )
      let relevantVertices = Object.values(this.neighbors.vertices).filter(vertice => relevantIds.has(vertice.id))
      relevantVertices.map(neighbor => {
        count[neighbor.type] = (count[neighbor.type] || 0) + 1
      })
      this.countByType = count
    }
  },
  mounted () {
    this.countNeighborsByType()
  },
  watch: {
    'neighbors': 'countNeighborsByType'
  }
}
</script>

<style>

.neighbor-icon-single {
  min-width: 3em;
}

.neighbor-icons {
  opacity: 0.7;
}

.neighbor-data:hover .neighbor-icons {
  opacity: 1;
}

</style>
