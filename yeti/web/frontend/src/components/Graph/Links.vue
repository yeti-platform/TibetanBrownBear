<template>
  <div class="links">
    <div v-if="loading">
      <i class='fas fa-circle-notch fa-spin fa-3x m-3'></i>
    </div>
    <table v-else class="table table-sm">
      <tr v-for="edge in graph.edges"
          v-bind:key='edge._id'>
        <td class="incoming-vertice">
          <router-link :to="{ name: detailComponent, params: {id: getIncomingVertice(graph, edge).id}}">
            <type-to-icon :type="getIncomingVertice(graph, edge).type"></type-to-icon>{{getIncomingVertice(graph, edge).name}}
          </router-link>
          </td>
        <td>&rarr;</td>
        <td>{{edge.relationship_type}}</td>
        <td>&rarr;</td>
        <td class="outgoing-vertice">
          <router-link :to="{ name: '', params: {id: getOutgoingVertice(graph, edge).id} }">
            <type-to-icon :type="getOutgoingVertice(graph, edge).type"></type-to-icon>{{getOutgoingVertice(graph, edge).name}}
          </router-link>
        </td>
        <td><markdown-text :text="edge.description || 'No description'"></markdown-text></td>
        <td>
          <p v-for="ref in edge.external_references" v-bind:key="ref.source_name">
              <a :href="ref.url" target="_blank">{{ref.source_name}}</a>
              <small v-if="ref.description"><br>{{ref.description}}</small>
              <small v-if="ref.external_id"><br>{{ref.external_id}}</small>
          </p>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
import TableFilter from '@/components/scaffolding/TableFilter'
import TypeToIcon from '@/components/scaffolding/TypeToIcon'
import MarkdownText from '@/components/scaffolding/MarkdownText'

export default {
  components: {
    TableFilter,
    TypeToIcon,
    MarkdownText
  },
  props: ['object', 'detailComponent'],
  data () {
    return {
      graph: [],
      loading: true
    }
  },
  computed: {
    apiPath () {
      return 'http://localhost:5000/api/entities/' + this.object.id + '/neighbors'
    }
  },
  methods: {
    fetchNeighbors () {
      this.loading = true
      console.log('fetching neighbors for ' + this.object.id)
      axios.get(this.apiPath)
        .then(response => {
          console.log('Got ' + response.data.edges.length + ' edges')
          this.graph = response.data
          this.loading = false
        })
    },
    getVerticeForEdge (graph, edge) {
      if (edge.source_ref === this.object.id) {
        return graph.vertices[edge.target_ref]
      }
      return graph.vertices[edge.source_ref]
    },
    getIncomingVertice (graph, edge) {
      if (edge.target_ref === this.object.id) {
        return graph.vertices[edge.source_ref]
      }
      return this.object
    },
    getOutgoingVertice (graph, edge) {
      if (edge.source_ref === this.object.id) {
        return graph.vertices[edge.target_ref]
      }
      return this.object
    }
  },
  watch: {
    object: 'fetchNeighbors'
  },
  mounted () {
    this.fetchNeighbors()
  }
}
</script>

<style lang="css">
  .links .outgoing-vertice, .links .incoming-vertice {
    white-space: nowrap;
  }
</style>
