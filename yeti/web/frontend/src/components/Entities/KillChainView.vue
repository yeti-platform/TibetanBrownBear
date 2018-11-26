<template>
    <div>
      <ul class="nav nav-tabs mb-3" id="tabs-tab" role="tablist">
        <li class="nav-item" v-for="killchain in killchains" v-bind:key="killchain.name">
          <a class="nav-link" :id="killchain.name+'-tab'" data-toggle="pill" :href="'#'+killchain.name" role="tab" :aria-controls="killchain.name" aria-selected="true">{{killchain.name}}</a>
        </li>
      </ul>
      <div class="tab-content" id="pills-tabContent">
        <div v-for="killchain in killchains" v-bind:key="killchain.name" class="tab-pane" :id="killchain.name" role="tabpanel" :aria-labelledby="killchain.name+'-tab'">
          <table class="table">
            <tr v-for="phase in getPhases(killchain)" v-bind:key="phase.name">
              <th>{{phase.name}}</th>
              <td class="neighbor-data" v-for="neighbor in neighborsPerKillchain[killchain.name][phase.name]" v-bind:key="killchain.name + phase.name + neighbor.id">
                <router-link :to="{ name: 'EntityDetails', params: {id: neighbor.id}}">
                  <type-to-icon :type="neighbor.type"></type-to-icon>{{neighbor.name}}
                </router-link>
                <neighbor-icons :entity="neighbor" :neighbors="extendedGraph"></neighbor-icons>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'
import TypeToIcon from '@/components/scaffolding/TypeToIcon'
import NeighborIcons from '@/components/Graph/NeighborIcons'

export default {
  components: {
    TypeToIcon,
    NeighborIcons
  },
  props: ['entity'],
  data () {
    return {
      killchains: [],
      extendedGraph: {},
      neighborsPerKillchain: {}
    }
  },
  methods: {
    getKillchains () {
      axios.get('/settings/killchains/')
        .then(response => {
          this.killchains = response.data
          var neighborsPerKillchain = {}
          for (var killchain of this.killchains) {
            neighborsPerKillchain[killchain.name] = {}
            for (var phase of killchain.settings[killchain.name]) {
              neighborsPerKillchain[killchain.name][phase.name] = []
            }
          }
          this.neighborsPerKillchain = neighborsPerKillchain
          this.getNeighbors()
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => {})
    },
    getPhases (killchain) {
      return killchain.settings[killchain.name]
    },
    getNeighbors () {
      axios.post('/entities/' + this.entity.id + '/neighbors/')
        .then(response => {
          this.sortNeighborsByPhase(response.data)
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => {})

      let extendedGraphParams = {
        hops: 2,
        include_original: true
      }
      axios.post('/entities/' + this.entity.id + '/neighbors/', extendedGraphParams)
        .then(response => {
          console.log('(kc extended) got ' + response.data.edges.length + ' edges')
          this.extendedGraph = response.data
        })
        .finally(() => { this.loading = false })
    },
    sortNeighborsByPhase (neighbors) {
      for (var neighbor of Object.values(neighbors.vertices)) {
        if (neighbor.kill_chain_phases === undefined) { return }
        neighbor.kill_chain_phases.map(phase => {
          this.neighborsPerKillchain[phase.kill_chain_name][phase.phase_name].push(neighbor)
        })
      }
    }
  },
  mounted () {
    this.getKillchains()
  }
}
</script>

<style>

</style>
