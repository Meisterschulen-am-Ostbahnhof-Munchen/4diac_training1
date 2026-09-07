import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ApixonAI from '../ApixonAI.vue'

describe('ApixonAI', () => {
  it('renders without crashing', () => {
    const wrapper = mount(ApixonAI, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    const wrapper = mount(ApixonAI)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 analog channel items', () => {
    const wrapper = mount(ApixonAI)
    const items = wrapper.findAll('.ai-item')
    expect(items).toHaveLength(8)
  })

  it('renders 12 output items', () => {
    const wrapper = mount(ApixonAI)
    const outputs = wrapper.findAll('.io-item.output')
    expect(outputs).toHaveLength(12)
  })

  it('renders raw and percent readouts for each analog channel', () => {
    const wrapper = mount(ApixonAI)
    expect(wrapper.findAll('.ai-raw')).toHaveLength(8)
    expect(wrapper.findAll('.ai-percent')).toHaveLength(8)
  })
})
