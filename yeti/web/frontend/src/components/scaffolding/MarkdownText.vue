<template>
  <div v-html="compiledMarkdown || 'N/A' "></div>
</template>

<script>
import marked from 'marked'

export default {
  props: ['text'],
  computed: {
    compiledMarkdown () {
      return marked(this.text || '', {
        breaks: true,
        sanitize: false
      })
    }
  }
}
</script>
