<template>
  <div>
    <nav aria-label="Pagination">
      <ul class="pagination justify-content-center">
        <li class="page-item" v-bind:class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" tabindex="-1" @click="currentPage = 1">&laquo;</a>
        </li>
        <li class="page-item" v-bind:class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" tabindex="-1" @click="prevPage">&lsaquo;</a>
        </li>
        <li v-for="pageNumber in dynamicPageButtons" v-bind:key="pageNumber" class="page-item" v-bind:class="{ disabled: currentPage === pageNumber }">
          <a @click="setPage(pageNumber)" class="page-link" href="#" >{{pageNumber}}</a>
        </li>
        <li class="page-item" v-bind:class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click="nextPage">&rsaquo;</a>
        </li>
        <li class="page-item" v-bind:class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" tabindex="-1" @click="currentPage = totalPages" >&raquo;</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  props: [
    'currentPage',
    'totalItems'
  ],
  data () {
    return {
      pageSize: 50,
      maxButtons: 10
    }
  },
  methods: {
    setPage (pageNumber) {
      if (pageNumber >= 1 && pageNumber * this.pageSize <= this.totalItems) {
        this.$emit('page-change', pageNumber)
      }
    },
    nextPage (data) {
      if (this.currentPage * this.pageSize < this.totalItems) {
        this.$emit('page-change', this.currentPage + 1)
      }
    },
    prevPage (data) {
      if (this.currentPage > 1) {
        this.$emit('page-change', this.currentPage - 1)
      }
    }
  },
  computed: {
    totalPages () {
      return Math.ceil(this.totalItems / this.pageSize)
    },
    dynamicPageButtons () {
      return [...Array(this.totalButtons).keys()].map(a => a + this.start)
    },
    delta () {
      return Math.ceil(this.totalButtons / 2)
    },
    start () {
      if (this.totalButtons >= this.totalPages || this.currentPage - this.delta < 1) {
        return 1
      }
      if (this.currentPage + this.delta >= this.totalPages) {
        return this.totalPages - this.totalButtons + 1
      }
      return this.currentPage - this.delta
    },
    totalButtons () {
      if (this.totalPages < this.maxButtons) {
        return this.totalPages
      } else {
        return this.maxButtons
      }
    }
  }
}
</script>

<style>

</style>
