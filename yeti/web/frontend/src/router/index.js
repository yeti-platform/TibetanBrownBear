import Vue from 'vue'
import Router from 'vue-router'

import Observables from '@/components/Observables/Observables'
import ObservableList from '@/components/Observables/ObservableList'
import ObservableDetails from '@/components/Observables/ObservableDetails'
import BulkMatch from '@/components/Observables/BulkMatch'

import Entities from '@/components/Entities/Entities'
import EntityList from '@/components/Entities/EntityList'
import NewEntity from '@/components/Entities/NewEntity'
import EntityDetails from '@/components/Entities/EntityDetails'

import AdminMain from '@/components/Admin/AdminMain'
import Tags from '@/components/Admin/Tags'
import Async from '@/components/Admin/Async'
import NotFound from '@/components/NotFound'

Vue.use(Router)

const uuidRegex = '([a-z-]+--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'

export const entityRoutes = {
  path: '/entities/:type([a-z-]+)?',
  component: Entities,
  props: true,
  children: [
    {
      path: '',
      name: 'EntityList',
      component: EntityList,
      props: true
    },
    {
      path: 'new',
      name: 'NewEntity',
      component: NewEntity,
      props: true
    },
    {
      path: '/entities/:id' + uuidRegex,
      name: 'EntityDetails',
      component: EntityDetails,
      props: true
    },
    {
      name: 'EntityEdit',
      path: '/entities/:id' + uuidRegex + '/edit',
      component: EntityDetails,
      props: (route) => { return {id: route.params.id, edit: true} }
    }
  ]
}

export const observableRoutes = {
  path: '/observables',
  component: Observables,
  props: true,
  children: [
    {
      path: 'browse',
      name: 'ObservableList',
      component: ObservableList,
      props: true
    },
    {
      path: '/observables/:id(\\d+)',
      name: 'ObservableDetails',
      component: ObservableDetails,
      props: true
    },
    {
      name: 'ObservableEdit',
      path: '/observables/:id(\\d+)/edit',
      component: ObservableDetails,
      props: (route) => { return {id: route.params.id, edit: true} }
    },
    {
      name: 'ObservablesBulk',
      path: '/observables/bulk',
      component: BulkMatch
    }
  ]
}

export const settingsRoutes = {
  path: '/admin',
  name: 'AdminMain',
  component: AdminMain,
  children: [
    {
      name: 'Tags',
      path: 'tags',
      component: Tags
    },
    {
      name: 'Async',
      path: 'async',
      component: Async
    }
  ]
}

export const routes = [
  // Observables
  observableRoutes,
  // Entities
  entityRoutes,
  // Settings
  settingsRoutes,
  {
    path: '*',
    name: 'NotFound',
    component: NotFound
  }
]

export default new Router({
  routes: routes,
  mode: 'history'
})
