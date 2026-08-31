import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ApixonAICalibrate from '../ApixonAICalibrate.vue'

describe('ApixonAICalibrate', () => {
  it('renders without crashing', () => {
    const wrapper = mount(ApixonAICalibrate, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    const wrapper = mount(ApixonAICalibrate)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 analog channel items', () => {
    const wrapper = mount(ApixonAICalibrate)
    const items = wrapper.findAll('.ai-item')
    expect(items).toHaveLength(8)
  })

  it('renders 12 output items', () => {
    const wrapper = mount(ApixonAICalibrate)
    const outputs = wrapper.findAll('.io-item.output')
    expect(outputs).toHaveLength(12)
  })

  it('renders raw and calibrated readouts for each analog channel', () => {
    const wrapper = mount(ApixonAICalibrate)
    expect(wrapper.findAll('.ai-raw')).toHaveLength(8)
    expect(wrapper.findAll('.ai-cal')).toHaveLength(8)
  })

  it('documents that calibration is VT-only, not remotely triggerable', () => {
    const wrapper = mount(ApixonAICalibrate)
    expect(wrapper.find('.calib-note').text()).toContain('VT-Bildschirm')
  })
})
