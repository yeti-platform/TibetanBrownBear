import Vue from 'vue'
import Router from 'vue-router'
import Observables from '@/components/Observables'
import EntityList from '@/components/Entities/EntityList'
import EntityDetails from '@/components/Entities/EntityDetails'
import Indicators from '@/components/Indicators'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/observables',
      name: 'Observables',
      component: Observables
    },
    {
      path: '/entities/:type([a-z]+)',
      name: 'EntityList',
      component: EntityList
    },
    {
      path: '/entities/:id(\\d+)',
      name: 'EntityDetails',
      component: EntityDetails
    },
    {
      path: '/indicators',
      name: 'Indicators',
      component: Indicators
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ],
  mode: 'history'
})
