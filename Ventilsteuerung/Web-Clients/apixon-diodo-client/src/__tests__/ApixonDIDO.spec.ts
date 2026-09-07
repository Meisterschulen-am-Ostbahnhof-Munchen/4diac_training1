import { afterEach, describe, expect, it, vi } from 'vitest'
import type { VueWrapper } from '@vue/test-utils'
import { mount } from '@vue/test-utils'
import { OPCUAClient } from '@wsopcua/wsopcua'
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
    // `new` requires a real function - an arrow function can't be a constructor.
    OPCUAClient: vi.fn().mockImplementation(function () {
      return new MockOPCUAClient()
    }),
  }
})

let wrapper: VueWrapper | undefined

afterEach(() => {
  wrapper?.unmount()
  wrapper = undefined
  vi.mocked(OPCUAClient).mockClear()
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

  it('disables the button while the automatic connection attempt is pending, and clicking it does not start a second client', async () => {
    const connectP = vi.fn(() => new Promise(() => {})) // never settles within the test
    vi.mocked(OPCUAClient).mockImplementationOnce(function () {
      return {
        connectP,
        disconnectP: vi.fn().mockResolvedValue(undefined),
        on: vi.fn(),
        off: vi.fn(),
      } as any
    })

    wrapper = mount(ApixonDIDO)
    await wrapper.vm.$nextTick()

    const button = wrapper.find('button')
    expect(button.attributes('disabled')).toBeDefined()

    await button.trigger('click')
    expect(vi.mocked(OPCUAClient)).toHaveBeenCalledTimes(1)
    expect(connectP).toHaveBeenCalledTimes(1)
  })

  it('closes a stale connection attempt instead of resurrecting it after unmount', async () => {
    let resolveConnectP: () => void = () => {}
    const connectP = vi.fn(
      () =>
        new Promise<void>((resolve) => {
          resolveConnectP = resolve
        })
    )
    let resolveCreateSessionP: (session: unknown) => void = () => {}
    const createSessionP = vi.fn(
      () =>
        new Promise((resolve) => {
          resolveCreateSessionP = resolve
        })
    )
    const disconnectP = vi.fn().mockResolvedValue(undefined)
    vi.mocked(OPCUAClient).mockImplementationOnce(function () {
      return {
        connectP,
        createSessionP,
        disconnectP,
        on: vi.fn(),
        off: vi.fn(),
      } as any
    })

    wrapper = mount(ApixonDIDO)
    await wrapper.vm.$nextTick()

    // Let connectP resolve so connect() proceeds to the (still pending) createSessionP.
    resolveConnectP()
    await Promise.resolve()
    await Promise.resolve()
    expect(createSessionP).toHaveBeenCalledTimes(1)

    // Unmount while createSessionP is still pending - this is the race from the review.
    wrapper.unmount()
    wrapper = undefined

    // Now let the stale attempt's createSessionP resolve.
    resolveCreateSessionP({})
    await Promise.resolve()
    await Promise.resolve()
    await Promise.resolve()

    // The stale attempt must close what it opened instead of publishing it.
    expect(disconnectP).toHaveBeenCalledTimes(1)
  })
})
