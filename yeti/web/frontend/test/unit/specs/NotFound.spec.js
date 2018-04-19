import Vue from 'vue'
import NotFound from '@/components/NotFound'

describe('NotFound.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(NotFound)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('p').textContent)
      .toEqual('404 - Not Found')
  })
})
