import { createLocalVue, shallowMount } from '@vue/test-utils'
import Sidebar from '@/components/scaffolding/Sidebar'
import Router from 'vue-router'
import { routes } from '@/router'

describe('Sidebar.vue', () => {
  let wrapper
  let localVue

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({ routes: routes, mode: 'history' })
    wrapper = shallowMount(Sidebar, {
      localVue,
      router,
      propsData: { id: 'malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b' }
    })
  })

  it('should render correct contents', () => {
    expect(wrapper.vm.$el.querySelector('span').textContent)
      .toEqual('Intelligence')
  })
})
