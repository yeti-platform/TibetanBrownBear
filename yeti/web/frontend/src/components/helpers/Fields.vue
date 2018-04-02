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

  <!-- fall back to displaying a normal value -->
  <span v-else>{{value}}</span>
</template>

<script>
export default {
  props: [
    'field',
    'value'
  ]
}
</script>

<style lang="css">
</style>
