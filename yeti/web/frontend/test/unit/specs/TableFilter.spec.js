import { createLocalVue, mount } from '@vue/test-utils'
import Router from 'vue-router'
import { routes } from '@/router'
import axios from 'axios'

import TableFilter from '@/components/scaffolding/TableFilter'

import mockObjects from '../__mocks__/mock_objects'
jest.mock('axios', () => ({
  post: jest.fn((url) => {
    return Promise.resolve({ data: mockObjects.mockMalwareList, status: 200 })
  })
}))

const mockFilterParams = {
  apiPath: '/fake/api/path',
  fields: [
    {name: 'name', type: 'text'},
    {name: 'family', type: 'list'}
  ],
  queryKey: 'name',
  typeFilter: 'malware'
}

describe('TableFilter.vue', () => {
  let localVue
  let wrapper

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: routes, mode: 'history'})
    wrapper = mount(TableFilter, {
      localVue,
      router,
      propsData: {
        detailComponent: 'EntityDetails',
        filterParams: mockFilterParams
      }
    })
  })

  afterEach(() => {
    jest.resetModules()
    jest.clearAllMocks()
  })

  it('should display a loading message', () => {
    wrapper.vm.loading = true
    expect(wrapper.text()).toBe('Loading...')
  })

  it('should correctly fetch elements to display', () => {
    expect(axios.post).toHaveBeenCalled()
    let args = axios.post.mock.calls[0]
    expect(args[0]).toBe('/fake/api/path')
    expect(args[1]['type']).toBe('malware')
    expect(args[1]['name']).toBe('')
  })

  it('should correctly displayElements', () => {
    expect(wrapper.find('#table-filter')).toBeDefined()
    expect(wrapper.findAll('#table-filter tbody tr').length).toBe(3)
  })

  it('should correctly fetch filtered elements when enter is pressed', (done) => {
    let filterValue = 'malware'
    wrapper.vm.searchQuery = filterValue
    wrapper.find('input#filter').trigger('keyup.enter')
    wrapper.vm.$nextTick(() => {
      let args = axios.post.mock.calls[1]
      expect(args[1]['name']).toEqual(filterValue)
      done()
    })
  })

  // Selection tests

  it('should correctly select a single row', () => {
    let rows = wrapper.findAll('#table-filter tbody tr')
    rows.at(0).trigger('click.exact')
    expect(wrapper.vm.selectedElements.length).toBe(1)
    expect(wrapper.vm.selectedElements[0]).toEqual(mockObjects.mockMalwareList[0].id)
    expect(wrapper.emitted('input')).toBeTruthy()
    expect(wrapper.emitted('input').length).toBe(1) // tests the event count, not the actual length of what is emitted
    expect(wrapper.emitted().input[0]).toEqual([[mockObjects.mockMalwareList[0]]])
  })

  it('single row selection overrides previous selection', () => {
    let rows = wrapper.findAll('#table-filter tbody tr')
    rows.at(0).trigger('click.exact')
    expect(wrapper.vm.selectedElements.length).toBe(1)
    expect(wrapper.vm.selectedElements[0]).toEqual(mockObjects.mockMalwareList[0].id)
    expect(wrapper.emitted('input').length).toBe(1)
    rows.at(1).trigger('click.exact')
    expect(wrapper.vm.selectedElements.length).toBe(1)
    expect(wrapper.vm.selectedElements[0]).toEqual(mockObjects.mockMalwareList[1].id)
    expect(wrapper.emitted('input').length).toBe(2) // two events have been emitted
  })

  it('multiple row selection emits multiple items', () => {
    let rows = wrapper.findAll('#table-filter tbody tr')
    rows.at(0).trigger('click.exact')
    expect(wrapper.vm.selectedElements.length).toBe(1)
    expect(wrapper.vm.selectedElements[0]).toEqual(mockObjects.mockMalwareList[0].id)
    expect(wrapper.emitted('input').length).toBe(1)
    rows.at(1).trigger('click.exact', {shiftKey: true})
    expect(wrapper.vm.selectedElements.length).toBe(2)
    expect(wrapper.vm.selectedElements[0]).toEqual(mockObjects.mockMalwareList[0].id)
    expect(wrapper.vm.selectedElements[1]).toEqual(mockObjects.mockMalwareList[1].id)
    expect(wrapper.emitted('input').length).toBe(2)
  })

  it('cancels a multiple selection when clicking on a single row', () => {
    let rows = wrapper.findAll('#table-filter tbody tr')
    rows.at(0).trigger('click.exact')
    rows.at(1).trigger('click.exact', {shiftKey: true})
    rows.at(0).trigger('click.exact')
    expect(wrapper.vm.selectedElements.length).toBe(1)
    expect(wrapper.emitted('input').length).toBe(3)
  })

  it('shif+clicking twice on an item cancels its selection', () => {
    let rows = wrapper.findAll('#table-filter tbody tr')
    rows.at(0).trigger('click.exact', {shiftKey: true})
    rows.at(1).trigger('click.exact', {shiftKey: true})
    rows.at(1).trigger('click.exact', {shiftKey: true})
    expect(wrapper.vm.selectedElements.length).toBe(1)
    expect(wrapper.emitted('input').length).toBe(3)
  })

  it('selection is cleared correctly and emits an event', () => {
    let rows = wrapper.findAll('#table-filter tbody tr')
    rows.at(0).trigger('click.exact', {shiftKey: true})
    rows.at(1).trigger('click.exact', {shiftKey: true})
    wrapper.vm.clearSelection()
    expect(wrapper.vm.selectedElements.length).toBe(0)
    expect(wrapper.emitted('input').length).toBe(3)
    expect(wrapper.emitted().input[2]).toEqual([[]])
  })
})
