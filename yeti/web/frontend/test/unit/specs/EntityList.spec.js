import { createLocalVue, shallow } from '@vue/test-utils'

import EntityList from '@/components/Entities/EntityList'
import Router from 'vue-router'
import { routes } from '@/router'

import mockObjects from '../__mocks__/mock_objects'

const malwareObjectResponse = { data: mockObjects.mockMalware }

describe('EntityList.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = shallow(EntityList, {
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
    expect(wrapper.vm.$el.querySelector('.btn-toolbar .btn-outline-secondary').textContent)
      .toContain('New malware')
  })

  it('the Entity default object should match the provided props', () => {
    let malwareDefaultObject = {
      type: 'entity.malware',
      family: []
    }
    expect(wrapper.vm.defaultObject).toEqual(malwareDefaultObject)
  })

  it('the Entity type should match the provided props', () => {
    let malwareSubTypeFields = [
      {name: 'name', type: 'text'},
      {name: 'family', type: 'list'}
    ]
    expect(wrapper.vm.subTypeFields).toEqual(malwareSubTypeFields)
  })

  it('the new object is correctly navigated to', () => {
    jest.spyOn(wrapper.vm.$router, 'push')
    wrapper.vm.navigateToNew(malwareObjectResponse)
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
      name: 'EntityDetails',
      params: {'id': 510808},
      path: '/entities/510808'
    })
  })
})
