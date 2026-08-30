<template>
  <div class="app">
    <header>
      <h1>APIXON Node 20 — DIDO Test</h1>
      <div class="connection">
        <span class="dot" :class="statusClass"></span>
        <span v-if="connected" class="tick-badge" :class="{ pulse: tickPulse }">{{ tick }}</span>
        <span>{{ status }}</span>
        <label for="endpoint-url" class="sr-only">OPC-UA Endpoint-URL</label>
        <input id="endpoint-url" v-model="endpointUrl" class="url-input" :disabled="connected" />
        <button @click="connected ? disconnect() : connect()">
          {{ connected ? 'Trennen' : 'Verbinden' }}
        </button>
      </div>
    </header>

    <section>
      <h2>Eingänge</h2>
      <div class="io-grid">
        <div
          v-for="n in 8"
          :key="'I' + n"
          class="io-item"
          :class="{ active: inputs[n - 1] }"
        >
          <div class="led" :class="{ on: inputs[n - 1] }"></div>
          <span>I{{ n }}</span>
        </div>
      </div>
    </section>

    <section>
      <h2>Ausgänge</h2>
      <div class="io-grid">
        <div
          v-for="n in 12"
          :key="'Q' + n"
          class="io-item output"
          :class="{ active: outputs[n - 1] }"
          @click="toggleOutput(n)"
        >
          <div class="led" :class="{ on: outputs[n - 1] }"></div>
          <span>Q{{ n }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import {
  OPCUAClient,
  MessageSecurityMode,
  SecurityPolicy,
  ClientSubscription,
  AttributeIds,
  TimestampsToReturn,
  DataType,
  coerceNodeId,
  WriteValue,
  DataValue,
  Variant,
} from '@wsopcua/wsopcua'

const endpointUrl = ref(`ws://${window.location.hostname || 'localhost'}:4841`)
const status = ref('Getrennt')
const connected = ref(false)
const inputs = ref<boolean[]>(new Array(8).fill(false))
const outputs = ref<boolean[]>(new Array(12).fill(false))
const tick = ref<number | string>('–')
const tickPulse = ref(false)

const statusClass = computed(() => {
  if (status.value === 'Verbunden') return 'green'
  if (status.value.startsWith('Fehler')) return 'red'
  return 'yellow'
})

let client: any = null
let session: any = null

function handleLost() {
  if (!connected.value) return
  connected.value = false
  status.value = 'Fehler: Verbindung verloren'
  inputs.value.fill(false)
  outputs.value.fill(false)
  tick.value = '–'
}

async function connect() {
  status.value = 'Verbinde…'
  client = new OPCUAClient({
    securityMode: MessageSecurityMode.None,
    securityPolicy: SecurityPolicy.None,
    endpoint_must_exist: false,
    connectionStrategy: { maxRetry: 0 },
  })

  try {
    await client.connectP(endpointUrl.value)
    client.on('connection_lost', handleLost)
    client.on('close', handleLost)
    session = await client.createSessionP({})
    connected.value = true
    status.value = 'Verbunden'

    const subscription = new ClientSubscription(session, {
      requestedPublishingInterval: 100,
      requestedLifetimeCount: 100,
      requestedMaxKeepAliveCount: 2,
      maxNotificationsPerPublish: 100,
      publishingEnabled: true,
      priority: 10,
    })

    /* Monitor all inputs I1-I8 */
    const inputItems = Array.from({ length: 8 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=I${i + 1}`),
      attributeId: AttributeIds.Value,
    }))
    const inputGroup = await subscription.monitorItemsP(
      inputItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    inputGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      inputs.value[index] = !!dataValue.value?.value
    })

    /* Monitor all outputs Q1-Q12 (reflect actual hardware state) */
    const outputItems = Array.from({ length: 12 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=Q${String(i + 1).padStart(2, '0')}`),
      attributeId: AttributeIds.Value,
    }))
    const outputGroup = await subscription.monitorItemsP(
      outputItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    outputGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      outputs.value[index] = !!dataValue.value?.value
    })

    /* Monitor the heartbeat/tick counter */
    const tickGroup = await subscription.monitorItemsP(
      [{ nodeId: coerceNodeId('ns=1;s=System.Tick'), attributeId: AttributeIds.Value }],
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    tickGroup.on('changed', (_item: any, dataValue: any) => {
      tick.value = dataValue.value?.value ?? '–'
      tickPulse.value = true
      setTimeout(() => { tickPulse.value = false }, 400)
    })
  } catch (err) {
    status.value = 'Fehler: ' + (err as Error).message
    connected.value = false
  }
}

async function toggleOutput(n: number) {
  if (!session) return
  const newVal = !outputs.value[n - 1]
  try {
    const wv = new WriteValue({
      nodeId: coerceNodeId(`ns=1;s=Q${String(n).padStart(2, '0')}`),
      attributeId: AttributeIds.Value,
      value: new DataValue({ value: new Variant({ dataType: DataType.Boolean, value: newVal }) }),
    })
    await session.writeP([wv])
    /* optimistic update — subscription will confirm */
    outputs.value[n - 1] = newVal
  } catch (err) {
    console.error(`Q${n} write failed:`, err)
  }
}

async function disconnect() {
  if (client) {
    client.off('connection_lost', handleLost)
    client.off('close', handleLost)
    await client.disconnectP()
  }
  connected.value = false
  status.value = 'Getrennt'
  inputs.value.fill(false)
  outputs.value.fill(false)
}

onUnmounted(() => disconnect())
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.app {
  font-family: system-ui, sans-serif;
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem;
  background: #1a1a2e;
  min-height: 100vh;
  color: #e0e0e0;
}

header {
  margin-bottom: 1.5rem;
}

h1 {
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
  color: #fff;
}

h2 {
  font-size: 1rem;
  color: #aaa;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.connection {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot.green  { background: #4caf50; box-shadow: 0 0 6px #4caf50; }
.dot.red    { background: #f44336; }
.dot.yellow { background: #ff9800; }

.tick-badge {
  font-size: 0.75rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: #4caf50;
  min-width: 1.5rem;
  text-align: center;
  transition: opacity 0.2s;
}
.tick-badge.pulse { color: #fff; }

.url-input {
  flex: 1;
  min-width: 180px;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #444;
  background: #0d0d1a;
  color: #e0e0e0;
  font-size: 0.85rem;
}

button {
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  border: none;
  background: #3f51b5;
  color: #fff;
  cursor: pointer;
  font-size: 0.85rem;
}
button:hover { background: #5c6bc0; }

section {
  background: #16213e;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.io-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.io-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  background: #0d0d1a;
  border: 2px solid transparent;
  user-select: none;
}

.io-item.output {
  cursor: pointer;
  transition: border-color 0.1s;
}
.io-item.output:hover { border-color: #3f51b5; }
.io-item.output:active { transform: scale(0.95); }

.led {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #2a2a3e;
  border: 2px solid #444;
  transition: background 0.1s, box-shadow 0.1s;
}
.led.on {
  background: #4caf50;
  border-color: #81c784;
  box-shadow: 0 0 10px #4caf50, 0 0 20px #4caf5066;
}

span {
  font-size: 0.8rem;
  font-weight: 600;
  color: #aaa;
}
.io-item.active span { color: #fff; }
</style>
