<template>
  <div>
    <div class="row">
      <div id="tag-list" class="col-12">
        <p>Click on a line in the table to manipulate Async Jobs.</p>
        <table-filter ref="asyncList"
                      :filter-params="filterParams"
                      :multiSelect="false"
                      v-on:toggle="toggle"
                      v-on:execute="execute" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import TableFilter from '@/components/scaffolding/TableFilter'

const apiRoot = `http://localhost:5000/api/async/`

export default {
  components: {
    TableFilter
  },
  data () {
    return {
      filterParams: {
        apiPath: apiRoot + 'filter',
        fields: [
          {name: 'name', type: 'text'},
          {name: 'last_executed', type: 'datetime'},
          {name: 'period', type: 'text'},
          {name: 'enabled', type: 'text'},
          {name: 'status', type: 'text'},
          {calls: this.toggle, type: 'action', label: 'Toggle'},
          {calls: this.execute, type: 'action', label: 'Execute'}
        ],
        queryKey: 'name'
      },
      defaultApiPath: apiRoot
    }
  },
  methods: {
    toggle (data) {
      console.log('caught toggle')
      let uri = apiRoot + data.name + '/toggle'
      axios.post(uri).then(response => {
        if (response.status === 200) {
          data.enabled = response.data.enabled
        }
      })
    },
    execute (data) {
      console.log('caught execute')
      let uri = apiRoot + data.name + '/execute'
      axios.post(uri).then(response => {
        if (response.status === 200) {
          console.log(response.data.status)
          console.log(data)
          data.status = response.data.status
        }
      })
    }
  }
}
</script>

<style lang="css">
</style>
