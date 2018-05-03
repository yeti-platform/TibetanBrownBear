import { mount } from '@vue/test-utils'

import EntityList from '@/components/Entities/EntityList'

describe('EntityList.vue', () => {
  let wrapper = mount(EntityList, {propsData: {type: 'malware'}})

  it('the New button should match the type', () => {
    expect(wrapper.vm.$el.querySelector('.btn-toolbar .btn-outline-secondary').textContent)
      .toContain('New malware')
  })
})
