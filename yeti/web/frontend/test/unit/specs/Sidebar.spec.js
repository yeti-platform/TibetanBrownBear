import Vue from 'vue'
import Sidebar from '@/components/scaffolding/Sidebar'

describe('Sidebar.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(Sidebar)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('span').textContent)
      .toEqual('Intelligence')
  })
})
