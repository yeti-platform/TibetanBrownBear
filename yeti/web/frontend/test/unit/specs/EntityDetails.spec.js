import { createLocalVue, mount } from '@vue/test-utils'

import EntityDetails from '@/components/Entities/EntityDetails'

import Router from 'vue-router'

import axios from 'axios'

const entityRoutes = [{
  path: '/entities/:id(\\d+)',
  name: 'EntityDetails',
  component: EntityDetails,
  props: true,
  children: [
    {
      name: 'EntityEdit',
      path: 'edit',
      component: EntityDetails
    }
  ]
}]

const mockMalwareObject = {
  _id: 'entities/510808',
  family: [
    'trojan',
    'asd'
  ],
  id: 510808,
  name: 'dsa',
  type: 'entity.malware'
}

jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: mockMalwareObject, status: 200 }))
}))

describe('EntityDetails.vue', () => {
  let localVue
  let localWrp

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({routes: entityRoutes, mode: 'history'})
    localWrp = mount(EntityDetails, {
      localVue,
      router,
      propsData: { id: 510808 }
    })
    jest.resetModules()
    jest.clearAllMocks()
  })

  // let wrapper = mount(EntityDetails)

  it('the ID value is correctly assigned as a prop', () => {
    expect(localWrp.vm.id).toBe(510808)
  })

  it('the loading text is correctly displayed', () => {
    localWrp.vm.loading = true
    expect(localWrp.find('div.loading').text()).toBe('Loading...')
  })

  it('object is correctly fetched', (done) => {
    localWrp.vm.fetchInfo()
    localWrp.vm.$nextTick(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/api/entities/510808')
      expect(localWrp.vm.entity).toBe(mockMalwareObject)
      done()
    })
  })

  it('correctly navigates to the edit component when button is clicked', (done) => {
    jest.spyOn(localWrp.vm.$router, 'push')
    localWrp.find('a.edit').trigger('click')
    localWrp.vm.$nextTick(() => {
      expect(localWrp.vm.$router.push).toHaveBeenCalledWith({
        name: 'EntityEdit',
        params: {'id': 510808},
        path: '/entities/510808/edit'
      })
      expect(localWrp.vm.isEdit).toBe(true)
      done()
    })
  })

  it('correctly parses the entity type', () => {
    expect(localWrp.vm.entityType).toBe('malware')
  })

  it('correctly determines the fields depending on the type', () => {
    expect(localWrp.vm.entityFields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'family', type: 'list', autocompleteValues: ['trojan', 'banker']}
    ])
  })

})
