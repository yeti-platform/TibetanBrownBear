import { mount } from '@vue/test-utils'
import Sidebar from '@/components/scaffolding/Sidebar'

describe('Sidebar.vue', () => {
  let wrapper = mount(Sidebar)

  it('should render correct contents', () => {
    expect(wrapper.vm.$el.querySelector('span').textContent)
      .toEqual('Intelligence')
  })
})
