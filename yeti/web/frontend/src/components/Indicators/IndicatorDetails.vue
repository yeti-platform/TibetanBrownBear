<template>
  <!-- Display details nicely -->
  <span v-if="loading" class="loading">
    <i class="fas fa-circle-notch fa-spin fa-5x m-5"></i>
  </span>
  <div v-else-if="!edit" class="indicator-details">

    <!-- Title and edit button -->
    <div class="title border-bottom mb-4 pb-2">
      <div class="indicator-type">
        {{indicatorTypeHuman.singular}}
      </div>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center">
        <h1 class="h1 yeti-title">{{indicator.name}}</h1>
        <div class="btn-toolbar mb-2 mb-md-0">
          <div class="btn-group mr-2">
            <router-link class="edit btn btn-sm btn-outline-secondary" :to="{name: 'IndicatorEdit', params: {id: id}}">Edit</router-link>
          </div>
        </div>
      </div>
      <div class="labels">
        <fields :field="{'type': 'list', 'name': 'labels'}"  :elt="indicator" />
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
            <th>Created:</th><td><fields :field="{'type': 'datetime', 'name': 'created'}" :elt="indicator" /></td>
            <th>Modified:</th><td><fields :field="{'type': 'datetime', 'name': 'modified'}" :elt="indicator" /></td>
          </tr>
          <tr v-if="indicator.tool_version">
            <th>Tool version</th><td>{{indicator.tool_version}}</td>
          </tr>
          <tr v-if="indicator.action">
            <th>Action</th><td>{{indicator.action}}</td>
          </tr>
          <tr v-if="indicator.idindicator_class">
            <th>Idindicator class</th><td colspan="5">{{indicator.idindicator_class}}</td>
          </tr>
          <tr v-if="indicator.sectors">
            <th>Sectors</th><td colspan="5"><fields :field="{'type': 'list', 'name': 'sectors'}" :elt="indicator" /></td>
          </tr>
          <tr v-if="indicator.contact_information">
            <th>Contact info</th><td colspan="5">{{indicator.contact_information}}</td>
          </tr>
          <tr v-if="indicator.aliases">
            <th>Aliases</th><td colspan="5"><fields :field="{'type': 'list', 'name': 'aliases'}" :elt="indicator" /></td>
          </tr>
          <tr v-if="indicator.kill_chain_phases">
            <th>Kill-chain phases</th>
            <td colspan="5"><fields :field="{'type': 'killchain', 'name': 'kill_chain_phases'}" :elt="indicator" /></td>
          </tr>
          <tr v-if="indicator.first_seen || indicator.last_seen">
            <th>First seen:</th><td><fields :field="{'type': 'datetime', 'name': 'first_seen'}" :elt="indicator" /></td>
            <th>Last seen:</th><td><fields :field="{'type': 'datetime', 'name': 'last_Seen'}" :elt="indicator" /></td>
          </tr>
          <tr v-if="indicator.objective">
            <th>Objective</th><td colspan="5">{{indicator.objective}}</td>
          </tr>
          <tr v-if="indicator.roles || indicator.sophistication">
            <th>Roles</th><td><fields :field="{'type': 'list', 'name': 'roles'}" :elt="indicator" /></td>
            <th>Sophistication</th><td>{{indicator.sophistication}}</td>
          </tr>
          <tr v-if="indicator.goals || indicator.resource_level">
            <th>Goals</th><td><fields :field="{'type': 'list', 'name': 'goals'}" :elt="indicator" /></td>
            <th>Resource level</th><td>{{indicator.resource_level}}</td>
          </tr>
          <tr v-if="indicator.primary_motivation || indicator.secondary_motivations || indicator.personal_motivations">
            <th>Primary motivation</th><td>{{indicator.primary_motivation}}</td>
            <th>Secondary</th><td><fields :field="{'type': 'list', 'name': 'secondary_motivations'}" :elt="indicator" /></td>
            <th>Personal</th><td><fields :field="{'type': 'list', 'name': 'personal_motivations'}" :elt="indicator" /></td>
          </tr>
        </table>

        <div class="description mb-3">
          <h2>Description</h2>
          <markdown-text :text="indicator.description || 'No description'"></markdown-text>
        </div>

         <div class="pattern mb-3">
          <h2>Pattern</h2>
          <fields :field="{'type': 'code', 'name': 'pattern'}" :elt="indicator"></fields>
        </div>

      </div>

      <!-- Detailed information -->
      <div class="tab-pane" id="details" role="tabpanel" aria-labelledby="details-tab">
        <div class="details mb-3">
          <h2>Details</h2>
          <table class='table'>
            <tr><td>Type</td><td><fields :field="{'type': 'code', 'name': 'type'}" :elt="indicator" /></td></tr>
            <tr><td>STIX ID</td><td><fields :field="{'type': 'code', 'name': 'id'}" :elt="indicator" /></td></tr>
            <tr><td>Created by</td><td><fields :field="{'type': 'code', 'name': 'created_by_ref'}"  :elt="indicator" /></td></tr>
            <tr><td>Created</td><td><fields :field="{'type': 'datetime', 'name': 'created'}"  :elt="indicator" /></td></tr>
            <tr><td>Modified</td><td><fields :field="{'type': 'datetime', 'name': 'modified'}"  :elt="indicator" /></td></tr>
            <tr><td>Revoked</td><td><fields :field="{'type': 'boolean', 'name': 'revoked'}"  :elt="indicator" /></td></tr>
            <tr v-for="ref in indicator.external_references" v-bind:key="ref.source_name">
              <td>External reference</td><td>
                <a :href="ref.url" target="_blank">{{ref.source_name}}</a>
                <small v-if="ref.description"><br>{{ref.description}}</small>
                <small v-if="ref.external_id"><br>{{ref.external_id}}</small>
              </td>
            </tr>
            <tr><td>Object markings</td><td><code v-bind:key="ref" v-for="ref in indicator.object_marking_refs">{{ref}}</code></td></tr>
            <tr><td>Granular markings</td><td><code v-bind:key="marking" v-for="marking in indicator.granular_markings">{{marking}}</code></td></tr>
          </table>
        <div v-if="getSpecificProperties(indicator).length > 0">
          <h2>{{indicatorTypeHuman.singular}} specific properties</h2>
          <table class="table">
            <tr v-for="prop in getSpecificProperties(indicator)" v-bind:key="prop.name">
              <td><code>{{prop.name}}</code></td><td>{{prop.value}}</td>
            </tr>
          </table>
        </div>
        <div v-if="getExtendedProperties(indicator).length > 0">
          <h2>Extended properties</h2>
          <table class="table">
            <tr v-for="prop in getExtendedProperties(indicator)" v-bind:key="prop.name">
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
          <links :object="indicator" :detailComponent="'IndicatorDetails'"/>
        </div>
      </div>

      <!-- JSON -->
      <div class="tab-pane" id="json" role="tabpanel" aria-labelledby="json-tab">
        <div class="json">
          <pre>{{indicator}}</pre>
        </div>
      </div>

    <!-- End tab content -->
    </div>

  </div>

  <!--  Edit form -->
  <!-- yeti-form should use emit instead of an onSaveCallback -->
  <yeti-form :object="indicator"
             :fields="indicatorFields"
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

import { editFields } from './IndicatorFields.js'
import { indicatorTypes } from './IndicatorTypes.js'

export default {
  data () {
    return {
      loading: true,
      indicator: {},
      error: {},
      defaultApiPath: `/indicators/`
    }
  },
  props: { id: [Number, String], edit: Boolean },
  components: {
    YetiForm,
    Fields,
    Links,
    MarkdownText
  },
  computed: {
    indicatorType () {
      if (this.indicator.type) {
        let arr = this.indicator.type.split('.')
        return arr[arr.length - 1]
      }
    },
    indicatorFields () {
      return editFields[this.indicatorType]
    },
    indicatorTypeHuman () {
      return indicatorTypes[this.indicatorType]
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
            this.indicator = response.data
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
    getSpecificProperties (indicator) {
      var properties = []
      for (var prop in indicator) {
        if (this.isSpecifcAttribute(indicator, prop)) {
          properties.push({value: indicator[prop], name: prop})
        }
      }
      return properties
    },
    getExtendedProperties (indicator) {
      var properties = []
      for (var prop in indicator) {
        if (this.isExtendedAttribute(indicator, prop)) {
          properties.push({value: indicator[prop], name: prop})
        }
      }
      return properties
    },
    isSpecifcAttribute (indicator, attribute) {
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
      return indicator.hasOwnProperty(attribute) && !commonProperties.includes(attribute) && !attribute.startsWith('x_')
    },
    isExtendedAttribute (indicator, attribute) {
      return indicator.hasOwnProperty(attribute) && attribute.startsWith('x_')
    }
  },
  mounted () {
    this.fetchInfo()
  },
  watch: {
    // call again the method if the id changes
    'id': 'fetchInfo'
  }
}
</script>
