import { createLocalVue, shallowMount } from '@vue/test-utils'
import EntityDetails from '@/components/Entities/EntityDetails'
import Router from 'vue-router'
import axios from 'axios'
import { routes } from '@/router'

import mockObjects from '../../__mocks__/mock_objects'
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
    localWrp = shallowMount(EntityDetails, {
      localVue,
      router,
      propsData: { id: 'malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b' }
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('the ID value is correctly assigned as a prop', () => {
    expect(localWrp.vm.id).toBe('malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b')
  })

  it('the loading text is correctly displayed', () => {
    localWrp.vm.loading = true
    expect(localWrp.findAll('div.loading')).toBeTruthy()
  })

  it('correctly parses the entity type', () => {
    expect(localWrp.vm.entityType).toBe('malware')
  })

  it('correctly determines the fields depending on the type', () => {
    expect(localWrp.vm.entityFields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'labels', type: 'list', vocab: 'malware'},
      {name: 'description', type: 'longtext'},
      {name: 'kill_chain_phases', type: 'killchain'}
    ])
  })

  it('calls fetchInfo when mounted', () => {
    expect(fetchInfoSpy).toHaveBeenCalled()
  })

  // tests involving API interaction

  it('object is correctly fetched', (done) => {
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/entities/malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b')
      expect(localWrp.vm.entity).toBe(mockMalwareObject)
      done()
    })
  })

  it('not found responses are assigned to the error attribute', (done) => {
    localWrp.vm.id = 'malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b'
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/entities/malware--976c0bcf-91f3-4ab8-a0cf-f01692afcb5b')
      done()
    })
  })
})
