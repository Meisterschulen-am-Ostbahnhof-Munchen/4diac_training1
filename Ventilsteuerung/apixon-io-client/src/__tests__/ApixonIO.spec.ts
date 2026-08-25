import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ApixonIO from '../ApixonIO.vue'

describe('ApixonIO', () => {
  it('renders without crashing', () => {
    const wrapper = mount(ApixonIO, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    const wrapper = mount(ApixonIO)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 input items', () => {
    const wrapper = mount(ApixonIO)
    const inputs = wrapper.findAll('.io-item:not(.output)')
    expect(inputs).toHaveLength(8)
  })

  it('renders 12 output items', () => {
    const wrapper = mount(ApixonIO)
    const outputs = wrapper.findAll('.io-item.output')
    expect(outputs).toHaveLength(12)
  })
})
