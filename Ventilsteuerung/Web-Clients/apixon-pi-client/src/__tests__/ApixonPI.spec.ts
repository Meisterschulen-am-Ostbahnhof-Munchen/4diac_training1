import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ApixonPI from '../ApixonPI.vue'

describe('ApixonPI', () => {
  it('renders without crashing', () => {
    const wrapper = mount(ApixonPI, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    const wrapper = mount(ApixonPI)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 pulse channel items', () => {
    const wrapper = mount(ApixonPI)
    const items = wrapper.findAll('.pi-item')
    expect(items).toHaveLength(8)
  })

  it('renders 12 output items', () => {
    const wrapper = mount(ApixonPI)
    const outputs = wrapper.findAll('.io-item.output')
    expect(outputs).toHaveLength(12)
  })

  it('renders count and frequency readouts for each pulse channel', () => {
    const wrapper = mount(ApixonPI)
    expect(wrapper.findAll('.pi-count')).toHaveLength(8)
    expect(wrapper.findAll('.pi-freq')).toHaveLength(8)
  })
})
