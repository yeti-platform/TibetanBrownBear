import { shallow } from '@vue/test-utils'

import IndicatorList from '@/components/Indicators/IndicatorList'

describe('IndicatorList.vue', () => {
  let wrapper = shallow(IndicatorList, {propsData: {type: 'regex'}})

  it('Fields are correctly determined with type', () => {
    expect(wrapper.vm.filterParams.fields).toEqual([
      {name: 'name', type: 'text'},
      {name: 'pattern', type: 'code'}
    ])
  })
})
