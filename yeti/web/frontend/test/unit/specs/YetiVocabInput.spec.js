import { createLocalVue, mount } from '@vue/test-utils'

import YetiVocabInput from '@/components/scaffolding/YetiVocabInput'
import Router from 'vue-router'
import { routes } from '@/router'
import mockObjects from '../__mocks__/mock_objects'

jest.mock('axios', () => ({
  post: jest.fn((url) => {
    return Promise.resolve({ data: mockObjects.malwareLabelOV, status: 200 })
  })
}))

describe('YetiVocabInput.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})

    wrapper = mount(YetiVocabInput, {
      localVue,
      router,
      propsData: {value: []}
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('plain items are processed correctly', () => {
    wrapper.setProps({
      value: ['tag1', 'tag2', 'tag3']
    })
    expect(wrapper.vm.listItems).toEqual([{text: 'tag1'}, {text: 'tag2'}, {text: 'tag3'}])
  })

  it('tags are processed correctly', () => {
    wrapper.setProps({
      value: [{name: 'tag1', data: 'random'}, {name: 'tag2', data: 'asd'}],
      displayKey: 'name'
    })
    expect(wrapper.vm.listItems).toEqual([{text: 'tag1'}, {text: 'tag2'}])
  })
})
