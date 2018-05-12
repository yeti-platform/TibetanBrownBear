import { shallow } from '@vue/test-utils'

import EntityList from '@/components/Entities/EntityList'

describe('EntityList.vue', () => {
  let wrapper = shallow(EntityList, {propsData: {type: 'malware'}})

  it('Fields are correctly determined with type', () => {
    expect(wrapper.vm.filterParams.fields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'family', type: 'list'}
    ])
  })
})
