<template>
  <div class="app">
    <header>
      <h1>APIXON Node 20 — Servo Test (Q2)</h1>
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
      Servo an <strong>Output_Q2</strong> (<code>logiBUS_QWA_SERVO</code>), Winkelbereich 0–180°.
      Der Slider schreibt den Sollwinkel per OPC-UA; die Anzeige darunter zeigt den vom
      Controller zurückgemeldeten, tatsächlich angewendeten Winkel (eigener Echo-Knoten,
      kein Selbst-Loop auf denselben Knoten).
    </p>

    <section>
      <div class="servo-card">
        <div class="angle-readout">
          <span class="angle-value">{{ liveAngle.toFixed(0) }}°</span>
          <span class="angle-label">aktueller Winkel (Echo)</span>
        </div>

        <input
          type="range"
          min="0"
          max="180"
          step="1"
          v-model.number="sliderAngle"
          :disabled="!connected"
          class="slider"
          @input="writeAngle"
        />
        <div class="slider-scale">
          <span>0°</span>
          <span>90°</span>
          <span>180°</span>
        </div>

        <div class="preset-buttons">
          <button :disabled="!connected" @click="setPreset(0)">0°</button>
          <button :disabled="!connected" @click="setPreset(90)">90°</button>
          <button :disabled="!connected" @click="setPreset(180)">180°</button>
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

/* Sollwinkel (0-180°), per Slider gesetzt - geschrieben auf SERVO_Q2_ANGLE_SET,
 * den der Controller abonniert (siehe Servo_Slider_OPC.SUB, AngleSubscribe). */
const sliderAngle = ref(0)

/* Tatsaechlich angewendeter Winkel (0-180°), vom Controller auf einen eigenen
 * Echo-Knoten SERVO_Q2_ANGLE zurueckgeschrieben (AngleEcho) - bewusst ein
 * anderer Knoten als SERVO_Q2_ANGLE_SET, damit Sollwert-Schreiben und
 * Echo-Publish sich nicht gegenseitig ueberschreiben (Selbst-Loop-Falle,
 * siehe Kommentare im AI-Calibrate-Client). */
const liveAngle = ref(0)

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
  liveAngle.value = 0
  session = null
  client = null
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
      maxNotificationsPerPublish: 10,
      publishingEnabled: true,
      priority: 10,
    })

    /* Monitor den Echo-Knoten SERVO_Q2_ANGLE (REAL, 0-180, read-only aus Client-Sicht). */
    const angleGroup = await subscription.monitorItemsP(
      [{ nodeId: coerceNodeId('ns=1;s=SERVO_Q2_ANGLE'), attributeId: AttributeIds.Value }],
      { samplingInterval: 100, discardOldest: true, queueSize: 2 },
      TimestampsToReturn.Neither
    )
    angleGroup.on('changed', (_item: any, dataValue: any) => {
      liveAngle.value = Number(dataValue.value?.value ?? 0)
    })
  } catch (err) {
    status.value = 'Fehler: ' + (err as Error).message
    connected.value = false
  }
}

async function writeAngle() {
  if (!session) return
  try {
    const wv = new WriteValue({
      nodeId: coerceNodeId('ns=1;s=SERVO_Q2_ANGLE_SET'),
      attributeId: AttributeIds.Value,
      value: new DataValue({ value: new Variant({ dataType: DataType.Float, value: sliderAngle.value }) }),
    })
    await session.writeP([wv])
  } catch (err) {
    console.error('Servo-Winkel schreiben fehlgeschlagen:', err)
  }
}

function setPreset(angle: number) {
  sliderAngle.value = angle
  writeAngle()
}

async function disconnect() {
  if (client) {
    client.off('connection_lost', handleLost)
    client.off('close', handleLost)
    await client.disconnectP()
  }
  connected.value = false
  status.value = 'Getrennt'
  liveAngle.value = 0
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
  max-width: 480px;
  margin: 0 auto;
  padding: 1rem;
  background: #1a1a2e;
  min-height: 100vh;
  color: #e0e0e0;
}

header {
  margin-bottom: 0.75rem;
}

h1 {
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
  color: #fff;
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
  padding: 1.25rem 1rem;
}

.servo-card {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 0.75rem;
}

.angle-readout {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.15rem;
  margin-bottom: 0.5rem;
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

.slider {
  width: 100%;
  accent-color: #4caf50;
  height: 2rem;
  cursor: pointer;
}
.slider:disabled { cursor: not-allowed; opacity: 0.4; }

.slider-scale {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #777;
  font-variant-numeric: tabular-nums;
}

.preset-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.preset-buttons button {
  flex: 1;
  background: #2a2a3e;
  border: 1px solid #444;
}
.preset-buttons button:hover:not(:disabled) { background: #3f51b5; }
</style>
