import { createLocalVue, shallowMount } from '@vue/test-utils'
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
    wrapper = shallowMount(NewEntity, {
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
    expect(wrapper.vm.editFields[wrapper.vm.type]).toEqual([
      {name: 'name', type: 'text'},
      {name: 'labels', type: 'list', vocab: 'malware-label-ov'},
      {name: 'description', type: 'longtext'},
      {name: 'kill_chain_phases', type: 'killchain'}
    ])
  })

  it('Fields default objects are correct given the type', () => {
    expect(wrapper.vm.defaultObjects[wrapper.vm.type]).toEqual({
      type: 'malware'
    })
  })

  it('redirects the user correctly when navigateToNew is called', () => {
    jest.spyOn(wrapper.vm.$router, 'push')
    wrapper.vm.navigateToNew(mockObjects.mockMalware)
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
      name: 'EntityDetails',
      params: {id: 'malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b'},
      path: '/entities/malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b'
    })
  })
})
