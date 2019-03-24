import { createLocalVue, mount } from '@vue/test-utils'

import Async from '@/components/Admin/Async'
import Router from 'vue-router'
import { routes } from '@/router'
import mockObjects from '../../__mocks__/mock_objects'

const toggleSpy = jest.spyOn(Async.methods, 'toggle')
const executeSpy = jest.spyOn(Async.methods, 'execute')

jest.mock('axios', () => ({
  post: jest.fn((url) => {
    return Promise.resolve({ data: mockObjects.mockMalwareList, status: 200 })
  })
}))

describe('Async.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})

    wrapper = mount(Async, {
      localVue,
      router
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('should call toggle function when clicking on toggle', () => {
    let toggle = wrapper.findAll('#table-filter tbody tr .btn')
    toggle.at(0).trigger('click.exact')
    expect(toggleSpy).toHaveBeenCalled()
  })

  it('should call the execute function when clicking on execute', () => {
    let execute = wrapper.findAll('#table-filter tbody tr .btn')
    execute.at(1).trigger('click.exact')
    expect(executeSpy).toHaveBeenCalled()
  })
})
