import { createLocalVue, mount } from '@vue/test-utils'

import Entities from '@/components/Entities/Entities'
import Router from 'vue-router'
import { routes } from '@/router'

describe('Entities.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = mount(Entities, {
      localVue,
      router,
      propsData: {type: 'malware'}
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('the New button should match the type', () => {
    expect(wrapper.find('#new-entity').text())
      .toContain('New malware')
  })
})
