import { mount } from '@vue/test-utils'

import Fields from '@/components/helpers/Fields'
import mockObjects from '../__mocks__/mock_objects'
import moment from 'moment-timezone'

describe('Fields.vue', () => {
  it('should correctly render generic text fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'name', type: 'text'}, elt: mockObjects.mockMalware
      }
    })
    expect(wrapper.text()).toBe('MyMalware')
  })

  it('should correctly render list fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'family', type: 'list'}, elt: mockObjects.mockMalware
      }
    })
    expect(wrapper.findAll('.family span.badge').length).toBe(2)
    expect(wrapper.findAll('.family span.badge').at(0).text()).toBe('trojan')
    expect(wrapper.findAll('.family span.badge').at(1).text()).toBe('banker')
  })

  it('should correctly render datetime fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'first_seen', type: 'datetime'}, elt: mockObjects.mockHostname.tags[0]
      }
    })
    let dateRegexp = /[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \+[0-9]{4}/
    expect(wrapper.find('.first_seen').text()).toMatch(dateRegexp)
  })

  it('should correctly render code fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'pattern', type: 'code'}, elt: mockObjects.mockRegex
      }
    })
    expect(wrapper.find('pre').text()).toBe('[a-z]{1,2}')
  })

  it('should correctly handle tag fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'tags', type: 'tags'}, elt: mockObjects.mockHostname
      }
    })
    expect(wrapper.findAll('.tags span.badge').length).toBe(3)
    expect(wrapper.findAll('.tags span.badge').at(0).text()).toBe('asd')
    expect(wrapper.findAll('.tags span.badge').at(1).text()).toBe('zxc')
    expect(wrapper.findAll('.tags span.badge').at(2).text()).toBe('qwe')
  })
})
