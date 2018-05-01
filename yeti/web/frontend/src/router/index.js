import Vue from 'vue'
import Router from 'vue-router'

import ObservableList from '@/components/Observables/ObservableList'
import ObservableDetails from '@/components/Observables/ObservableDetails'

import EntityList from '@/components/Entities/EntityList'
import EntityDetails from '@/components/Entities/EntityDetails'

import IndicatorList from '@/components/Indicators/IndicatorList'
import IndicatorDetails from '@/components/Indicators/IndicatorDetails'

import AdminMain from '@/components/Admin/AdminMain'
import Tags from '@/components/Admin/Tags'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
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
              component: ObservableDetails
            }
          ]
        }
      ]
    },
    // Entities
    {
      path: '/entities/:type([a-z]+)?',
      name: 'EntityList',
      component: EntityList,
      children: [
        {
          path: '/entities/:id(\\d+)',
          name: 'EntityDetails',
          component: EntityDetails,
          children: [
            {
              name: 'EntityEdit',
              path: 'edit',
              component: EntityDetails
            }
          ]
        }
      ]
    },
    // Indicators
    {
      path: '/indicators/:type([a-z]+)?',
      name: 'IndicatorList',
      component: IndicatorList,
      children: [
        {
          path: '/indicators/:id(\\d+)',
          name: 'IndicatorDetails',
          component: IndicatorDetails,
          children: [
            {
              name: 'IndicatorEdit',
              path: 'edit',
              component: IndicatorDetails
            }
          ]
        }
      ]
    },
    // Settings
    {
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
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ],
  mode: 'history'
})
