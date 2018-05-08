import { createLocalVue, mount } from '@vue/test-utils'

import IndicatorList from '@/components/Indicators/IndicatorList'
import IndicatorDetails from '@/components/Indicators/IndicatorDetails'
import Router from 'vue-router'

import mockObjects from '../__mocks__/mock_objects'

const regexObjectResponse = {data: mockObjects.mockRegex}

const indicatorRoutes = [{
  path: '/indicators/:type([a-z]+)?',
  name: 'IndicatorList',
  component: IndicatorList,
  props: true,
  children: [
    {
      path: '/indicators/:id(\\d+)',
      name: 'IndicatorDetails',
      component: IndicatorDetails,
      props: true,
      children: [
        {
          name: 'IndicatorEdit',
          path: 'edit',
          component: IndicatorDetails
        }
      ]
    }
  ]
}]

describe('IndicatorList.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: indicatorRoutes, mode: 'history'})
    wrapper = mount(IndicatorList, {
      localVue,
      router,
      propsData: {type: 'regex'}
    })
  })

  it('the New button should match the type', () => {
    expect(wrapper.vm.$el.querySelector('.btn-toolbar .btn-outline-secondary').textContent)
      .toContain('New regex')
  })

  it('the Indicator default object should match the provided props', () => {
    let regexDefaultObject = {
      type: 'indicator.regex',
      pattern: ''
    }
    expect(wrapper.vm.defaultObject).toEqual(regexDefaultObject)
  })

  it('the Indicator type should match the provided props', () => {
    let regexSubTypeFields = [
      {name: 'name', type: 'text'},
      {name: 'pattern', type: 'code'}
    ]
    expect(wrapper.vm.subTypeFields).toEqual(regexSubTypeFields)
  })

  it('the new object is correctly navigated to', () => {
    jest.spyOn(wrapper.vm.$router, 'push')
    wrapper.vm.navigateToNew(regexObjectResponse)
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
      name: 'IndicatorDetails',
      params: {id: 477775},
      path: '/indicators/477775'
    })
  })
})
