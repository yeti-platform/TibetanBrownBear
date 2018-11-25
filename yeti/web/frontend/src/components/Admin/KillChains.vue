<template>
  <div>
    <div v-bind:key="killChain.id" v-for="killChain in killChains" class="killchain mt-4 mb-4">
      <h3>{{killChain.human_name}}</h3>Slug: <code>{{killChain.name}}</code>
      <p>{{killChain.description}}</p>
      <div>

        <div class="form-row">
          <div class='col col-md-3'><p>Phase name</p></div>
          <div class='col'><p>Phase description</p></div>
        </div>

        <div class="form-row show-on-hover" v-for="phase in killChain.settings[killChain.name]" v-bind:key="phase.name">
          <div class="col col-md-3">
            <input class="form-control " type="text" v-model="phase.name">
          </div>
          <div class="col">
            <input class="form-control " type="text" v-model="phase.description">
          </div>
          <div class="form-group">
            <a href="#" class="btn btn-outline-danger show-on-hover" @click="removeField(killChain.settings[killChain.name], phase)">
              <i class="fas fa-fw fa-lg fa-minus-circle"></i>
              </a>
          </div>
        </div>

        <div class="form-inline">
          <div class="form-row">
            <div class="col">
              <button v-bind:class="{ disabled: saving }" class="btn btn-light mr-2" @click="addField(killChain.settings[killChain.name])">
              Add phase
              </button>
              <button v-bind:class="{ disabled: saving }" class="btn btn-primary" @click="updateKillChain(killChain, killChain.settings[killChain.name])">
                {{saving ? "Saving..." : "Save changes"}}
              </button>
            </div>
          </div>
        </div>

      </div>

      <hr>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      killChains: [],
      saving: false
    }
  },
  methods: {
    fetchKillChains () {
      axios.get('/settings/killchains')
        .then(response => {
          this.killChains = response.data
        })
    },
    updateKillChain (killChain, phases) {
      this.saving = true
      axios.put('/settings/killchains/' + killChain.name + '/', {phases: phases})
        .then(response => {
          killChain = response.data
        })
        .catch(error => {
          this.errors = error.response.data
        })
        .finally(() => {
          this.saving = false
        })
    },
    addField (killChainPhases) {
      killChainPhases.push({name: '', description: ''})
    },
    removeField (killChainPhases, phase) {
      killChainPhases.splice(killChainPhases.indexOf(phase), 1)
      console.log(killChainPhases)
    }
  },
  mounted () {
    this.fetchKillChains()
  }
}
</script>

<style lang="css">

  a.show-on-hover {
    opacity: 0;
  }

  div.show-on-hover:hover .show-on-hover {
    opacity: 1;
  }

</style>
