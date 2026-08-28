import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ApixonPWM from '../ApixonPWM.vue'

describe('ApixonPWM', () => {
  it('renders without crashing', () => {
    const wrapper = mount(ApixonPWM, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    const wrapper = mount(ApixonPWM)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 input items', () => {
    const wrapper = mount(ApixonPWM)
    const inputs = wrapper.findAll('.io-item')
    expect(inputs).toHaveLength(8)
  })

  it('renders 12 PWM output sliders', () => {
    const wrapper = mount(ApixonPWM)
    const sliders = wrapper.findAll('input[type="range"]')
    expect(sliders).toHaveLength(12)
  })

  it('renders 12 PWM numeric fields', () => {
    const wrapper = mount(ApixonPWM)
    const numbers = wrapper.findAll('.pwm-number')
    expect(numbers).toHaveLength(12)
  })
})
