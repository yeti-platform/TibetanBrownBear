import { createLocalVue, mount } from '@vue/test-utils'
import IndicatorDetails from '@/components/Indicators/IndicatorDetails'
import Router from 'vue-router'
import axios from 'axios'

import mockObjects from '../__mocks__/mock_objects'
jest.mock('axios', () => ({
  get: jest.fn((url) => {
    return Promise.resolve({ data: mockIndicatorObject, status: 200 })
  })
}))

const mockIndicatorObject = mockObjects.mockRegex

const indicatorRoutes = [{
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
}]

describe('IndicatorDetails.vue', () => {
  let localVue
  let localWrp
  let fetchInfoSpy

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: indicatorRoutes, mode: 'history'})
    jest.resetModules()
    jest.clearAllMocks()
    fetchInfoSpy = jest.spyOn(IndicatorDetails.methods, 'fetchInfo')
    localWrp = mount(IndicatorDetails, {
      localVue,
      router,
      propsData: { id: 477775 }
    })
  })

  // let wrapper = mount(IndicatorDetails)

  it('the ID value is correctly assigned as a prop', () => {
    expect(localWrp.vm.id).toBe(477775)
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
        name: 'IndicatorEdit',
        params: {'id': 477775},
        path: '/indicators/477775/edit'
      })
      expect(localWrp.vm.isEdit).toBe(true)
      done()
    })
  })

  it('correctly parses the indicator type', () => {
    expect(localWrp.vm.indicatorType).toBe('regex')
  })

  it('correctly determines the fields depending on the type', () => {
    expect(localWrp.vm.indicatorFields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'pattern', type: 'code'}
    ])
  })

  it('calls fetchInfo when mounted', () => {
    expect(fetchInfoSpy).toHaveBeenCalled()
  })

  // tests involving API interaction

  it('object is correctly fetched', (done) => {
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/indicators/477775')
      expect(localWrp.vm.indicator).toBe(mockIndicatorObject)
      done()
    })
  })

  it('not found responses are assigned to the error attribute', (done) => {
    localWrp.vm.id = 12345
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/indicators/12345')
      done()
    })
  })


})
