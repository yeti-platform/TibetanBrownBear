import { mount } from '@vue/test-utils'

// import TableFilter from '@/components/scaffolding/TableFilter'
import Fields from '@/components/helpers/Fields'

const fakeElement = {
  _id: 'entities/510808',
  family: [
    'trojan',
    'banker'
  ],
  id: 510808,
  name: 'MyMalware',
  type: 'entity.malware',
  created_at: '2018-04-16T16:18:25.179482+00:00',
  randomcode: `This is code`,
  tags: [
    {
      expiration: '2018-05-02T15:39:06.543454+00:00',
      first_seen: '2018-05-01T15:39:06.543454+00:00',
      fresh: true,
      last_seen: '2018-05-01T17:15:16.567785+00:00',
      name: 'tag1'
    },
    {
      expiration: '2018-05-02T16:50:52.002557+00:00',
      first_seen: '2018-05-01T16:50:52.002557+00:00',
      fresh: true,
      last_seen: '2018-05-01T17:15:16.567785+00:00',
      name: 'tag2'
    }
  ]
}

describe('TableFilter.vue', () => {
  it('should correctly render generic text fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'name', type: 'text'}, elt: fakeElement
      }
    })
    expect(wrapper.text()).toBe('MyMalware')
  })

  it('should correctly render list fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'family', type: 'list'}, elt: fakeElement
      }
    })
    expect(wrapper.findAll('.family span.badge').length).toBe(2)
    expect(wrapper.findAll('.family span.badge').at(0).text()).toBe('trojan')
    expect(wrapper.findAll('.family span.badge').at(1).text()).toBe('banker')
  })

  it('should correctly render datetime fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'created_at', type: 'datetime'}, elt: fakeElement
      }
    })
    expect(wrapper.find('.created_at').text()).toBe('2018-04-16 18:18:25 +0200')
  })

  it('should correctly render code fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'randomcode', type: 'code'}, elt: fakeElement
      }
    })
    expect(wrapper.find('pre').text()).toBe(`This is code`)
  })

  it('should correctly handle tag fields', () => {
    let wrapper = mount(Fields, {
      propsData: {
        field: {name: 'tags', type: 'tags'}, elt: fakeElement
      }
    })
    expect(wrapper.findAll('.tags span.badge').length).toBe(2)
    expect(wrapper.findAll('.tags span.badge').at(0).text()).toBe('tag1')
    expect(wrapper.findAll('.tags span.badge').at(1).text()).toBe('tag2')
  })

})
