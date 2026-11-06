<template>
  <div class="app">
    <header>
      <h1>APIXON Node 20 — Servo Q2 an Slider AI3 (2P-kalibriert)</h1>
      <div class="connection">
        <span class="dot" :class="statusClass"></span>
        <span>{{ status }}</span>
        <label for="endpoint-url" class="sr-only">OPC-UA Endpoint-URL</label>
        <input id="endpoint-url" v-model="endpointUrl" class="url-input" :disabled="connected" />
        <button @click="connected ? disconnect() : connect()">
          {{ connected ? 'Trennen' : 'Verbinden' }}
        </button>
      </div>
    </header>

    <p class="note">
      Servo an <strong>Output_Q2</strong> folgt dem Slider <strong>AI3</strong>
      (2-Punkt-Kalibrierung, <code>logiBUS_AI_Calibrate_2P_OPC</code>). Der Slider hält seine
      Position, es gibt keine Mittelstellung. Der kalibrierte Wert ist direkt der Servo-Winkel in
      Grad (0–180°, außerhalb wird begrenzt).
      Kalibrieren: Referenzwerte (z.&nbsp;B. 0 / 180) übernehmen, Slider an den unteren Anschlag
      und <strong>CO</strong> drücken, dann an den oberen Anschlag und <strong>CS</strong>
      drücken. Beide Punkte werden gespeichert (INI, überlebt Neustart).
    </p>

    <section>
      <div class="servo-card">
        <div class="angle-readout">
          <span class="angle-value">{{ liveAngle.toFixed(0) }}°</span>
          <span class="angle-label">Servo-Winkel (Echo)</span>
        </div>
        <div class="angle-track">
          <div class="angle-fill" :style="{ width: (Math.min(Math.max(liveAngle, 0), 180) / 180 * 100) + '%' }"></div>
        </div>
        <div class="slider-scale">
          <span>0°</span>
          <span>90°</span>
          <span>180°</span>
        </div>
      </div>
    </section>

    <section>
      <h2>AI3 — Rohwert / kalibriert</h2>
      <div class="ai-row">
        <div class="ai-cell">
          <span class="ai-caption">Rohwert</span>
          <span class="ai-raw">{{ raw }}</span>
        </div>
        <div class="ai-cell">
          <span class="ai-caption">kalibriert</span>
          <span class="ai-cal">{{ cal.toFixed(1) }}</span>
        </div>
      </div>
      <div class="ai-bar-track">
        <div class="ai-bar-fill" :style="{ width: (raw / 4095 * 100) + '%' }"></div>
      </div>
    </section>

    <section>
      <h2>Kalibrierung AI3</h2>
      <div class="calib-grid">
        <div v-for="p in points" :key="p.key" class="calib-col">
          <span class="calib-title">{{ p.title }}</span>
          <label :for="`ref-${p.key}`" class="ref-label">{{ p.ref }}_REF [°]</label>
          <div class="ref-row">
            <input :id="`ref-${p.key}`" v-model="refInput[p.idx]" class="ref-input" :disabled="!connected" />
            <button class="small-btn" :disabled="!connected" @click="writeRef(p.idx)">Übernehmen</button>
          </div>
          <span class="ref-live">aktuell: {{ refLive[p.idx].toFixed(1) }}°</span>
          <button class="calib-btn" :disabled="!connected" @click="triggerCalibrate(p.key)">
            {{ p.key }} setzen
          </button>
          <span class="ref-live">Rohwert am Punkt: {{ pointRaw[p.idx] }}</span>
        </div>
      </div>
      <button class="defaults-btn" :disabled="!connected" @click="writeDefaultRefs">
        Referenzwerte 0 / 180° übernehmen
      </button>
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
  makeBrowsePath,
  CallMethodRequest,
} from '@wsopcua/wsopcua'

/* OPC-UA-Knoten siehe test_AX/Meins/Servo_AI3_Calibrate_2P_OPC/SubStrings.gcf (Prefix SAI3_,
 * Ordner /Objects/ServoAI3) - bewusst eigene Namen, damit es nicht mit den AIC_I3_*-Knoten
 * des AI-Calibrate-2P-Testers kollidiert. */
type Point = 'CO' | 'CS'
const points: { key: Point; idx: number; title: string; ref: string }[] = [
  { key: 'CO', idx: 0, title: 'Nullpunkt (CO)', ref: 'ZERO' },
  { key: 'CS', idx: 1, title: 'Spanne (CS)', ref: 'SPAN' },
]

const endpointUrl = ref(`ws://${window.location.hostname || 'logibus.local'}:4841`)
const status = ref('Getrennt')
const connected = ref(false)

const liveAngle = ref(0)
const raw = ref(0)
const cal = ref(0)
/* Live ZERO_REF/SPAN_REF (Echo-Knoten, den der Baustein tatsaechlich verwendet) */
const refLive = ref<number[]>([0, 0])
/* Eingabefelder, vorbelegt mit dem Servo-Bereich */
const refInput = ref<string[]>(['0', '180'])
/* Rohwert an den 2 Kalibrierpunkten (Diagnose) */
const pointRaw = ref<number[]>([0, 0])

const statusClass = computed(() => {
  if (status.value === 'Verbunden') return 'green'
  if (status.value.startsWith('Fehler')) return 'red'
  return 'yellow'
})

let client: any = null
let session: any = null

function resetValues() {
  liveAngle.value = 0
  raw.value = 0
  cal.value = 0
  refLive.value = [0, 0]
  pointRaw.value = [0, 0]
}

function disconnectQuietly(c: any) {
  if (!c) return
  try {
    c.off('connection_lost', handleLost)
    c.off('close', handleLost)
  } catch {
    /* ignore */
  }
  c.disconnectP().catch(() => {})
}

function handleLost() {
  if (!connected.value) return
  connected.value = false
  status.value = 'Fehler: Verbindung verloren'
  resetValues()
  const lostClient = client
  session = null
  client = null
  disconnectQuietly(lostClient)
}

async function monitor(subscription: any, nodeIds: string[], onChange: (index: number, v: any) => void) {
  const group = await subscription.monitorItemsP(
    nodeIds.map((id) => ({ nodeId: coerceNodeId(`ns=1;s=${id}`), attributeId: AttributeIds.Value })),
    { samplingInterval: 100, discardOldest: true, queueSize: 2 },
    TimestampsToReturn.Neither
  )
  group.on('changed', (_item: any, dataValue: any, index: number) => onChange(index ?? 0, dataValue.value?.value))
}

async function connect() {
  status.value = 'Verbinde…'
  /* Erst lokal aufbauen, erst nach Erfolg in die Modul-Refs committen (wie apixon-servo-client). */
  const newClient = new OPCUAClient({
    securityMode: MessageSecurityMode.None,
    securityPolicy: SecurityPolicy.None,
    endpoint_must_exist: false,
    connectionStrategy: { maxRetry: 0 },
  })

  try {
    await newClient.connectP(endpointUrl.value)
    const newSession = await newClient.createSessionP({})

    const subscription = new ClientSubscription(newSession, {
      requestedPublishingInterval: 100,
      requestedLifetimeCount: 100,
      requestedMaxKeepAliveCount: 2,
      maxNotificationsPerPublish: 20,
      publishingEnabled: true,
      priority: 10,
    })

    await monitor(subscription, ['SAI3_ANGLE'], (_i, v) => { liveAngle.value = Number(v ?? 0) })
    await monitor(subscription, ['SAI3_RAW'], (_i, v) => { raw.value = Number(v ?? 0) })
    await monitor(subscription, ['SAI3_CAL'], (_i, v) => { cal.value = Number(v ?? 0) })
    await monitor(subscription, ['SAI3_ZEROREF', 'SAI3_SPANREF'], (i, v) => {
      refLive.value[i] = Number(v ?? 0)
    })
    await monitor(subscription, ['SAI3_ZERO_RAW', 'SAI3_SPAN_RAW'], (i, v) => {
      pointRaw.value[i] = Number(v ?? 0)
    })

    client = newClient
    session = newSession
    client.on('connection_lost', handleLost)
    client.on('close', handleLost)
    connected.value = true
    status.value = 'Verbunden'
  } catch (err) {
    status.value = 'Fehler: ' + (err as Error).message
    connected.value = false
    disconnectQuietly(newClient)
  }
}

/* CO/CS: argumentlose OPC-UA-Methode (SERVER_0 im Baustein), Pfad per
 * TranslateBrowsePath aufgeloest - gleiches Muster wie apixon-ai-calibrate-2p-client. */
async function triggerCalibrate(which: Point) {
  if (!session) return
  try {
    const path = `/1:ServoAI3/1:${which}Method`
    const parentPath = '/1:ServoAI3'
    const [methodResult, parentResult] = await Promise.all([
      session.translateBrowsePathP(makeBrowsePath('ObjectsFolder', path)),
      session.translateBrowsePathP(makeBrowsePath('ObjectsFolder', parentPath)),
    ])
    const methodId = methodResult.targets?.[0]?.targetId
    const objectId = parentResult.targets?.[0]?.targetId
    if (!methodId || !objectId) {
      console.error(`AI3 ${which}: Methode nicht gefunden (${path})`)
      return
    }
    await session.callP([new CallMethodRequest({ objectId, methodId, inputArguments: [] })])
  } catch (err) {
    console.error(`AI3 ${which} method call failed:`, err)
  }
}

const REF_NODES = ['SAI3_ZEROREF_EXT', 'SAI3_SPANREF_EXT']

/* Schreibt einen Referenzwert auf den _EXT-Override-Knoten (last-writer-wins im Baustein). */
async function writeRefValue(idx: number, val: number) {
  if (!session) return
  const wv = new WriteValue({
    nodeId: coerceNodeId(`ns=1;s=${REF_NODES[idx]}`),
    attributeId: AttributeIds.Value,
    value: new DataValue({ value: new Variant({ dataType: DataType.Float, value: val }) }),
  })
  await session.writeP([wv])
}

async function writeRef(idx: number) {
  const text = refInput.value[idx].trim().replace(',', '.')
  if (text === '') return
  const val = Number(text)
  if (!Number.isFinite(val) || val < 0 || val > 180) {
    console.error(`AI3 Referenzwert ${text} ausserhalb 0..180°`)
    return
  }
  try {
    await writeRefValue(idx, val)
  } catch (err) {
    console.error('AI3 Referenzwert schreiben fehlgeschlagen:', err)
  }
}

async function writeDefaultRefs() {
  refInput.value = ['0', '180']
  for (const p of points) await writeRef(p.idx)
}

async function disconnect() {
  if (client) {
    client.off('connection_lost', handleLost)
    client.off('close', handleLost)
    await client.disconnectP()
  }
  connected.value = false
  status.value = 'Getrennt'
  resetValues()
  session = null
  client = null
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
  max-width: 520px;
  margin: 0 auto;
  padding: 1rem;
  background: #1a1a2e;
  min-height: 100vh;
  color: #e0e0e0;
}

header { margin-bottom: 0.75rem; }

h1 {
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
  color: #fff;
}

h2 {
  font-size: 0.85rem;
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
button:hover:not(:disabled) { background: #5c6bc0; }
button:disabled { opacity: 0.4; cursor: not-allowed; }

.note {
  font-size: 0.78rem;
  color: #aaa;
  background: #16213e;
  border-radius: 8px;
  padding: 0.6rem 0.8rem;
  margin-bottom: 1rem;
  line-height: 1.4;
}
.note code {
  background: #0d0d1a;
  padding: 0 0.3rem;
  border-radius: 3px;
}

section {
  background: #16213e;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.servo-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.angle-readout {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
}

.angle-value {
  font-size: 2.5rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #4caf50;
}

.angle-label {
  font-size: 0.75rem;
  color: #aaa;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.angle-track,
.ai-bar-track {
  width: 100%;
  height: 10px;
  border-radius: 5px;
  background: #2a2a3e;
  border: 1px solid #444;
  overflow: hidden;
}
.angle-fill,
.ai-bar-fill {
  height: 100%;
  background: #4caf50;
  transition: width 0.15s;
}

.slider-scale {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #777;
  font-variant-numeric: tabular-nums;
}

.ai-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 0.6rem;
}
.ai-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.ai-caption {
  font-size: 0.7rem;
  color: #777;
}
.ai-raw {
  font-size: 1.4rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: #fff;
}
.ai-cal {
  font-size: 1.4rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: #4caf50;
}

.calib-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.calib-col {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  background: #0d0d1a;
  border-radius: 8px;
  padding: 0.6rem 0.5rem;
  min-width: 0;
}

.calib-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #fff;
  text-align: center;
}

.ref-label {
  font-size: 0.65rem;
  font-weight: 600;
  color: #aaa;
}

.ref-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.ref-input {
  width: 100%;
  padding: 0.2rem 0.3rem;
  border-radius: 4px;
  border: 1px solid #444;
  background: #1a1a2e;
  color: #e0e0e0;
  font-size: 0.8rem;
}

.small-btn {
  padding: 0.2rem 0.3rem;
  font-size: 0.68rem;
  background: #2a2a3e;
  border: 1px solid #444;
}

.ref-live {
  font-size: 0.65rem;
  color: #777;
  font-variant-numeric: tabular-nums;
}

.calib-btn {
  margin-top: 0.3rem;
  padding: 0.45rem 0;
  font-weight: 600;
}

.defaults-btn {
  margin-top: 0.75rem;
  width: 100%;
  background: #2a2a3e;
  border: 1px solid #444;
}
.defaults-btn:hover:not(:disabled) { background: #3f51b5; }
</style>
