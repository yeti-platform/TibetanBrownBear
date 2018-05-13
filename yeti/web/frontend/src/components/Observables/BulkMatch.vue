<template lang="html">
  <div>
    <form @submit="submitForm">
      <div class="form-group">
          <label for="bulk-search">Input observables, one on each line.</label>
          <textarea v-model="rawInput" class="form-control" id="bulk-search" rows="3"></textarea>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary">Search</button>
      </div>
    </form>
    <pre>{{observables}}</pre>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      observables: [],
      rawInput: '',
      defaultApiPath: `http://localhost:5000/api/observables/match`,
      error: {}
    }
  },
  methods: {
    submitForm: function (e) {
      e.preventDefault()
      this.parseRawInput()
      this.sendMatchQuery()
    },
    parseRawInput: function () {
      this.observables = this.rawInput.split('\n').map(item => item.trim()).filter(item => item.length)
    },
    sendMatchQuery: function () {
      axios.post(this.defaultApiPath, {observables: this.observables})
        .then(response => {
          if (response.status !== 200) {
            this.error = response.data
          } else {
            this.observables = response.data
          }
        })
    }
  }
}
</script>

<style lang="css">
</style>
