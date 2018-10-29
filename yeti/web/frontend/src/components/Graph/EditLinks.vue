<template>
  <div class="new-link mb-2 mr-2 float-left">
    <a v-if="selectedLinks.length == 1" href="#" class="btn btn-light" data-toggle="modal" data-target="#relationshipModal">Edit link</a>
    <a v-if="selectedLinks.length > 1" href="#" class="btn btn-light" data-toggle="modal" data-target="#relationshipModal">Edit {{ selectedLinks.length }} links</a>
    <div class="modal" id="relationshipModal" tabindex="-1" role="dialog" aria-labelledby="relationshipModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title" id="relationshipModalLabel">Edit links</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <div class="modal-body">
            <yeti-form-field v-model="newRelationship.relationship_type" :field="{'name': 'relationship_type', 'type': 'text', humanName: 'Relationship type'}">
            </yeti-form-field>
            <yeti-form-field v-model="newRelationship.description" :field="{'name': 'description', 'type': 'longtext', humanName: 'Description'}">
            </yeti-form-field>
          </div>

          <div class="modal-footer">
            <small>This action will affect {{ selectedLinks.length }} selected links.</small>
            <button type="button" ref="modalClose" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="saveLinkData" v-bind:class="{ disabled: saving }">{{saving ? "Saving..." : "Save changes"}}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import YetiForm from '@/components/scaffolding/YetiForm'
import YetiFormField from '@/components/scaffolding/YetiFormField'

export default {
  components: {
    YetiForm,
    YetiFormField
  },
  props: ['selectedLinks'],
  data () {
    return {
      newRelationship: {},
      saving: false
    }
  },
  methods: {
    fetchLinkData (linkId) {
      var linkID = this.selectedLinks[0]
      axios.get('/relationships/' + linkID + '/')
        .then(response => {
          if (response.status === 200) {
            this.newRelationship = response.data
          }
        })
    },
    saveLinkData () {
      this.saving = true
      for (var index = 0; index < this.selectedLinks.length; index++) {
        var lastIndex = index
        var linkID = this.selectedLinks[index]
        let linkData = {
          'description': this.newRelationship.description,
          'relationship_type': this.newRelationship.relationship_type
        }
        axios.put('/relationships/' + linkID + '/', linkData)
          .then(response => {
            if (lastIndex === this.selectedLinks.length - 1) {
              this.saving = false
              this.$refs.modalClose.click()
              this.$emit('links-changed', response.data)
            }
          })
      }
    }
  },
  watch: {
    'selectedLinks': function () {
      if (this.selectedLinks.length > 0) {
        this.fetchLinkData()
      }
    }
  }
}
</script>

<style>

</style>
