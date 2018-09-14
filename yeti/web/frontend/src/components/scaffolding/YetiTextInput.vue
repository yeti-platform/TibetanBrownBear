<template>
  <div>
    <input @keyup="valueUpdated" class="form-control" v-model="bufferValue">
    <small v-if="vocab" class="form-text text-muted">Suggested values from <code>{{vocab}}</code>: {{fieldVocab.join(', ')}}</small>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['value', 'vocab'],
  data () {
    return {
      fieldVocab: [],
      bufferValue: ''
    }
  },
  methods: {
    getVocabValues () {
      axios.get('/api/settings/vocabs/' + this.vocab + '/').then(response => {
        if (response.status === 200) {
          this.fieldVocab = response.data
        }
      })
    },
    valueUpdated () {
      this.$emit('input', this.bufferValue)
    }
  },
  mounted () {
    this.bufferValue = this.value
    if (this.vocab) {
      this.getVocabValues()
    }
  }
}
</script>

<style>

</style>
