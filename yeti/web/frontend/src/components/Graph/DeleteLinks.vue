<template>
  <div class="delete-link mb-2 mr-2 float-left">
    <a v-if="selectedLinks.length == 1" href="#" class="btn btn-light" @click="deleteLinks(selectedLinks)">Delete link</a>
    <a v-if="selectedLinks.length > 1" href="#" class="btn btn-light" @click="deleteLinks(selectedLinks)">Delete {{ selectedLinks.length }} links</a>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['selectedLinks'],
  methods: {
    deleteLinks: function (links) {
      if (!confirm('Are you sure?')) {
        return
      }
      axios.post('/relationships/delete/', links)
        .then(response => {
          this.$emit('links-deleted', links)
        })
    }
  }
}
</script>

<style>

</style>
