import { shallowMount } from '@vue/test-utils'

import KillChainView from '@/components/Entities/KillChainView'
import axios from 'axios'

import mockObjects from '../../__mocks__/mock_objects'

jest.mock('axios', () => ({
  get: jest.fn((url) => {
    return Promise.resolve({ data: mockObjects.mockKillChains, status: 200 })
  }),
  post: jest.fn((url) => {
    return Promise.resolve({ data: mockObjects.mockNeighbors, status: 200 })
  })
}))

describe('KillChainView.vue', () => {
  let wrapper = shallowMount(KillChainView, {
    propsData: { entity: { 'id': 'malware--123' } },
    stubs: ['router-link', 'router-view']
  })

  it('Neighbor per killchain object is correctly populated', () => {
    wrapper.vm.getKillchains()
    expect(wrapper.vm.killchains).toEqual(mockObjects.mockKillChains)
    expect(axios.get).toHaveBeenCalledWith('/settings/killchains/')
    expect(axios.post).toHaveBeenCalledWith('/entities/malware--123/neighbors/')
    expect(wrapper.vm.neighborsPerKillchain).toEqual({
      'kc1': {
        'foo': [
          {
            'created': '2017-05-31T21:30:19.735Z',
            'created_by_ref': 'identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5',
            'description': 'blah',
            'external_references': [],
            'id': 'attackpattern1',
            'kill_chain_phases': [{ 'kill_chain_name': 'kc1', 'phase_name': 'foo' }],
            'modified': '2018-10-17T00:14:20.652Z',
            'name': 'Credential Dumping',
            'object_marking_refs': ['marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168'],
            'type': 'attack-pattern' }
        ]
      }
    })
  })

  it('Phases for a killchain can be retrieved', () => {
    wrapper.vm.getKillchains()
    expect(wrapper.vm.getPhases(wrapper.vm.killchains[0])).toEqual([{
      'description': 'First and last phase',
      'name': 'foo'
    }])
  })

})
