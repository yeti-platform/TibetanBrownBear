<template>
  <div class="links">
    <new-link ref="newLink" :sourceEntity="object" v-on:links-changed='fetchNeighbors'></new-link>
    <delete-links ref="deleteLinks"
                  v-if="selectedLinks.length >= 1"
                  :selectedLinks="selectedLinks"
                  v-on:links-deleted='fetchNeighbors'>
    </delete-links>
    <edit-links :selectedLinks="selectedLinks" v-on:links-changed='fetchNeighbors'></edit-links>
    <span v-if="loading">
      <i class='fas fa-circle-notch fa-spin fa-3x m-3'></i>
    </span>
    <table v-else class="table table-sm">
      <tr v-for="edge in graph.edges"
          v-bind:key='edge._id'
          @click.exact="select(edge)"
          @click.shift.exact="selectMultiple(edge)"
          v-bind:class="{'selected': selectedLinks.includes(edge.id)}"
          class="show-on-hover"
        >
        <td class="show-on-hover"><a href="#" @click="$refs.deleteLinks.deleteLinks([edge.id])"><i class="fas fa-unlink"></i></a></td>
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
import NewLink from '@/components/Graph/NewLink'
import DeleteLinks from '@/components/Graph/DeleteLinks'
import EditLinks from '@/components/Graph/EditLinks'

export default {
  components: {
    TableFilter,
    TypeToIcon,
    MarkdownText,
    NewLink,
    DeleteLinks,
    EditLinks
  },
  props: ['object', 'detailComponent'],
  data () {
    return {
      graph: [],
      loading: true,
      selectedLinks: []
    }
  },
  computed: {
    apiPath () {
      return 'entities/' + this.object.id + '/neighbors/'
    }
  },
  methods: {
    fetchNeighbors () {
      console.log('fetching neighbors for ' + this.object.id)
      this.loading = true
      axios.get(this.apiPath)
        .then(response => {
          console.log('Got ' + response.data.edges.length + ' edges')
          this.graph = response.data
          this.selectedLinks = []
        })
        .finally(() => { this.loading = false })
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
    },
    select (elt) {
      this.selectedLinks = [elt.id]
      this.$emit('input', [elt])
    },
    selectMultiple (elt) {
      if (!this.selectedLinks.includes(elt.id)) {
        this.selectedLinks.push(elt.id)
      } else {
        this.selectedLinks.splice(this.selectedLinks.indexOf(elt.id), 1)
      }
      this.$emit('input', this.graph.edges.filter(elt => this.selectedLinks.includes(elt.id)))
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

.selected {
  background-color: #ffffe4;
}

td.show-on-hover {
  opacity: 0;
}

tr.show-on-hover:hover .show-on-hover {
  opacity: 1;
}

.links .outgoing-vertice, .links .incoming-vertice {
  white-space: nowrap;
}
</style>
