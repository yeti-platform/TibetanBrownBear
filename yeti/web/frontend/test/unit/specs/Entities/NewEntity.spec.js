import { createLocalVue, shallow } from '@vue/test-utils'
import NewEntity from '@/components/Entities/NewEntity'
import Router from 'vue-router'
import { routes } from '@/router'

import mockObjects from '../../__mocks__/mock_objects'

describe('NewEntity.vue', () => {
  let wrapper

  beforeEach(() => {
    let localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = shallow(NewEntity, {
      localVue,
      router,
      propsData: {type: 'malware'}
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('Fields default fields are correct', () => {
    expect(wrapper.vm.defaultFields[wrapper.vm.type]).toEqual([
      {name: 'name', type: 'text'},
      {name: 'family', type: 'list'}
    ])
  })

  it('Fields default objects are correct given the type', () => {
    expect(wrapper.vm.defaultObjects[wrapper.vm.type]).toEqual({
      type: 'entity.malware',
      family: []
    })
  })

  it('redirects the user correctly when navigateToNew is called', () => {
    jest.spyOn(wrapper.vm.$router, 'push')
    wrapper.vm.navigateToNew(mockObjects.mockMalware)
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
      name: 'EntityDetails',
      params: {id: 510808},
      path: '/entities/510808'
    })
  })
})
