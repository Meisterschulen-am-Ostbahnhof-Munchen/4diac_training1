<template>
  <div class="app">
    <header>
      <h1>APIXON Node 20 — PI Test</h1>
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
      <div class="scope-header">
        <h2>Puls-Eingänge (Zähler / Frequenz 0-100 Hz)</h2>
        <label class="scope-window-label">
          Oszi-Zeitfenster:
          <select v-model.number="scopeWindowSec">
            <option :value="5">5 s</option>
            <option :value="10">10 s</option>
            <option :value="30">30 s</option>
            <option :value="60">60 s</option>
          </select>
        </label>
      </div>
      <div class="pi-grid">
        <div v-for="n in 8" :key="'PI' + n" class="pi-item">
          <span class="pi-label">PI{{ n }}</span>
          <span class="pi-count">{{ count[n - 1] }}</span>
          <span class="pi-freq">{{ freq[n - 1].toFixed(1) }} Hz</span>
          <div class="pi-bar-track">
            <div class="pi-bar-fill" :style="{ width: freq[n - 1] + '%' }"></div>
          </div>
          <canvas
            class="pi-scope"
            :ref="(el) => setScopeRef(el as HTMLCanvasElement | null, n - 1)"
            width="240"
            height="60"
          ></canvas>
          <span class="pi-scope-info">
            Δt letzte Samples: {{ sampleIntervalMs[n - 1] !== null ? sampleIntervalMs[n - 1] + ' ms' : '–' }}
          </span>
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
/* Zaehlerstand (DWORD, logiBUS_PI_IDA.IN unskaliert, monoton wachsend) */
const count = ref<number[]>(Array(8).fill(0))
/* Frequenz 0.0-100.0 Hz (REAL), FT_DERIV(K=1.0) ueber den Zaehler */
const freq = ref<number[]>(Array(8).fill(0))
const outputs = ref<boolean[]>(Array(12).fill(false))
const tick = ref<number | string>('–')
const tickPulse = ref(false)

/* Oszilloskop-Ansicht pro Kanal: rollierendes Liniendiagramm der Frequenz,
 * um live zu sehen/messen, wie sich logiBUS_PI_ID's Poll-Parameter (TimeDelta/
 * TimeRateLimit/ImpulseDelta) auf das dargestellte Signal auswirken
 * (Abtastrate/Aliasing) - im Gegensatz zu ISOBUS-VT, das keine Zeitachsen-
 * Grafik kennt. Reiner Web-Client-Zusatz, kein Einfluss auf FORTE/SUB. */
interface ScopeSample { t: number; v: number }
const scopeWindowSec = ref(10)
const scopeBuffers: ScopeSample[][] = Array.from({ length: 8 }, () => [])
const scopeCanvases: (HTMLCanvasElement | null)[] = Array(8).fill(null)
const sampleIntervalMs = ref<(number | null)[]>(Array(8).fill(null))
let scopeRafId: number | null = null
/* Puffer laenger als das aktuell gewaehlte Fenster behalten, damit ein
 * groesseres Zeitfenster rueckwirkend mehr Historie zeigt, ohne neu zu
 * subscriben. */
const SCOPE_BUFFER_MS = 120_000

function setScopeRef(el: HTMLCanvasElement | null, index: number) {
  scopeCanvases[index] = el
}

function pushScopeSample(index: number, value: number) {
  const now = performance.now()
  const buf = scopeBuffers[index]
  if (buf.length > 0) {
    sampleIntervalMs.value[index] = Math.round(now - buf[buf.length - 1].t)
  }
  buf.push({ t: now, v: value })
  const cutoff = now - SCOPE_BUFFER_MS
  while (buf.length > 0 && buf[0].t < cutoff) buf.shift()
}

function drawScopes() {
  const now = performance.now()
  const windowMs = scopeWindowSec.value * 1000
  for (let i = 0; i < 8; i++) {
    const canvas = scopeCanvases[i]
    if (!canvas) continue
    const ctx = canvas.getContext('2d')
    if (!ctx) continue
    const w = canvas.width
    const h = canvas.height

    ctx.fillStyle = '#0d0d1a'
    ctx.fillRect(0, 0, w, h)

    ctx.strokeStyle = '#2a2a3e'
    ctx.lineWidth = 1
    for (const frac of [0, 0.25, 0.5, 0.75, 1]) {
      const y = Math.round(h - frac * h) + 0.5
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(w, y)
      ctx.stroke()
    }

    const visible = scopeBuffers[i].filter((s) => s.t >= now - windowMs)
    if (visible.length > 0) {
      ctx.strokeStyle = '#4caf50'
      ctx.lineWidth = 1.5
      ctx.beginPath()
      visible.forEach((s, idx) => {
        const x = w - ((now - s.t) / windowMs) * w
        const y = h - (s.v / 100) * h
        if (idx === 0) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      })
      /* letzten bekannten Wert bis "jetzt" durchziehen (Step-Hold) - zeigt
       * ehrlich, wie "alt" der letzte Sample gerade ist, statt eine
       * Interpolation vorzutaeuschen, die es nicht gab. */
      const last = visible[visible.length - 1]
      ctx.lineTo(w, h - (last.v / 100) * h)
      ctx.stroke()
    }
  }
  scopeRafId = requestAnimationFrame(drawScopes)
}

function resetScopes() {
  scopeBuffers.forEach((b) => (b.length = 0))
  sampleIntervalMs.value.fill(null)
}

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
  count.value.fill(0)
  freq.value.fill(0)
  outputs.value.fill(false)
  tick.value = '–'
  if (scopeRafId !== null) {
    cancelAnimationFrame(scopeRafId)
    scopeRafId = null
  }
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

    /* Monitor all pulse counters PI_I1_COUNT-PI_I8_COUNT (DWORD, roh, monoton wachsend, read-only) */
    const countItems = Array.from({ length: 8 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=PI_I${i + 1}_COUNT`),
      attributeId: AttributeIds.Value,
    }))
    const countGroup = await subscription.monitorItemsP(
      countItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    countGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      count.value[index] = Number(dataValue.value?.value ?? 0)
    })

    /* Monitor all pulse frequencies PI_I1_FREQ-PI_I8_FREQ (REAL Hz, read-only) */
    const freqItems = Array.from({ length: 8 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=PI_I${i + 1}_FREQ`),
      attributeId: AttributeIds.Value,
    }))
    const freqGroup = await subscription.monitorItemsP(
      freqItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    freqGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      const v = Number(dataValue.value?.value ?? 0)
      freq.value[index] = v
      pushScopeSample(index, v)
    })

    /* Monitor all outputs Q1-Q12 (reflect actual hardware state, unveraendert wie im DIDO-Beispiel) */
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

    resetScopes()
    if (scopeRafId === null) scopeRafId = requestAnimationFrame(drawScopes)
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
  count.value.fill(0)
  freq.value.fill(0)
  outputs.value.fill(false)
  if (scopeRafId !== null) {
    cancelAnimationFrame(scopeRafId)
    scopeRafId = null
  }
  resetScopes()
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

/* Puls-Eingaenge: read-only Zaehlerstand + Frequenz + kleiner Bargraph je Kanal,
 * kein Slider/Input - nur Anzeige. */
.pi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}

.pi-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  background: #0d0d1a;
  user-select: none;
}

.pi-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #aaa;
}

.pi-count {
  font-size: 1.1rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: #fff;
}

.pi-freq {
  font-size: 0.85rem;
  font-variant-numeric: tabular-nums;
  color: #4caf50;
}

.pi-bar-track {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: #2a2a3e;
  border: 1px solid #444;
  overflow: hidden;
}

.pi-bar-fill {
  height: 100%;
  background: #4caf50;
  transition: width 0.15s;
}

.scope-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.scope-header h2 { margin-bottom: 0; }

.scope-window-label {
  font-size: 0.8rem;
  color: #aaa;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.scope-window-label select {
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  border: 1px solid #444;
  background: #0d0d1a;
  color: #e0e0e0;
  font-size: 0.8rem;
}

.pi-scope {
  width: 100%;
  height: 60px;
  border-radius: 4px;
  border: 1px solid #2a2a3e;
  display: block;
}

.pi-scope-info {
  font-size: 0.65rem;
  color: #777;
  font-variant-numeric: tabular-nums;
}
</style>
