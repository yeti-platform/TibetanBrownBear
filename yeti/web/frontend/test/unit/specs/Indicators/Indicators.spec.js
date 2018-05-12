import { createLocalVue, mount } from '@vue/test-utils'

import Indicators from '@/components/Indicators/Indicators'
import Router from 'vue-router'
import { routes } from '@/router'

describe('Indicators.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = mount(Indicators, {
      localVue,
      router,
      propsData: {type: 'regex'}
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('the New button should match the type', () => {
    expect(wrapper.find('#new-indicator').text())
      .toContain('New regex')
  })
})
