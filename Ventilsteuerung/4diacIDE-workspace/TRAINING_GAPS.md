# Trainings-Lücken-Analyse (test_AX / test_VV / .lib)

Stand: 2026-09-06. Gap-Analyse per Fork-Agent, basierend auf tatsächlicher
Grep-Prüfung (nicht nur Dateinamen) gegen `test_AX/Uebungen`, `test_B`,
`test_VV/sys/03_OPC_UA` und die vendorierten Typelibs. Reine Bestandsaufnahme,
keine Umsetzung.

## Bestätigt (0 Verwendung in irgendeiner Übung)

- **`AE_SPLIT_2..9`, `ASR_SPLIT_2..9`, `ASRT_SPLIT_2..9`** — die gesamte
  Fan-out-Seite der Event-Adapter-Familie wird nirgends geübt, obwohl Fan-in
  (`*_MERGE`) seit `Uebung_229/230_AX` abgedeckt ist.
- Alles ASRT-spezifische aus dieser Session: `ASRT_MERGE_2..7`, sowie die 4
  neuen AE-basierten Konverter (`ASRT_3AE_TO_SRT`, `ASRT_SRT_TO_3AE`,
  `ASRT_SRT_TO_SR_AE`, `ASRT_SR_AE_TO_SRT`, plus `ASR_2AE_TO_SR`/
  `ASR_SR_TO_2AE`). `Uebung_171_ASR`/`Uebung_172_ASRT` zeigen zwar schon den
  ALTEN Plain-Event-Konvertierungsweg (`ASR_2EVENTS_TO_SR`,
  `ASRT_3EVENTS_TO_SRT`) in `ASR_AX_SR`/`ASRT_AX_T_FF_SR`, aber nichts zeigt
  die neueren AE-Adapter-Konverter oder MERGE/SPLIT.
- **`DualHysteresis_AR_A2X`** (zusammen mit `BargraphSplitFS`/
  `PositionMarkerFS` in dieser Session vendoriert) — die beiden Geschwister
  haben je 7-9 Übungen, DualHysteresis hat 0.
- **`ILOCK_T_FF_SR`/`ILOCK_T_FF_SR_AX`** — bestätigt ungenutzt, die
  ILOCK-README nennt das selbst schon.

## Starkes vorhandenes Signal — ILOCK_README.md's eigene "Was fehlt?"-Tabelle

Nicht neu herleiten, sondern direkt übernehmen: 3-Wege-Verriegelung (nur
2-kanalig vorhanden), `ILOCK_CONFLICT_TRIP` mit Dead-Time (Trip hat keine
`DT_PROTECT`-Variante), ein genereller `QI`-Enable/Qualitäts-Eingang über die
ganze ILOCK-Familie, Entprellung/Hysterese, Aktor-Rückmeldung/Plausibilisierung.

## Priorisierte Top-Lücken

1. ~~**`ASRT_MERGE_2`-Übung (höchster Wert, auffälligste Lücke).**~~ **Erledigt
   2026-09-06**: `Uebung_232_AX.SUB` (+ Beschreibung im Documentation-Attribut).
   Direktes Geschwister zu `Uebung_229/230_AX`, mit `ASRT` durchgängig: Quelle 1
   ist eine neue Composite-SubApp `AX_ASRT_RF_TRIG` (Pendant zu `AX_ASR_RF_TRIG`,
   aus diesem plus `ASRT_SR_AE_TO_SRT` zusammengesetzt - SR_IN direkt aus dem ASR,
   TOGGLE_IN unverdrahtet) an einem klassischen Taster; Quelle 2 ist
   `ASRT_3EVENTS_TO_SRT` mit nur `TOGGLE` verdrahtet an einem echten
   Toggle-Taster; `ASRT_MERGE_2` führt beide zu einem gemeinsamen
   `ASRT_AX_T_FF_SR`-Latch zusammen. Neuer Baustein:
   `MyLib_AX-1.0.0/typelib/sys/AX_ASRT_RF_TRIG.SUB`.

2. **Eine `*_SPLIT`-Übung (Fan-out, beliebige Familie).** Ein physischer
   Trigger steuert 2-3 unabhängige nachgelagerte Verbraucher über
   `AE_SPLIT_2` oder `ASR_SPLIT_2` an — das Spiegelbild zur Fan-in-Lektion
   aus 229/230. Naheliegender Slot: `Uebung_231_AX`, explizit als
   "MERGE war N→1, hier ist 1→N" gerahmt.

3. **`ASR_2AE_TO_SR`/`ASRT_3AE_TO_SRT` in einer aktualisierten
   171/172-Variante.** Da 171/172 schon die Plain-Event-Konvertierung lehren,
   würde eine `171b`/`172b`-Variante mit den AE-Adapter-Konvertern direkt
   zeigen, WARUM der AE-basierte Weg existiert (komponierbare Einzelsignal-
   AE-Stecker vs. gebündelte rohe Events), ohne neue Pädagogik zu erfinden.

4. **`ASR_MERGE_3`** (oder höher) — natürliche Fortsetzung von 229/230s
   "2 Taster, Last-Wins" zu "3 Taster, Last-Wins", validiert, dass die
   N-beliebig-Behauptung der MERGE-Familie kein reiner 2-Input-Spezialfall ist.

5. **`DualHysteresis_AR_A2X`-Übung** — eine echte Analogsignal-Übung (z.B.
   Zweipunkt-Regelung, klassisches Thermostat-/Füllstandsschalter-Muster),
   passend zur Tiefe, die `BargraphSplitFS`/`PositionMarkerFS` schon haben.

6. **`ILOCK_CONFLICT_TRIP` + Dead-Time-Variante** und **eine QI-gegatete
   ILOCK-Übung** — beide von der README selbst markiert, weder Baustein noch
   Übung existiert bisher (braucht erst einen neuen `.fbt`, keine reine
   Übungslücke).

7. **`ILOCK_T_FF_SR`/`_AX`** — der letzte ungenutzte, aber existierende
   ILOCK-Typ. Billigster Quick-Win: eine Übung, die ihn mit dem etablierten
   Toggle-FF-Muster (analog zu `ILOCK_T_FF`) paart.

## Außerhalb des Fokus / niedrigere Priorität

- `Q_ChildPosition`/Scaling-Flag-Familie — laut Doku bewusst nativer Stub,
  keine Übungslücke.
- Volle 3-Wege-Verriegelung — echte neue `.fbt`-Arbeit, keine reine fehlende
  Übung.
