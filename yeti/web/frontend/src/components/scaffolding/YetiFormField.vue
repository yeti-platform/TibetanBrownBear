<template>
  <div>
    <div class="form-group">
      <label :for="field.name">{{field.name}}</label>

      <!-- plain text input -->
      <yeti-text-input v-if="field.type === 'text'" v-model="bufferValue"
          :vocab="field.vocab"
          :id="field['name']"/>

      <!-- code input -->
      <textarea v-if="field.type === 'code'" v-model="bufferValue"
          class="form-control code"
          :id="field['name']"
          rows="8" cols="80" ></textarea>

      <!-- textarea -->
      <textarea v-if="field.type === 'longtext'" v-model="bufferValue"
          class="form-control"
          :id="field['name']"
          rows="8" cols="80" ></textarea>

      <!-- datetime -->
      <datepicker v-if="field.type === 'datetime'" :id="field['name']" v-model="bufferValue"
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
      <yeti-killchain-input v-if="field.type === 'killchain'" v-model="bufferValue" />

      <small v-if="field.help" :id="field['name']+'-help'" class="form-text text-muted">{{field.help}}</small>
    </div>
  </div>
</template>

<script>
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
      bufferValue: null
    }
  },
  props: ['field', 'value'],
  methods: {
    valueUpdated () {
      this.$emit('input', this.bufferValue)
    }
  },
  mounted () {
    console.log('updating buffervalue')
    this.bufferValue = this.value
    console.log(this.bufferValue)
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
