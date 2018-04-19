<template lang="html">
  <!-- display tags -->
  <div v-if="field === 'tags'">
    <span v-for="tag in value"
          v-bind:key="tag.name"
          class="badge m-1"
          v-bind:class="{'badge-secondary': !tag.fresh, 'badge-primary': tag.fresh}">
      {{tag.name}}
    </span>
  </div>

  <!-- display generic arrays as a list of tags -->
  <div v-else-if="value instanceof Array">
    <span v-for="v in value"
          v-bind:key="v"
          class="badge m-1 badge-primary">
      {{v}}
    </span>
  </div>

  <div v-else-if="checkValidDate(value)">
    <span>{{ formatDateString(value) }}</span>
  </div>

  <!-- fall back to displaying a normal value -->
  <span v-else>{{value}}</span>
</template>

<script>
import moment from 'moment'

// Expected input format: 2018-04-16T16:18:25.179482+00:00
const inputDateTimeFormat = 'YYYY-MM-DDTHH:mm:ss.SSSSSSZZ'
// Wanted output format: 2018-04-16 16:18:25 +02:00 (to localtime)
const outputDateTimeFormat = 'YYYY-MM-DD HH:mm:ss ZZ'

export default {
  props: [
    'field',
    'value'
  ],
  methods: {
    checkValidDate (string) {
      return moment(string, inputDateTimeFormat, true).isValid()
    },
    formatDateString (string) {
      return moment(string, inputDateTimeFormat).format(outputDateTimeFormat)
    }
  }
}
</script>

<style lang="css">
</style>
