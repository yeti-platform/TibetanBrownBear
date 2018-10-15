<template lang="html">
  <i :class="classArray"></i>
</template>

<script>

const typeToIcon = {
  'malware': 'fa-bug',
  'threat-actor': 'fa-user-secret',
  'attack-pattern': 'fa-gamepad',
  'tool': 'fa-wrench',
  'intrusion-set': 'fa-umbrella',
  'indicator': 'fa-bolt',
  'x-regex': 'fa-bolt',
  'x-yara': 'fa-bolt',
  'vulnerability': 'fa-bolt',
  'campaign': 'fa-fighter-jet',
  'course-of-action': 'fa-medkit',
  'identity': 'fa-id-card'
}

export default {
  props: ['type', 'large'],
  data () {
    return {
      typeToIcon: typeToIcon
    }
  },
  computed: {
    classArray () {
      return ['fas', 'fa-fw', typeToIcon[this.type], {'fa-lg': this.large}]
    }
  }
}
</script>

<style lang="css">
</style>
