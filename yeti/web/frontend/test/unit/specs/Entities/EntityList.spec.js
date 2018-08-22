import { shallowMount } from '@vue/test-utils'

import EntityList from '@/components/Entities/EntityList'

describe('EntityList.vue', () => {
  let wrapper = shallowMount(EntityList, {propsData: {type: 'malware'}})

  it('Fields are correctly determined with type', () => {
    expect(wrapper.vm.filterParams.fields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'labels', type: 'list'}
    ])
  })
})
