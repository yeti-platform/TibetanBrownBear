<template>
  <!-- Display details nicely -->
  <div v-if="!isEdit" id="detail">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{entity.name}} <small>{{entity.type}}</small></h3>
      <fields :field="{'type': 'list', 'name': 'family'}"  :elt="entity" />
      {{entity.description || 'No description'}}
    </div>
    <router-link class="btn btn-sm btn-outline-secondary" :to="{name: 'EntityEdit'}">Edit</router-link>
  </div>
  <!--  Edit form -->

  <yeti-form :object="entity"
             :fields="entityFields"
             :apiPath="this.defaultApiPath+$route.params.id+'/'"
             method='PUT'
             :onSaveCallback='toggleEdit'
             v-else
             />
</template>

<script>
import axios from 'axios'
import YetiForm from '@/components/scaffolding/YetiForm'
import Fields from '@/components/helpers/Fields'

const typeFields = {
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'family', type: 'list', autocompleteValues: ['trojan', 'banker']}
  ],
  'actor': [
    {name: 'name', type: 'text'}
  ]
}

export default {
  data () {
    return {
      loading: true,
      entity: {},
      error: {},
      defaultApiPath: `http://localhost:5000/api/entities/`
    }
  },
  components: {
    YetiForm,
    Fields
  },
  computed: {
    isEdit () {
      return this.$route.path.endsWith('edit')
    },
    entityType () {
      let arr = this.entity.type.split('.')
      return arr[arr.length - 1]
    },
    entityFields () {
      return typeFields[this.entityType]
    }
  },
  methods: {
    fetchInfo () {
      console.log('Fetching info')
      axios.get(this.defaultApiPath + this.$route.params.id)
        .then(response => {
          if (response.status !== 200) {
            this.error = response.data
          } else {
            this.entity = response.data
          }
        })
        .catch(error => {
          console.log(error)
          this.error = error
        })
        .finally(() => { this.loading = false })
    },
    toggleEdit () {
      this.$router.go(-1)
    }
  },
  mounted () {
    this.fetchInfo()
  }
}
</script>

<style lang="css">
</style>
