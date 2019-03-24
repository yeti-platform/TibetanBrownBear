<template>
  <div>
    <div class="form-group">
      <label :for="slug">{{field.humanName}}</label>

      <!-- plain text input -->
      <yeti-text-input v-if="field.type === 'text'" v-model="bufferValue"
          :vocab="field.vocab"
          :id="slug"/>

      <!-- code input -->
      <textarea v-if="field.type === 'code'" v-model="bufferValue"
          class="form-control code"
          :id="slug"
          rows="8" cols="80" ></textarea>

      <!-- textarea -->
      <textarea v-if="field.type === 'longtext'" v-model="bufferValue"
          class="form-control"
          :id="slug"
          rows="8" cols="80" ></textarea>

      <!-- datetime -->
      <datepicker v-if="field.type === 'datetime'" :id="slug" v-model="bufferValue"
          :format="customFormatter"
          :bootstrap-styling="true"
          :typeable="true"
          placeholder="Click to pick date">
      </datepicker>

      <!-- list-type input -->
      <yeti-vocab-input v-if="field.type === 'list'" v-model="bufferValue"
          :autocompleteVocab="field['vocab']" />

      <!-- tag input -->
      <yeti-vocab-input v-if="field.type === 'tags'" v-model="bufferValue"
          displayKey="name"
          :autocompleteVocab="field['vocab']" />

      <!-- killchain input -->
      <div v-if="field.type === 'killchain'">
        <yeti-killchain-input v-model="bufferValue"
          v-for="killchain in availableKillchains" v-bind:key="killchain.name"
          :killchainName="killchain.name"
          class="mb-2"/>
      </div>

      <small v-if="field.help" :id="slug+'-help'" class="form-text text-muted">{{field.help}}</small>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import YetiVocabInput from '@/components/scaffolding/YetiVocabInput'
import YetiTextInput from '@/components/scaffolding/YetiTextInput'
import YetiKillchainInput from '@/components/scaffolding/YetiKillchainInput'
import Datepicker from 'vuejs-datepicker'

export default {
  components: {
    YetiVocabInput,
    YetiTextInput,
    YetiKillchainInput,
    Datepicker
  },
  data () {
    return {
      bufferValue: null,
      availableKillchains: []
    }
  },
  props: ['field', 'value'],
  methods: {
    valueUpdated () {
      this.$emit('input', this.bufferValue)
    },
    fetchKillchains () {
      axios.get('/settings/killchains/')
        .then(response => {
          this.availableKillchains = response.data
        })
    }
  },
  computed: {
    slug () {
      return this.field.name.toLowerCase().replace(/[\s_]+|[^\w-]|^-+|-+$/g, '')
    }
  },
  mounted () {
    this.bufferValue = this.value
    this.fetchKillchains()
  },
  watch: {
    'bufferValue': 'valueUpdated',
    'value': function (val) {
      this.bufferValue = val
    }
  }
}
</script>

<style>

</style>
