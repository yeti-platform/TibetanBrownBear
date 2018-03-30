import Vue from 'vue'
import Router from 'vue-router'
import Observables from '@/components/Observables'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/observables', component: Observables },
    { path: '*', component: NotFound }
  ],
  mode: 'history'
})
