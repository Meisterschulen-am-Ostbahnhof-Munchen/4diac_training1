# Übung 236: Derselbe Last-Wins-Effekt wie 229/230/233 — ohne Edge-Detektor und Latch

## Thema: `AX_LAST_2` — gleiches Verhalten, drastisch weniger Bausteine

### Situationsbeschreibung

Zwei Taster `I1`/`I2` steuern gemeinsam einen Ausgang `Q1` — dieselbe Grundidee wie in
`Uebung_229_AX`/`Uebung_230_AX`, aber mit einem völlig anderen Baustein: `AX_LAST_2`
(`adapter::events::unidirectional`) statt `AX_RF_TRIG`/`AX_ASR_RF_TRIG`+`ASR_MERGE_2`+`AX_SR`/
`ASR_AX_SR`.

**Wichtig, korrigiert gegenüber einer früheren Fassung dieser Beschreibung:** `Uebung_236_AX`
verhält sich **beobachtbar identisch** zu `Uebung_229_AX`/`Uebung_230_AX`/`Uebung_233_AX` — nicht
anders, wie hier ursprünglich fälschlich behauptet wurde. Der Unterschied liegt im Bauplan, nicht
im Verhalten.

### Warum 229/230/233 KEIN "hält nach Loslassen"-Latch sind

`AX_RF_TRIG`/`AX_ASR_RF_TRIG` meldet die steigende Flanke (Drücken) als `SET` UND die fallende
Flanke (Loslassen) als `RESET` — beide Flanken BEIDER (bzw. aller drei) Taster wirken auf denselben
`AX_SR`/`ASR_AX_SR`. Das bedeutet: **jedes** Loslassen irgendeines Tasters schaltet `Q1` sofort AUS,
selbst wenn ein anderer Taster noch gedrückt gehalten wird — `Uebung_229_AX`s eigene Beschreibung
sagt das bereits explizit: "Der Ausgang folgt also nicht dem Tasterzustand, sondern immer der
zuletzt aufgetretenen Flanke (Drücken oder Loslassen, an welchem Taster auch immer)." Das ist also
kein Speicher, der "merkt", dass ein anderer Taster noch aktiv ist — es ist bereits dieselbe
"letzte Flanke gewinnt"-Logik wie bei `AX_LAST_2`.

### Funktionsbeschreibung

- **`AX_LAST_2`** hat zwei AX-Sockets (`IN1`, `IN2`) und einen AX-Plug (`OUT`). Sein ECC ist denkbar
  einfach: welcher Socket zuletzt sein eigenes Event (`IN1.E1`/`IN2.E1`) ausgelöst hat, dessen
  aktueller Datenwert (`D1`) wird sofort 1:1 an `OUT` durchgereicht.
- **Direkt verdrahtet**: `DigitalInput_I1`/`_I2` (`logiBUS_IXA`) gehen ohne Umweg über
  `AX_LAST_2.IN1`/`IN2` — `logiBUS_IXA.IN.E1` feuert (über `logiBUS_IX.IND`) ohnehin nur bei
  echter Zustandsänderung, ist also selbst schon "edge-getriggert", genau wie `E_RF_TRIG` in
  `AX_(ASR_)RF_TRIG`. Deshalb entsteht hier ohne jeden Zwischenbaustein exakt dieselbe
  "letzte Flanke gewinnt"-Sequenz wie in 229/230/233.
- **Der eigentliche Unterschied zu 229/230/233 ist der Bauplan, nicht das Verhalten:**
  - `Uebung_229_AX`: 2 `AX_RF_TRIG` + gemeinsamer `AX_SR` (lose EventConnections).
  - `Uebung_230_AX`: 2 `AX_ASR_RF_TRIG` + `ASR_MERGE_2` + `ASR_AX_SR` (dieselbe Funktion, als
    Adapter-Bausteine statt loser Events).
  - `Uebung_236_AX`: **ein einziger** Baustein (`AX_LAST_2`) ersetzt die komplette Kette aus
    Flankenerkennung + Merge + Latch, weil er direkt auf den rohen AX-Schreibereignissen arbeitet
    statt auf explizit erzeugten SET/RESET-Kommandos.

### Unterschied zu Übung 233 (`ASR_MERGE_3`) — Skalierbarkeit der Baustein-Familie

Der einzige *substantielle* Unterschied zwischen dieser Familie und `AX_LAST_2` ist nicht das
Verhalten, sondern wie gut sie auf mehr als 2 Quellen skalieren:

- **`ASR_MERGE_N`** existiert als ganze Familie (`ASR_MERGE_2..7`) — von 2 auf 3 Quellen zu gehen
  (Übung 230 → 233) heißt nur: einen weiteren `AX_ASR_RF_TRIG` anschließen und `ASR_MERGE_2` durch
  `ASR_MERGE_3` ersetzen (ein zusätzlicher Socket `IN3`, sonst identisch). Eine vierte Quelle wäre
  genauso einfach `ASR_MERGE_4`.
- **`AX_LAST_2`** hat dagegen **keine** höherwertige Geschwister — es gibt kein `AX_LAST_3` in der
  Bibliothek. Eine dritte Rohquelle lässt sich nur durch **Kaskadieren** zweier `AX_LAST_2`-Instanzen
  einbinden (`OUT` der einen auf `IN1`/`IN2` der nächsten). Das bleibt aber semantisch korrektes
  Last-Wins über alle drei Quellen, keine zweistufige Rangfolge: `AX_LAST_2` kopiert bei jeder
  Übernahme sowohl den Wert nach `OUT.D1` als auch löst es `OUT.E1` aus, jede Änderung an einer der
  ursprünglichen Quellen läuft also bei jedem Kaskadenschritt als frisches Event durch. Der
  Unterschied zu `ASR_MERGE_N` ist rein baulich (1 Baustein pro Eingangszahl vs. N-1 kaskadierte
  Instanzen), keine andere Semantik. Wie bei jeder IEC-61499-Anwendung mit mehreren unabhängigen
  Event-Quellen garantiert die Norm allerdings keine feste Reihenfolge für nahezu gleichzeitig
  eintreffende Events an verschiedenen Sockets (`IN1`/`IN2`) — "wer zuletzt schrieb" bezieht sich auf
  die tatsächliche Verarbeitungsreihenfolge im Laufzeitsystem, nicht auf einen exakten
  Quell-Zeitstempel.

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_236_AX` an (bereits als Referenzlösung vorhanden).
2. Verbinden Sie `Input_I1`/`Input_I2` direkt (ohne Zwischenbaustein) mit `AX_LAST_2.IN1`/`IN2`.
3. Verbinden Sie `AX_LAST_2.OUT` mit `Output_Q1`.
4. Am echten Terminal/Hardware testen und mit Übung 229/230 vergleichen: `I1` drücken → `Q1` ON;
   `I2` zusätzlich drücken und halten → `Q1` bleibt ON (I2 hat zuletzt geschrieben); `I2` loslassen
   (`I1` bleibt gedrückt) → `Q1` fällt sofort auf OFF — identisch zum Verhalten von Übung 229/230,
   nur mit einem einzigen Baustein statt drei.
5. Vergleichen Sie die beiden SubApps im 4diac-Editor: `Uebung_230_AX` hat 4 Bausteine
   (2x `AX_ASR_RF_TRIG`, `ASR_MERGE_2`, `ASR_AX_SR`) zwischen Ein- und Ausgang, `Uebung_236_AX`
   nur einen einzigen (`AX_LAST_2`) — für exakt dasselbe Verhalten.

### Referenzlösung

`Uebung_236_AX.SUB`. Der verwendete Baustein liegt in
`Ventilsteuerung\4diacIDE-workspace\.lib\adapter-3.0.0\typelib\events\unidirectional\BOOL\AX_LAST_2.fbt`.
