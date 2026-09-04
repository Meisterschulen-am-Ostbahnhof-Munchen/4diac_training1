import { afterEach, describe, expect, it, vi } from 'vitest'
import type { VueWrapper } from '@vue/test-utils'
import { mount } from '@vue/test-utils'
import ApixonDIDO from '../ApixonDIDO.vue'

/* Auto-connect on mount would otherwise try a real WebSocket connection in
 * every test, leaking async work past the test's own teardown. */
vi.mock('@wsopcua/wsopcua', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@wsopcua/wsopcua')>()
  class MockOPCUAClient {
    connectP = vi.fn().mockRejectedValue(new Error('no server in tests'))
    disconnectP = vi.fn().mockResolvedValue(undefined)
    on = vi.fn()
    off = vi.fn()
  }
  return {
    ...actual,
    OPCUAClient: MockOPCUAClient,
  }
})

let wrapper: VueWrapper | undefined

afterEach(() => {
  wrapper?.unmount()
  wrapper = undefined
})

describe('ApixonDIDO', () => {
  it('renders without crashing', () => {
    wrapper = mount(ApixonDIDO, {
      global: {
        stubs: { teleport: true },
      },
    })
    expect(wrapper.find('h1').text()).toContain('APIXON')
  })

  it('shows connect button when disconnected', () => {
    wrapper = mount(ApixonDIDO)
    const button = wrapper.find('button')
    expect(button.text()).toBe('Verbinden')
  })

  it('renders 8 input items', () => {
    wrapper = mount(ApixonDIDO)
    const inputs = wrapper.findAll('.io-item:not(.output)')
    expect(inputs).toHaveLength(8)
  })

  it('renders 12 output items', () => {
    wrapper = mount(ApixonDIDO)
    const outputs = wrapper.findAll('.io-item.output')
    expect(outputs).toHaveLength(12)
  })
})
