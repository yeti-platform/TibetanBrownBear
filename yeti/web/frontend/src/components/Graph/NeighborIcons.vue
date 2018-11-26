<template>
  <div class='neighbor-icons'>
    <div v-for="type in Object.keys(countByType)" v-bind:key="type" class="float-left mr-3 neighbor-icon-single">
      <type-to-icon :type="type"></type-to-icon>
      <span class="badge badge-pill badge-light"> {{countByType[type]}}</span>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import TypeToIcon from '@/components/scaffolding/TypeToIcon'

export default {
  components: {
    TypeToIcon
  },
  props: ['entity'],
  data () {
    return {
      neighbors: [],
      countByType: {}
    }
  },
  methods: {
    getNeighbors () {
      axios.get('/entities/' + this.entity.id + '/neighbors/')
        .then(response => {
          this.neighbors = response.data
          this.countNeighborsByType()
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => {})
    },
    countNeighborsByType () {
      let count = {}
      Object.values(this.neighbors.vertices).map(neighbor => {
        count[neighbor.type] = (count[neighbor.type] || 0) + 1;
      })
      this.countByType = count
    }
  },
  mounted () {
    this.getNeighbors()
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
