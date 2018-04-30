<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">Entities</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <button v-if="subType" class="btn btn-sm btn-outline-secondary" @click="() => {newEntity = !newEntity}">
            {{newEntity ? "Cancel" : "New " + subType}}
          </button>
        </div>
      </div>
    </div>
    <nav class="nav nav-pills flex-column flex-sm-row">
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/entities/malware">Malware</router-link>
      <router-link class="flex-sm-fill text-sm-center nav-link" to="/entities/actor">Actors</router-link>
    </nav>
    <router-view />
    <table-filter v-if="!newEntity && subType" :filter-params="filterParams" detailComponent="EntityDetails"/>
    <yeti-form v-if="newEntity"
               apiPath="http://localhost:5000/api/entities/"
               :object="defaultObject"
               :fields="subTypeFields"
               :onSaveCallback='navigateToNew'/>
  </div>
</template>

<script>
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

const typeFields = {
  'malware': [
    {name: 'name', type: 'text'},
    {name: 'family', type: 'list'}
  ],
  'actor': [
    {name: 'name', type: 'text'}
  ]
}

export default {
  components: {
    TableFilter,
    YetiForm
  },
  data () {
    return {
      newEntity: false,
      defaultObjects: {
        'malware': {
          type: 'entity.malware',
          family: []
        },
        'actor': {
          type: 'entity.actor'
        }
      }
    }
  },
  computed: {
    subType () {
      return this.$route.params.type
    },
    subTypeFields () {
      return typeFields[this.subType]
    },
    filterParams () {
      let type = this.$route.params.type
      return {
        apiPath: `http://localhost:5000/api/entities/filter/`,
        fields: typeFields[type],
        querykey: 'name',
        typeFilter: type
      }
    },
    defaultObject () {
      return this.defaultObjects[this.subType]
    }
  },
  methods: {
    navigateToNew (object) {
      this.$router.push({name: 'EntityDetails', params: {id: object.data.id}})
    }
  }
}
</script>
