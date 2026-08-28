<template>
  <div class="app">
    <header>
      <h1>APIXON Node 20 — PWM Test</h1>
      <div class="connection">
        <span class="dot" :class="statusClass"></span>
        <span v-if="connected" class="tick-badge" :class="{ pulse: tickPulse }">{{ tick }}</span>
        <span>{{ status }}</span>
        <input v-model="endpointUrl" class="url-input" :disabled="connected" />
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
      <h2>PWM-Ausgänge (0-100 %)</h2>
      <div class="pwm-grid">
        <div v-for="n in 12" :key="'Q' + n" class="pwm-item">
          <span class="pwm-label">Q{{ n }}</span>
          <input
            type="range"
            min="0"
            max="100"
            step="0.1"
            v-model.number="outputs[n - 1]"
            @input="writeOutputThrottled(n)"
            @change="writeOutput(n)"
          />
          <input
            type="number"
            min="0"
            max="100"
            step="0.1"
            class="pwm-number"
            v-model.number="outputs[n - 1]"
            @change="writeOutput(n)"
          />
          <button
            class="pwm-switch"
            :class="{ on: channelSwitches[n - 1] }"
            @click="writeSwitch(n)"
            :title="channelSwitches[n - 1] ? 'Kanal aktiv (klicken zum Deaktivieren)' : 'Kanal inaktiv (klicken zum Aktivieren)'"
          >
            <span class="pwm-switch-knob"></span>
          </button>
          <div class="led led-small" :class="{ on: channelStatus[n - 1] }" title="Kanal-Status (QO)"></div>
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
const inputs = ref<boolean[]>(Array(8).fill(false))
/* Prozent 0.0-100.0 (REAL), nicht Bool wie beim DIDO-Beispiel */
const outputs = ref<number[]>(Array(12).fill(0))
/* Kanal-Ein/Aus (BOOL), echo des Kanal-Schalters (E_T_FF_SWITCH.Q) */
const channelSwitches = ref<boolean[]>(Array(12).fill(false))
/* Kanal-Status (BOOL), logiBUS_QD_PWM.QO, nur lesend */
const channelStatus = ref<boolean[]>(Array(12).fill(false))
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
  outputs.value.fill(0)
  channelSwitches.value.fill(false)
  channelStatus.value.fill(false)
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

    /* Monitor all inputs I1-I8 (unveraendert, wie im DIDO-Beispiel) */
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

    /* Monitor all PWM outputs Q1-Q12 (Prozent REAL, reflect actual hardware state) */
    const outputItems = Array.from({ length: 12 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=PWM_Q${String(i + 1).padStart(2, '0')}`),
      attributeId: AttributeIds.Value,
    }))
    const outputGroup = await subscription.monitorItemsP(
      outputItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    outputGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      outputs.value[index] = Number(dataValue.value?.value ?? 0)
    })

    /* Monitor all channel switches Q1-Q12 (BOOL, echo of the actual enable state) */
    const switchItems = Array.from({ length: 12 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=PWM_Q${String(i + 1).padStart(2, '0')}_SWITCH`),
      attributeId: AttributeIds.Value,
    }))
    const switchGroup = await subscription.monitorItemsP(
      switchItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    switchGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      channelSwitches.value[index] = !!dataValue.value?.value
    })

    /* Monitor all channel status LEDs Q1-Q12 (BOOL, logiBUS_QD_PWM.QO, read-only) */
    const statusItems = Array.from({ length: 12 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=PWM_Q${String(i + 1).padStart(2, '0')}_STATUS`),
      attributeId: AttributeIds.Value,
    }))
    const statusGroup = await subscription.monitorItemsP(
      statusItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    statusGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      channelStatus.value[index] = !!dataValue.value?.value
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

/* Leading-edge throttle while dragging the slider, so the PWM value updates live
 * without flooding the OPC-UA write channel; @change still fires one final,
 * unthrottled write on mouse-up to guarantee the committed value is sent. */
const THROTTLE_MS = 150
const throttleTimers: (ReturnType<typeof setTimeout> | null)[] = Array(12).fill(null)

function writeOutputThrottled(n: number) {
  if (throttleTimers[n - 1]) return
  writeOutput(n)
  throttleTimers[n - 1] = setTimeout(() => {
    throttleTimers[n - 1] = null
  }, THROTTLE_MS)
}

async function writeOutput(n: number) {
  if (!session) return
  const clamped = Math.min(100, Math.max(0, outputs.value[n - 1]))
  outputs.value[n - 1] = clamped
  try {
    const wv = new WriteValue({
      nodeId: coerceNodeId(`ns=1;s=PWM_Q${String(n).padStart(2, '0')}`),
      attributeId: AttributeIds.Value,
      /* IEC 61499 REAL ist 32-bit -> DataType.Float, bestaetigt in FORTEs
       * eigenem Quellcode (opcua_helper.cpp: CIEC_REAL -> UA_TYPES_FLOAT). */
      value: new DataValue({ value: new Variant({ dataType: DataType.Float, value: clamped }) }),
    })
    await session.writeP([wv])
  } catch (err) {
    console.error(`PWM_Q${n} write failed:`, err)
  }
}

/* Der Kanal-Schalter im SUB ist ein Toggle-FlipFlop (E_T_FF): jeder Schreib-
 * zugriff auf den SWITCH-Knoten togglet den Kanal, unabhaengig vom
 * uebertragenen Wert selbst (genau wie ein physischer Tastendruck). Der
 * geschriebene Wert dient nur der optischen Konsistenz mit dem erwarteten
 * neuen Zustand, nicht als tatsaechlich ausgewerteter Soll-Zustand. */
async function writeSwitch(n: number) {
  if (!session) return
  const next = !channelSwitches.value[n - 1]
  try {
    const wv = new WriteValue({
      nodeId: coerceNodeId(`ns=1;s=PWM_Q${String(n).padStart(2, '0')}_SWITCH`),
      attributeId: AttributeIds.Value,
      value: new DataValue({ value: new Variant({ dataType: DataType.Boolean, value: next }) }),
    })
    await session.writeP([wv])
  } catch (err) {
    console.error(`PWM_Q${n}_SWITCH write failed:`, err)
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
  outputs.value.fill(0)
  channelSwitches.value.fill(false)
  channelStatus.value.fill(false)
}

onUnmounted(() => disconnect())
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

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

.pwm-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.pwm-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  border-radius: 8px;
  background: #0d0d1a;
}

.pwm-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #aaa;
  width: 2rem;
  flex-shrink: 0;
}

.pwm-item input[type="range"] {
  flex: 1;
  min-width: 0;
  accent-color: #4caf50;
}

.pwm-number {
  width: 4.2rem;
  padding: 0.2rem 0.3rem;
  border-radius: 4px;
  border: 1px solid #444;
  background: #1a1a2e;
  color: #e0e0e0;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.pwm-switch {
  position: relative;
  width: 34px;
  height: 18px;
  flex-shrink: 0;
  padding: 0;
  border-radius: 9px;
  border: 1px solid #444;
  background: #2a2a3e;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.pwm-switch.on {
  background: #4caf50;
  border-color: #81c784;
}
.pwm-switch-knob {
  position: absolute;
  top: 1px;
  left: 1px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #e0e0e0;
  transition: transform 0.15s;
}
.pwm-switch.on .pwm-switch-knob {
  transform: translateX(16px);
}

.led-small {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
</style>
