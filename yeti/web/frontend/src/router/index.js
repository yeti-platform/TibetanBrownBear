import Vue from 'vue'
import Router from 'vue-router'

import ObservableList from '@/components/Observables/ObservableList'
import ObservableDetails from '@/components/Observables/ObservableDetails'

import Entities from '@/components/Entities/Entities'
import EntityList from '@/components/Entities/EntityList'
import NewEntity from '@/components/Entities/NewEntity'
import EntityDetails from '@/components/Entities/EntityDetails'

import Indicators from '@/components/Indicators/Indicators'
import IndicatorList from '@/components/Indicators/IndicatorList'
import NewIndicator from '@/components/Indicators/NewIndicator'
import IndicatorDetails from '@/components/Indicators/IndicatorDetails'

import AdminMain from '@/components/Admin/AdminMain'
import Tags from '@/components/Admin/Tags'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export const entityRoutes = {
  path: '/entities/:type([a-z]+)?',
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
      path: '/entities/:id(\\d+)',
      name: 'EntityDetails',
      component: EntityDetails,
      props: true
    },
    {
      name: 'EntityEdit',
      path: '/entities/:id(\\d+)/edit',
      component: EntityDetails,
      props: (route) => { return {id: route.params.id, edit: true} }
    }
  ]
}

export const indicatorRoutes = {
  path: '/indicators/:type([a-z]+)?',
  component: Indicators,
  props: true,
  children: [
    {
      path: '',
      name: 'IndicatorList',
      component: IndicatorList,
      props: true
    },
    {
      path: 'new',
      name: 'NewIndicator',
      component: NewIndicator,
      props: true
    },
    {
      path: '/indicators/:id(\\d+)',
      name: 'IndicatorDetails',
      component: IndicatorDetails,
      props: true
    },
    {
      name: 'IndicatorEdit',
      path: '/indicators/:id(\\d+)/edit',
      component: IndicatorDetails,
      props: (route) => { return {id: route.params.id, edit: true} }
    }
  ]
}

export const observableRoutes = {
  path: '/observables',
  name: 'ObservableList',
  component: ObservableList,
  props: true,
  children: [
    {
      path: '/observables/:id(\\d+)',
      name: 'ObservableDetails',
      component: ObservableDetails,
      props: true,
      children: [
        {
          name: 'ObservableEdit',
          path: 'edit',
          component: ObservableDetails,
          props: true
        }
      ]
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
    }
  ]
}

export const routes = [
  // Observables
  observableRoutes,
  // Entities
  entityRoutes,
  // Indicators
  indicatorRoutes,
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
