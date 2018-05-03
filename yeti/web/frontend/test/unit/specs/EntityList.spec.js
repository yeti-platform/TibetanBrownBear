import { createLocalVue, mount } from '@vue/test-utils'

import EntityList from '@/components/Entities/EntityList'
import EntityDetails from '@/components/Entities/EntityDetails'

import Router from 'vue-router'

const entityRoutes = {
  path: '/entities/:type([a-z]+)?',
  name: 'EntityList',
  component: EntityList,
  props: true,
  children: [
    {
      path: '/entities/:id(\\d+)',
      name: 'EntityDetails',
      component: EntityDetails,
      props: true
    }
  ]
}

const malwareObjectResponse = {
  data: {
    _id: 'entities/510808',
    family: [
      'trojan',
      'asd'
    ],
    id: 510808,
    name: 'dsa',
    type: 'entity.malware'
  }
}

describe('EntityList.vue', () => {
  let wrapper = mount(EntityList, {propsData: {type: 'malware'}})

  it('the New button should match the type', () => {
    expect(wrapper.vm.$el.querySelector('.btn-toolbar .btn-outline-secondary').textContent)
      .toContain('New malware')
  })

  it('the Entity default object should match the provided props', () => {
    let malwareDefaultObject = {
      type: 'entity.malware',
      family: []
    }
    expect(wrapper.vm.defaultObject).toEqual(malwareDefaultObject)
  })

  it('the Entity type should match the provided props', () => {
    let malwareSubTypeFields = [
      {name: 'name', type: 'text'},
      {name: 'family', type: 'list'}
    ]
    expect(wrapper.vm.subTypeFields).toEqual(malwareSubTypeFields)
  })

  it('the new object is correctly navigated to', () => {
    let localVue = createLocalVue()
    localVue.use(Router)
    let router = new Router({entityRoutes})
    const wrp = mount(EntityList, {
      localVue,
      router
    })
    jest.spyOn(wrp.vm.$router, 'push')
    wrp.vm.navigateToNew(malwareObjectResponse)
    expect(wrp.vm.$router.push).toHaveBeenCalledWith({
      name: 'EntityDetails',
      params: {
        id: 510808
      }
    })
  })
})
