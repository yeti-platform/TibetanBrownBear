<template lang="html">
  <i :class="'fas fa-fw fa-lg ' + icon"></i>
</template>

<script>

const typeToIcon = {
  'malware': 'fa-bug',
  'threat-actor': 'fa-user-secret',
  'attack-pattern': 'fa-gamepad',
  'tool': 'fa-wrench',
  'intrusion-set': 'fa-umbrella',
  'vulnerability': 'fa-bolt',
  'campaign': 'fa-fighter-jet',
  'course-of-action': 'fa-medkit',
  'identity': 'fa-id-card'
}

export default {
  props: ['type'],
  computed: {
    icon () {
      return typeToIcon[this.type]
    }
  }
}
</script>

<style lang="css">
</style>
