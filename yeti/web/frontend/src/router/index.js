import Vue from 'vue'
import Router from 'vue-router'
import Observables from '@/components/Observables'
import Entities from '@/components/Entities'
import EntityDetails from '@/components/EntityDetails'
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
      path: '/entities',
      name: 'Entities',
      component: Entities,
      children: Entities.childrenRoutes
    },
    {
      path: '/entities/:id',
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
