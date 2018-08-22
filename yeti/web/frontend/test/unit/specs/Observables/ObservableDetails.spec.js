import { createLocalVue, shallowMount } from '@vue/test-utils'
import ObservableDetails from '@/components/Observables/ObservableDetails'
import Router from 'vue-router'
import axios from 'axios'
import { routes } from '@/router'

import mockObjects from '../../__mocks__/mock_objects'
jest.mock('axios', () => ({
  get: jest.fn((url) => {
    return Promise.resolve({ data: mockObservableObject, status: 200 })
  })
}))

const mockObservableObject = mockObjects.mockHostname

describe('ObservableDetails.vue', () => {
  let localVue
  let localWrp
  let fetchInfoSpy

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    fetchInfoSpy = jest.spyOn(ObservableDetails.methods, 'fetchInfo')
    localWrp = shallowMount(ObservableDetails, {
      localVue,
      router,
      propsData: { id: 483373 }
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('the ID value is correctly assigned as a prop', () => {
    expect(localWrp.vm.id).toBe(483373)
  })

  it('the loading text is correctly displayed', () => {
    localWrp.vm.loading = true
    expect(localWrp.find('div.loading').text()).toBe('Loading...')
  })

  it('correctly parses the observable type', () => {
    expect(localWrp.vm.observableType).toBe('domain-name')
  })

  it('correctly determines the fields depending on the type', () => {
    expect(localWrp.vm.observableFields).toEqual([
      {name: 'value', type: 'text'},
      {name: 'tags', type: 'tags'}
    ])
  })

  it('calls fetchInfo when mounted', () => {
    expect(fetchInfoSpy).toHaveBeenCalled()
  })

  // tests involving API interaction

  it('object is correctly fetched', (done) => {
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/observables/483373')
      expect(localWrp.vm.observable).toBe(mockObservableObject)
      done()
    })
  })

  it('not found responses are assigned to the error attribute', (done) => {
    localWrp.vm.id = 12345
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/observables/12345')
      done()
    })
  })
})
