import { shallow } from '@vue/test-utils'

import NotFound from '@/components/NotFound'

describe('NotFound.vue', () => {
  let wrapper = shallow(NotFound)

  it('should render correct contents', () => {
    expect(wrapper.vm.$el.querySelector('p').textContent)
      .toEqual('404 - Not Found')
  })
})
