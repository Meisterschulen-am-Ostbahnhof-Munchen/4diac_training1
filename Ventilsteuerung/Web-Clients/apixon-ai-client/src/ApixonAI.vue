<template>
  <div class="app">
    <header>
      <h1>APIXON Node 20 — AI Test</h1>
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
      <div class="scope-header">
        <h2>Analog-Eingänge (Rohwert 0-4095 / 0-100 %)</h2>
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
      <div class="ai-grid">
        <div v-for="n in 8" :key="'AI' + n" class="ai-item">
          <span class="ai-label">AI{{ n }}</span>
          <span class="ai-raw">{{ raw[n - 1] }}</span>
          <span class="ai-percent">{{ percent[n - 1].toFixed(1) }} %</span>
          <div class="ai-bar-track">
            <div class="ai-bar-fill" :style="{ width: percent[n - 1] + '%' }"></div>
          </div>
          <canvas
            class="ai-scope"
            :ref="(el) => setScopeRef(el as HTMLCanvasElement | null, n - 1)"
            width="240"
            height="60"
          ></canvas>
          <span class="ai-scope-info">
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
/* Rohwert 0-4095 (DWORD, logiBUS_AI_IDA.IN unskaliert) */
const raw = ref<number[]>(new Array(8).fill(0))
/* Prozent 0.0-100.0 (REAL), linear raw/4095*100, keine physikalische Kalibrierung */
const percent = ref<number[]>(new Array(8).fill(0))
const outputs = ref<boolean[]>(new Array(12).fill(false))
const tick = ref<number | string>('–')
const tickPulse = ref(false)

/* Oszilloskop-Ansicht pro Kanal: rollierendes Liniendiagramm des Prozentwerts,
 * um live zu sehen/messen, wie sich logiBUS_AI_ID's Poll-Parameter (TimeDelta/
 * TimeRateLimit/AnalogInput_hysteresis) auf das dargestellte Signal auswirken
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
  raw.value.fill(0)
  percent.value.fill(0)
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

    /* Monitor all analog raw values AI_I1_RAW-AI_I8_RAW (DWORD 0-4095, read-only) */
    const rawItems = Array.from({ length: 8 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=AI_I${i + 1}_RAW`),
      attributeId: AttributeIds.Value,
    }))
    const rawGroup = await subscription.monitorItemsP(
      rawItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    rawGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      raw.value[index] = Number(dataValue.value?.value ?? 0)
    })

    /* Monitor all analog percent values AI_I1_PERCENT-AI_I8_PERCENT (REAL 0.0-100.0, read-only) */
    const percentItems = Array.from({ length: 8 }, (_, i) => ({
      nodeId: coerceNodeId(`ns=1;s=AI_I${i + 1}_PERCENT`),
      attributeId: AttributeIds.Value,
    }))
    const percentGroup = await subscription.monitorItemsP(
      percentItems,
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    percentGroup.on('changed', (_item: any, dataValue: any, index: number) => {
      const v = Number(dataValue.value?.value ?? 0)
      percent.value[index] = v
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
  raw.value.fill(0)
  percent.value.fill(0)
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

/* Analog-Eingaenge: read-only Rohwert + Prozent + kleiner Bargraph je Kanal,
 * kein Slider/Input - nur Anzeige (Kalibrierung folgt spaeter als eigene UI). */
.ai-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}

.ai-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  background: #0d0d1a;
  user-select: none;
}

.ai-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #aaa;
}

.ai-raw {
  font-size: 1.1rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: #fff;
}

.ai-percent {
  font-size: 0.85rem;
  font-variant-numeric: tabular-nums;
  color: #4caf50;
}

.ai-bar-track {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: #2a2a3e;
  border: 1px solid #444;
  overflow: hidden;
}

.ai-bar-fill {
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

.ai-scope {
  width: 100%;
  height: 60px;
  border-radius: 4px;
  border: 1px solid #2a2a3e;
  display: block;
}

.ai-scope-info {
  font-size: 0.65rem;
  color: #777;
  font-variant-numeric: tabular-nums;
}
</style>
