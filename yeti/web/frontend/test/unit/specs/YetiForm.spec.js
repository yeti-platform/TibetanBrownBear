import { shallow } from '@vue/test-utils'

import YetiForm from '@/components/scaffolding/YetiForm'
import mockObjects from '../__mocks__/mock_objects'
import axios from 'axios'

jest.mock('axios', () => ({
  put: jest.fn((url) => {
    return Promise.resolve({ data: mockObjects.mockMalware, status: 200 })
  })
}))

describe('YetiForm.vue', () => {
  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('should correctly render generic text fields', () => {
    let wrapper = shallow(YetiForm, {
      propsData: {
        fields: [{name: 'name', type: 'text'}],
        apiPath: '',
        object: mockObjects.mockMalware
      }
    })
    expect(wrapper.find('#name').element.value).toBe(mockObjects.mockMalware.name)
  })

  it('should correctly render code fields', () => {
    let wrapper = shallow(YetiForm, {
      propsData: {
        fields: [{name: 'pattern', type: 'code'}],
        apiPath: '',
        object: mockObjects.mockRegex
      }
    })
    expect(wrapper.find('#pattern').element.value).toBe(mockObjects.mockRegex.pattern)
  })

  it('should correctly submit object information', (done) => {
    let wrapper = shallow(YetiForm, {
      propsData: {
        fields: [{name: 'name', type: 'text'}],
        apiPath: '/fake/api/path',
        method: 'PUT',
        object: mockObjects.mockMalware
      }
    })
    mockObjects.mockMalware.name = 'NastyMalware'
    jest.spyOn(axios, 'put')
    wrapper.find('form').trigger('submit')
    wrapper.vm.$nextTick(() => {
      expect(axios.put).toHaveBeenCalledWith('/fake/api/path', mockObjects.mockMalware)
      let args = axios.put.mock.calls[0]
      expect(args[1].name).toBe('NastyMalware')
      done()
    })
  })

  it('correctly calls the onsavecallback function', () => {
    let wrapper = shallow(YetiForm, {
      propsData: {
        fields: [{name: 'name', type: 'text'}],
        apiPath: '/fake/api/path',
        method: 'PUT',
        object: mockObjects.mockMalware
      }
    })
    wrapper.find('form').trigger('submit')
    wrapper.vm.$nextTick(() => {
      expect(wrapper.emitted()['form-submit'][0][0]).toEqual(mockObjects.mockMalware)
    })
  })
})
