import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ApixonAIMV from '../ApixonAIMV.vue'

describe('ApixonAIMV', () => {
  it('renders without crashing', () => {
    const wrapper = mount(ApixonAIMV, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    const wrapper = mount(ApixonAIMV)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 analog channel items', () => {
    const wrapper = mount(ApixonAIMV)
    const items = wrapper.findAll('.ai-item')
    expect(items).toHaveLength(8)
  })

  it('renders 12 output items', () => {
    const wrapper = mount(ApixonAIMV)
    const outputs = wrapper.findAll('.io-item.output')
    expect(outputs).toHaveLength(12)
  })

  it('renders a mV readout for each analog channel', () => {
    const wrapper = mount(ApixonAIMV)
    expect(wrapper.findAll('.ai-mv')).toHaveLength(8)
    expect(wrapper.find('.ai-mv').text()).toBe('0 mV')
  })

  it('shows a dash for the scaled value while no value is known', () => {
    const wrapper = mount(ApixonAIMV)
    expect(wrapper.findAll('.ai-cal')).toHaveLength(8)
    expect(wrapper.find('.ai-cal').text()).toBe('Wert: –')
  })
})
