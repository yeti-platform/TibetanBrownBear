<template>
  <!-- Display details nicely -->
  <div v-if="!isEdit" class="entity-details">
    <div class="loading" v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{entity.name}} <small>{{entity.type}}</small></h3>
      <fields :field="{'type': 'list', 'name': 'family'}"  :elt="entity" />
      {{entity.description || 'No description'}}
    </div>
    <router-link class="edit btn btn-sm btn-outline-secondary" :to="{name: 'EntityEdit', params: {id: id}}">Edit</router-link>
  </div>

  <!--  Edit form -->
  <!-- yeti-form should use emit instead of an onSaveCallback -->
  <yeti-form :object="entity"
             :fields="entityFields"
             :apiPath="defaultApiPath+id+'/'"
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
  props: ['id'],
  components: {
    YetiForm,
    Fields
  },
  beforeRouteUpdate (to, from, next) { // how do we test this?
    this.fetchInfo()
    next()
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
      axios.get(this.defaultApiPath + this.id)
        .then(response => {
          if (response.status !== 200) {
            this.error = response.data
          } else {
            this.entity = response.data
          }
        })
        .catch(error => { // how do we catch 404 errors?
          this.error = error
        })
        .finally(() => { this.loading = false })
    },
    toggleEdit () {
      this.$router.go(-1)
    }
  },
  mounted () { // how to we test for mounted?
    this.fetchInfo()
  }
}
</script>

<style lang="css">
</style>
