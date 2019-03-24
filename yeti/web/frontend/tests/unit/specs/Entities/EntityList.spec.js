import { shallowMount } from '@vue/test-utils'

import EntityList from '@/components/Entities/EntityList'

describe('EntityList.vue', () => {
  let wrapper = shallowMount(EntityList, {
    propsData: { type: 'malware' },
    stubs: ['router-link', 'router-view']
  })

  it('Fields are correctly determined with type', () => {
    expect(wrapper.vm.filterParams.fields).toEqual([
      { name: 'name', type: 'text', humanName: 'Name' },
      { name: 'labels', type: 'list', vocab: 'malware-label-ov', humanName: 'Labels' },
      { name: 'kill_chain_phases', type: 'killchain', humanName: 'Kill-chain stage' }
    ])
  })

  it('the New button should match the type', () => {
    expect(wrapper.find('#new-entity').text())
      .toContain('New Malware')
  })
})
