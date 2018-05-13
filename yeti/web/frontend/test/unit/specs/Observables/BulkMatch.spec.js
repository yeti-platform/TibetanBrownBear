import { createLocalVue, shallow } from '@vue/test-utils'
import BulkMatch from '@/components/Observables/BulkMatch'
import Router from 'vue-router'
import axios from 'axios'
import { routes } from '@/router'

import mockObjects from '../../__mocks__/mock_objects'
jest.mock('axios', () => ({
  post: jest.fn((url) => {
    return Promise.resolve({ data: mockMatchResult, status: 200 })
  })
}))

const mockMatchResult = mockObjects.mockObservableMatchresult

describe('BulkMatch.vue', () => {
  let localVue
  let localWrp

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    localWrp = shallow(BulkMatch, {
      localVue,
      router
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('the textarea is correctly parsed when form is submitted', () => {
    localWrp.setData({rawInput: 'tota.com\ntoto.com\nasd'})
    localWrp.find('form').trigger('submit')
    expect(localWrp.vm.observables).toEqual(['tota.com', 'toto.com', 'asd'])
  })

  it('query is correcly sent', () => {
    localWrp.setData({rawInput: 'tota.com\ntoto.com\nasd'})
    localWrp.find('form').trigger('submit')
    let expectedParams = {observables: ['tota.com', 'toto.com', 'asd']}
    expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/api/observables/match', expectedParams)
  })

  it('results are correctly displayed in a <pre> tag', (done) => {
    localWrp.setData({rawInput: 'tota.com\ntoto.com\nasd'})
    localWrp.find('form').trigger('submit')
    localWrp.vm.$nextTick(() => {
      let resultText = localWrp.find('pre').text()
      expect(resultText).toContain('asd')
      expect(resultText).toContain('"error": null')
      expect(resultText).toContain('"error": "Invalid observable type"')
      done()
    })
  })
})
