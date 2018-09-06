<template>
  <!-- Display details nicely -->
  <span v-if="loading" class="loading">
    <i class="fas fa-circle-notch fa-spin fa-5x m-5"></i>
  </span>
  <div v-else-if="!edit" class="entity-details">

    <!-- Title and edit button -->
    <div class="title border-bottom mb-4 pb-2">
      <div class="entity-type">
        {{entityTypeHuman.singular}}
      </div>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center">
        <h1 class="h1 yeti-title">{{entity.name}}</h1>
        <div class="btn-toolbar mb-2 mb-md-0">
          <div class="btn-group mr-2">
            <router-link class="edit btn btn-sm btn-outline-secondary" :to="{name: 'EntityEdit', params: {id: id}}">Edit</router-link>
          </div>
        </div>
      </div>
      <div class="labels">
        <fields :field="{'type': 'list', 'name': 'labels'}"  :elt="entity" />
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

        <table class="table">
          <tr>
            <th>Created:</th><td><fields :field="{'type': 'datetime', 'name': 'created'}" :elt="entity" /></td>
            <th>Modified:</th><td><fields :field="{'type': 'datetime', 'name': 'modified'}" :elt="entity" /></td>
          </tr>
          <tr v-if="entity.tool_version">
            <th>Tool version</th><td>{{entity.tool_version}}</td>
          </tr>
          <tr v-if="entity.action">
            <th>Action</th><td>{{entity.action}}</td>
          </tr>
          <tr v-if="entity.identity_class">
            <th>Identity class</th><td colspan="5">{{entity.identity_class}}</td>
          </tr>
          <tr v-if="entity.sectors">
            <th>Sectors</th><td colspan="5"><fields :field="{'type': 'list', 'name': 'sectors'}" :elt="entity" /></td>
          </tr>
          <tr v-if="entity.contact_information">
            <th>Contact info</th><td colspan="5">{{entity.contact_information}}</td>
          </tr>
          <tr v-if="entity.aliases">
            <th>Aliases</th><td colspan="5"><fields :field="{'type': 'list', 'name': 'aliases'}" :elt="entity" /></td>
          </tr>
          <tr v-if="entity.kill_chain_phases">
            <th>Kill-chain phases</th>
            <td colspan="5"><fields :field="{'type': 'killchain', 'name': 'kill_chain_phases'}" :elt="entity" /></td>
          </tr>
          <tr v-if="entity.first_seen || entity.last_seen">
            <th>First seen:</th><td><fields :field="{'type': 'datetime', 'name': 'first_seen'}" :elt="entity" /></td>
            <th>Last seen:</th><td><fields :field="{'type': 'datetime', 'name': 'last_Seen'}" :elt="entity" /></td>
          </tr>
          <tr v-if="entity.objective">
            <th>Objective</th><td colspan="5">{{entity.objective}}</td>
          </tr>
          <tr v-if="entity.roles || entity.sophistication">
            <th>Roles</th><td><fields :field="{'type': 'list', 'name': 'roles'}" :elt="entity" /></td>
            <th>Sophistication</th><td>{{entity.sophistication}}</td>
          </tr>
          <tr v-if="entity.goals || entity.resource_level">
            <th>Goals</th><td><fields :field="{'type': 'list', 'name': 'goals'}" :elt="entity" /></td>
            <th>Resource level</th><td>{{entity.resource_level}}</td>
          </tr>
          <tr v-if="entity.primary_motivation || entity.secondary_motivations || entity.personal_motivations">
            <th>Primary motivation</th><td>{{entity.primary_motivation}}</td>
            <th>Secondary</th><td><fields :field="{'type': 'list', 'name': 'secondary_motivations'}" :elt="entity" /></td>
            <th>Personal</th><td><fields :field="{'type': 'list', 'name': 'personal_motivations'}" :elt="entity" /></td>
          </tr>
        </table>

        <div class="description mb-3">
          <h2>Description</h2>
          <markdown-text :text="entity.description || 'No description'"></markdown-text>
        </div>
      </div>

      <!-- Detailed information -->
      <div class="tab-pane" id="details" role="tabpanel" aria-labelledby="details-tab">
        <div class="details mb-3">
          <h2>Details</h2>
          <table class='table'>
            <tr><td>Type</td><td><fields :field="{'type': 'code', 'name': 'type'}" :elt="entity" /></td></tr>
            <tr><td>STIX ID</td><td><fields :field="{'type': 'code', 'name': 'id'}" :elt="entity" /></td></tr>
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
        <div v-if="getSpecificProperties(entity).length > 0">
          <h2>{{entityTypeHuman.singular}} specific properties</h2>
          <table class="table">
            <tr v-for="prop in getSpecificProperties(entity)" v-bind:key="prop.name">
              <td><code>{{prop.name}}</code></td><td>{{prop.value}}</td>
            </tr>
          </table>
        </div>
        <div v-if="getExtendedProperties(entity).length > 0">
          <h2>Extended properties</h2>
          <table class="table">
            <tr v-for="prop in getExtendedProperties(entity)" v-bind:key="prop.name">
              <td><code>{{prop.name}}</code></td><td>{{prop.value}}</td>
            </tr>
          </table>
        </div>

        </div>
      </div>

      <!-- Links and graph -->
      <div class="tab-pane" id="relationships" role="tabpanel" aria-labelledby="relationships-tab">
        <div class="relationships">
          <h2>Relationships</h2>
          <links :object="entity" :detailComponent="'EntityDetails'"/>
        </div>
      </div>

      <!-- JSON -->
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

import YetiForm from '@/components/scaffolding/YetiForm'
import MarkdownText from '@/components/scaffolding/MarkdownText'
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
    Links,
    MarkdownText
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
      this.loading = true
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
    getSpecificProperties (entity) {
      var properties = []
      for (var prop in entity) {
        if (this.isSpecifcAttribute(entity, prop)) {
          properties.push({value: entity[prop], name: prop})
        }
      }
      return properties
    },
    getExtendedProperties (entity) {
      var properties = []
      for (var prop in entity) {
        if (this.isExtendedAttribute(entity, prop)) {
          properties.push({value: entity[prop], name: prop})
        }
      }
      return properties
    },
    isSpecifcAttribute (entity, attribute) {
      let commonProperties = [
        'created',
        'type',
        'id',
        'created_by_ref',
        'created',
        'modified',
        'revoked',
        'external_references',
        'object_marking_refs',
        'granular_markings',
        'description',
        'labels',
        'name'
      ]
      return entity.hasOwnProperty(attribute) && !commonProperties.includes(attribute) && !attribute.startsWith('x_')
    },
    isExtendedAttribute (entity, attribute) {
      return entity.hasOwnProperty(attribute) && attribute.startsWith('x_')
    }
  },
  mounted () {
    this.fetchInfo()
  },
  watch: {
    // call again the method if the route changes
    'id': 'fetchInfo'
  }
}
</script>
