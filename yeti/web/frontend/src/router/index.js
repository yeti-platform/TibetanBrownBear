import Vue from 'vue'
import Router from 'vue-router'
import Observables from '@/components/Observables'
import Entities from '@/components/Entities'
import Indicators from '@/components/Indicators'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/observables', name: 'Observables', component: Observables, props: true },
    { path: '/entities', name: 'Entities', component: Entities, props: true },
    { path: '/indicators', name: 'Indicators', component: Indicators, props: true },
    { path: '*', name: 'NotFound', component: NotFound, props: true }
  ],
  mode: 'history'
})
