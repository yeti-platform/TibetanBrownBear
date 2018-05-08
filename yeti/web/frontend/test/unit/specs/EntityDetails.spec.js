import { createLocalVue, mount } from '@vue/test-utils'
import EntityDetails from '@/components/Entities/EntityDetails'
import Router from 'vue-router'
import axios from 'axios'
import { routes } from '@/router'

import mockObjects from '../__mocks__/mock_objects'
jest.mock('axios', () => ({
  get: jest.fn((url) => {
    return Promise.resolve({ data: mockMalwareObject, status: 200 })
  })
}))

const mockMalwareObject = mockObjects.mockMalware

describe('EntityDetails.vue', () => {
  let localVue
  let localWrp
  let fetchInfoSpy

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    fetchInfoSpy = jest.spyOn(EntityDetails.methods, 'fetchInfo')
    localWrp = mount(EntityDetails, {
      localVue,
      router,
      propsData: { id: 510808 }
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('the ID value is correctly assigned as a prop', () => {
    expect(localWrp.vm.id).toBe(510808)
  })

  it('the loading text is correctly displayed', () => {
    localWrp.vm.loading = true
    expect(localWrp.find('div.loading').text()).toBe('Loading...')
  })

  it('correctly navigates to the edit component when button is clicked', (done) => {
    jest.spyOn(localWrp.vm.$router, 'push')
    localWrp.find('a.edit').trigger('click')
    localWrp.vm.$nextTick(() => {
      expect(localWrp.vm.$router.push).toHaveBeenCalledWith({
        name: 'EntityEdit',
        params: {'id': 510808},
        path: '/entities/510808/edit'
      })
      expect(localWrp.vm.isEdit).toBe(true)
      done()
    })
  })

  it('correctly parses the entity type', () => {
    expect(localWrp.vm.entityType).toBe('malware')
  })

  it('correctly determines the fields depending on the type', () => {
    expect(localWrp.vm.entityFields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'family', type: 'list', autocompleteValues: ['trojan', 'banker']}
    ])
  })

  it('calls fetchInfo when mounted', () => {
    expect(fetchInfoSpy).toHaveBeenCalled()
  })

  // tests involving API interaction

  it('object is correctly fetched', (done) => {
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/entities/510808')
      expect(localWrp.vm.entity).toBe(mockMalwareObject)
      done()
    })
  })

  it('not found responses are assigned to the error attribute', (done) => {
    localWrp.vm.id = 12345
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/entities/12345')
      done()
    })
  })


})
