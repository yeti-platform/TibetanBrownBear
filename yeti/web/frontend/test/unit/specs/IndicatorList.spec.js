import { createLocalVue, mount } from '@vue/test-utils'

import IndicatorList from '@/components/Indicators/IndicatorList'
import IndicatorDetails from '@/components/Indicators/IndicatorDetails'

import Router from 'vue-router'

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
      props: true
    }
  ]
}]

const regexObjectResponse = {
  data: {
    _id: 'indicators/477775',
    id: 477775,
    name: 'asdasd',
    pattern: '[a-z]{1a,2}',
    type: 'indicator.regex'
  }
}

describe('IndicatorList.vue', () => {
  let wrapper = mount(IndicatorList, {propsData: {type: 'regex'}})

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
    let localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: indicatorRoutes, mode: 'history'})
    const wrp = mount(IndicatorList, {
      localVue,
      router
    })
    jest.spyOn(wrp.vm.$router, 'push')
    wrp.vm.navigateToNew(regexObjectResponse)
    expect(wrp.vm.$router.push).toHaveBeenCalledWith({
      name: 'IndicatorDetails',
      params: {id: 477775},
      path: '/indicators/477775'
    })
  })
})
