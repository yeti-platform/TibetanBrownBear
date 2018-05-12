import { createLocalVue, shallow } from '@vue/test-utils'
import NewIndicator from '@/components/Indicators/NewIndicator'
import Router from 'vue-router'
import { routes } from '@/router'

import mockObjects from '../../__mocks__/mock_objects'

describe('NewIndicator.vue', () => {
  let wrapper

  beforeEach(() => {
    let localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = shallow(NewIndicator, {
      localVue,
      router,
      propsData: {type: 'regex'}
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('Fields default fields are correct', () => {
    expect(wrapper.vm.defaultFields[wrapper.vm.type]).toEqual([
      {name: 'name', type: 'text'},
      {name: 'pattern', type: 'code'}
    ])
  })

  it('Fields default objects are correct given the type', () => {
    expect(wrapper.vm.defaultObjects[wrapper.vm.type]).toEqual({
      type: 'indicator.regex',
      pattern: ''
    })
  })

  it('redirects the user correctly when navigateToNew is called', () => {
    jest.spyOn(wrapper.vm.$router, 'push')
    wrapper.vm.navigateToNew(mockObjects.mockRegex)
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
      name: 'IndicatorDetails',
      params: {id: 477775},
      path: '/indicators/477775'
    })
  })
})
