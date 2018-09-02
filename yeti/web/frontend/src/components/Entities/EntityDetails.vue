<template>
  <!-- Display details nicely -->
  <div v-if="!edit && !loading" class="entity-details">

    <!-- Title and edit button -->
    <div class="entity-type">
      {{entityTypeHuman.singular}}
    </div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h1">{{entity.name}}</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <router-link class="edit btn btn-sm btn-outline-secondary" :to="{name: 'EntityEdit', params: {id: id}}">Edit</router-link>
        </div>
      </div>
    </div>

    <ul class="nav nav-pills mb-3" id="myTab" role="tablist">
      <li class="nav-item">
        <a class="nav-link active" id="main-tab" data-toggle="tab" href="#main" role="tab" aria-controls="main" aria-selected="true">Main</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="details-tab" data-toggle="tab" href="#details" role="tab" aria-controls="details" aria-selected="false">Details</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="relationships-tab" data-toggle="tab" href="#relationships" role="tab" aria-controls="relationships" aria-selected="false">Relationships</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="json-tab" data-toggle="tab" href="#json" role="tab" aria-controls="json" aria-selected="false">Raw JSON</a>
      </li>
    </ul>

    <div class="tab-content">

      <!-- Labels and other common info -->
      <div class="tab-pane show active" id="main" role="tabpanel" aria-labelledby="main-tab">
        <div class="labels mb-3">
          <h5><fields :field="{'type': 'list', 'name': 'labels'}"  :elt="entity" /></h5>
        </div>
        <div class="description mb-3">
          <h2>Description</h2>
          <div v-html="compiledMarkdown(entity.description) || 'No description' "></div>
        </div>
      </div>

      <!-- Detailed information -->
      <div class="tab-pane" id="details" role="tabpanel" aria-labelledby="details-tab">
        <div class="details mb-3">
          <h2>Details</h2>
          <table class='table table-compact'>
            <tr><td>Type</td><td><fields :field="{'type': 'code', 'name': 'type'}"  :elt="entity" /></td></tr>
            <tr><td>STIX ID</td><td><fields :field="{'type': 'code', 'name': 'id'}"  :elt="entity" /></td></tr>
            <tr><td>Created by</td><td><fields :field="{'type': 'code', 'name': 'created_by_ref'}"  :elt="entity" /></td></tr>
            <tr><td>Created</td><td><fields :field="{'type': 'datetime', 'name': 'created'}"  :elt="entity" /></td></tr>
            <tr><td>Modified</td><td><fields :field="{'type': 'datetime', 'name': 'modified'}"  :elt="entity" /></td></tr>
            <tr><td>Revoked</td><td><fields :field="{'type': 'boolean', 'name': 'revoked'}"  :elt="entity" /></td></tr>
            <tr v-for="ref in entity.external_references" v-bind:key="ref.source_name">
              <td>External reference</td><td>
                <a :href="ref.url" target="_blank">{{ref.source_name}}</a>
                <small v-if="ref.description"><br>{{ref.description}}</small>
                <small v-if="ref.external_id"><br>{{ref.external_id}}</small>
              </td>
            </tr>
            <tr><td>Object markings</td><td><code v-bind:key="ref" v-for="ref in entity.object_marking_refs">{{ref}}</code></td></tr>
            <tr><td>Granular markings</td><td><code v-bind:key="marking" v-for="marking in entity.granular_markings">{{marking}}</code></td></tr>
          </table>
        </div>
      </div>

      <!-- Links and graph -->
      <div class="tab-pane" id="relationships" role="tabpanel" aria-labelledby="relationships-tab">
        <div class="relationships">
          <h2>Relationships</h2>
          <links :object="entity"/>
        </div>
      </div>

      <div class="tab-pane" id="json" role="tabpanel" aria-labelledby="json-tab">
        <div class="json">
          <pre>{{entity}}</pre>
        </div>
      </div>


    <!-- End tab content -->
    </div>

  </div>

  <!--  Edit form -->
  <!-- yeti-form should use emit instead of an onSaveCallback -->
  <yeti-form :object="entity"
             :fields="entityFields"
             :apiPath="defaultApiPath+id+'/'"
             method='PUT'
             v-on:form-submit='toggleEdit'
             v-else
             />
</template>

<style lang="css">
  .json pre {
    white-space: pre-wrap;
  }

</style>

<script>
import axios from 'axios'
import marked from 'marked'

import YetiForm from '@/components/scaffolding/YetiForm'
import Links from '@/components/Graph/Links'
import Fields from '@/components/helpers/Fields'

import { typeFields } from './EntityFields.js'
import { entityTypes } from './EntityTypes.js'

export default {
  data () {
    return {
      loading: true,
      entity: {},
      error: {},
      defaultApiPath: `http://localhost:5000/api/entities/`
    }
  },
  props: { id: [Number, String], edit: Boolean },
  components: {
    YetiForm,
    Fields,
    Links
  },
  beforeRouteUpdate (to, from, next) { // how do we test this?
    this.fetchInfo()
    next()
  },
  computed: {
    entityType () {
      if (this.entity.type) {
        let arr = this.entity.type.split('.')
        return arr[arr.length - 1]
      }
    },
    entityFields () {
      return typeFields[this.entityType]
    },
    entityTypeHuman () {
      return entityTypes[this.entityType]
    }
  },
  methods: {
    fetchInfo () {
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
    },
    compiledMarkdown (text) {
      return marked(text || '', {
        breaks: true,
        sanitize: false
      })
    }
  },
  mounted () {
    this.fetchInfo()
  }
}
</script>
