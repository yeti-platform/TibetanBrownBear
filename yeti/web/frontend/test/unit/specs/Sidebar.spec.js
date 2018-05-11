import { createLocalVue, shallow } from '@vue/test-utils'
import Sidebar from '@/components/scaffolding/Sidebar'
import Router from 'vue-router'
import { routes } from '@/router'

describe('Sidebar.vue', () => {
  let wrapper
  let localVue

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = shallow(Sidebar, {
      localVue,
      router,
      propsData: { id: 510808 }
    })
  })

  it('should render correct contents', () => {
    expect(wrapper.vm.$el.querySelector('span').textContent)
      .toEqual('Intelligence')
  })
})
