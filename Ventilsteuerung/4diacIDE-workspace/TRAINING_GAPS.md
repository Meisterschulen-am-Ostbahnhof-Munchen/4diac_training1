# Trainings-Lücken-Analyse (test_AX / test_VV / .lib)

Stand: 2026-09-07. Gap-Analyse per Fork-Agent, ursprünglich basierend auf
tatsächlicher Grep-Prüfung (nicht nur Dateinamen) gegen `test_AX/Uebungen`,
`test_B`, `test_VV/sys/03_OPC_UA` und die vendorierten Typelibs; die
Zero-Usage-Liste unten wurde am 2026-09-07 gegen die inzwischen ergänzten
Übungen aktualisiert (siehe die "Erledigt"-Einträge weiter unten).

## Bestätigt (0 Verwendung in irgendeiner Übung)

- **`AE_SPLIT_2..9`, `ASRT_SPLIT_2..9`, `ASR_SPLIT_3..9`** — die Fan-out-Seite
  der Event-Adapter-Familie bleibt größtenteils ungeübt, obwohl Fan-in
  (`*_MERGE`) seit `Uebung_229/230_AX` abgedeckt ist. `ASR_SPLIT_2` selbst ist
  davon ausgenommen — siehe Punkt 2 unten (`Uebung_231_AX`).
- Alles ASRT-spezifische aus dieser Session außer `ASRT_MERGE_2` (siehe
  Punkt 1 unten): `ASRT_MERGE_3..7`, sowie die 4 neuen AE-basierten
  Konverter (`ASRT_3AE_TO_SRT`, `ASRT_SRT_TO_3AE`, `ASRT_SRT_TO_SR_AE`,
  `ASRT_SR_AE_TO_SRT`, plus `ASR_2AE_TO_SR`/`ASR_SR_TO_2AE`).
  `Uebung_171_ASR`/`Uebung_172_ASRT` zeigen zwar schon den ALTEN
  Plain-Event-Konvertierungsweg (`ASR_2EVENTS_TO_SR`, `ASRT_3EVENTS_TO_SRT`)
  in `ASR_AX_SR`/`ASRT_AX_T_FF_SR`, aber nichts zeigt die neueren
  AE-Adapter-Konverter.
- **`ILOCK_T_FF_SR`** (klassische, nicht-AX-Variante) — bestätigt ungenutzt,
  die ILOCK-README nennt das selbst schon. `ILOCK_T_FF_SR_AX` ist davon
  ausgenommen — siehe Punkt 7 unten (`Uebung_206b_AX`).

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

2. ~~**Eine `*_SPLIT`-Übung (Fan-out, beliebige Familie).**~~ **Erledigt
   2026-09-07**: `Uebung_231_AX.SUB`. Direktes Spiegelbild zu `Uebung_230_AX`:
   ein Taster liefert über `AX_ASR_RF_TRIG` ein ASR-Signal, `ASR_SPLIT_2`
   dupliziert es (weil ein Adapter-Plug nur punkt-zu-punkt geht) auf zwei
   unabhängige `ASR_AX_SR`-Latches mit je eigenem Ausgang (`Q1`/`Q2`) - "MERGE
   war N→1, hier ist SPLIT 1→N", explizit so gerahmt.

3. ~~**`ASR_2AE_TO_SR`/`ASRT_3AE_TO_SRT` in einer aktualisierten
   171/172-Variante.**~~ **Erledigt 2026-09-07**: `Uebung_171b_ASR.SUB` und
   `Uebung_172b_ASRT.SUB`. Identisches Verhalten zu 171/172, aber
   `ASR_2AE_TO_SR`/`ASRT_3AE_TO_SRT` (AE-Adapter-Sockets) statt
   `ASR_2EVENTS_TO_SR`/`ASRT_3EVENTS_TO_SRT` (rohe EventInputs), mit je einem
   `AE_EVENT_TO_E` pro Kanal als Brücke vom rohen Klick-Event zum getypten
   AE-Plug - zeigt den Gewinn (AE-Plugs sind wie jeder Adapter mit
   `AE_SPLIT_2` weiterverarbeitbar, rohe Events nicht). Zusätzlich
   `Uebung_171c_ASR.SUB`/`Uebung_172c_ASRT.SUB`: dieselbe Funktion nochmal mit
   `logiBUS_IEA` statt `logiBUS_IE` - der AE-Plug ist dort schon eingebaut,
   macht `AE_EVENT_TO_E` überflüssig (Pendant zu `IX`→`IXA` für Event-Eingänge).

4. ~~**`ASR_MERGE_3`** (oder höher)~~ **Erledigt 2026-09-07**: `Uebung_233_AX.SUB`.
   Direkte Fortsetzung von `Uebung_230_AX`: 3 Taster über je einen
   `AX_ASR_RF_TRIG`, zusammengeführt via `ASR_MERGE_3` auf ein gemeinsames
   `ASR_AX_SR`-Latch - validiert, dass die MERGE-Familie kein reiner
   2-Input-Spezialfall ist.

5. ~~**`DualHysteresis_AR_A2X`-Übung**~~ **Erledigt 2026-09-07**, als Paar:
   `Uebung_234_AX.SUB` (reine Hardware-Variante: echter Analogsensor über
   `logiBUS_AI_IDA`, UP/DOWN auf 2 physische Ausgänge via `A2X_TO_QXA2`) und
   `Uebung_235_AX.SUB` + `Uebung_235_AX_Beschreibung.md` (VT-Variante, passend
   zur Tiefe von `BargraphSplitFS`/`PositionMarkerFS`: Messwert per
   `InputNumber_Messwert` simuliert, UP/DOWN als Hintergrundfarbe auf zwei
   neuen VT-Textfeldern in `Workspace_Dreieck`/`DataMask_M1`). Beide zeigen
   dasselbe Zweipunktregler-Muster mit denselben MI/DEAD/HYSTERESIS-Werten
   (500/20/30), einmal hardwarenah, einmal VT-nah.

6. ~~**`ILOCK_CONFLICT_TRIP` + Dead-Time-Variante**~~ **Erledigt 2026-09-07**:
   neue Bausteine `ILOCK_CONFLICT_TRIP_PROTECT`/`_AX` (TRIP-Semantik von
   `ILOCK_CONFLICT_TRIP` + `DT_PROTECT`-Totzeit von `ILOCK_BLOCK_PROTECT`),
   dazu `Uebung_204c_AX.SUB`. ILOCK_README.md aktualisiert. (Die
   QI-gegatete-ILOCK-Hälfte wurde nach Punkt 19 ausgelagert.)

7. ~~**`ILOCK_T_FF_SR`/`_AX`**~~ **Erledigt 2026-09-07** (AX-Hälfte):
   `Uebung_206b_AX.SUB` - wie `Uebung_206_AX` (`ILOCK_T_FF_AX`, 2 verkettete
   Toggle-FFs), aber `ILOCK_T_FF_SR_AX` mit zusätzlichem direktem Set/Reset
   auf FF1, das über dieselbe Adapterkette genauso verriegelnd wirkt wie ein
   CLK-Toggle. Die klassische (nicht-AX) `ILOCK_T_FF_SR`-Variante hat noch
   keine Übung.

8. **Klassische (nicht-AX) Vorführung von 2x Flankentrigger + Set/Reset-Merge
   fehlt als Übung.** Nachgefragt 2026-09-07: Es gibt KEINE Übung, die
   `AX_ASR_RF_TRIG` (2x) + `ASR_AX_SR` mit einfachem `logiBUS_IX`/`QX` statt
   `logiBUS_IXA`/`QXA` zeigt. Die einzige Stelle, an der genau dieses
   FB-Trio (`AX_ASR_RF_TRIG` 2x + `ASR_MERGE_2` + `ASR_AX_SR`) überhaupt
   vorkommt, ist die Library-SubApp
   `Button_IXA_TO_logiBUS_QXA_BG_OPC_LATCHING.SUB` (Produktions-Baustein,
   keine Übung) - und selbst die nutzt durchgängig die AX-Adapter-Varianten
   (`Button_IXA`/`logiBUS_QXA`), nicht die klassischen `_IX`/`_QX`. Da
   `AX_ASR_RF_TRIG`/`ASR_AX_SR` inhärent AX-Adapter-Sockets sind, bräuchte
   eine echte "mit einfachem IX/QX"-Variante zusätzlich eine BOOL-zu-AX-Brücke
   an den Rändern - didaktisch fraglich, ob das die Lektion verwässert oder
   gerade zeigt, wie man AX-Verarbeitung in eine klassische Schaltung
   einbettet. `Uebung_230_AX` selbst bleibt die sauberste vorhandene
   Demonstration (aber komplett im AX-Stil, nicht gemischt).

9. ~~**`AX_LAST_2`-Übung fehlt komplett.**~~ **Erledigt 2026-09-07**:
   `Uebung_236_AX.SUB`. Zwei Taster direkt (ohne `AX_ASR_RF_TRIG`) auf
   `AX_LAST_2.IN1`/`IN2`, `OUT` treibt `Q1` — verhält sich **beobachtbar
   identisch** zu `Uebung_229/230_AX` (beide sind "letzte Flanke gewinnt",
   da `AX_(ASR_)RF_TRIG` Loslassen ebenfalls als RESET wertet - kein
   "hält nach Loslassen"-Latch, siehe Korrektur in
   `Uebung_236_AX_Beschreibung.md`), nur mit einem einzigen Baustein statt
   drei. Der substantielle Unterschied zur `ASR_MERGE_N`-Familie ist
   Skalierbarkeit: `ASR_MERGE_2..7` deckt beliebig viele Quellen ab,
   `AX_LAST_2` hat kein `AX_LAST_3` und müsste kaskadiert werden (ändert
   die Semantik zu einer zweistufigen Rangfolge statt flacher N-fach-ODER).

10. ~~**`AD_TO_AR_NUM`/`AD_TO_AR`/`AD_TO_AUDI`+`AUDI_TO_AR` — Bit-Reinterpretation-
    Falle wird nirgends als Übung/Beispiel gezeigt.**~~ **Erledigt 2026-09-07**:
    `Uebung_237_AX.SUB`. Derselbe Analogwert (`AnalogInput_I4`, per `AD_SPLIT_2`
    verdoppelt) läuft parallel durch `AD_TO_AR_WRONG` (`AD_TO_AR` - liefert
    eine bedeutungslose Zahl nahe Null) und `AD_TO_AR_NUM_CORRECT`
    (`AD_TO_AR_NUM` - liefert den echten Messwert); beide `AR_OUT.D1` sollen
    im 4diac-Monitor per Watch verglichen werden. Dokumentation im
    Documentation-Attribut der SubApp, kein separates .md nötig.

11. **SAFE-Arithmetik (`SafeArithmetic::arithmetic::SAFE_ADD_2/_3/_4`,
    `SAFE_MUL_2/_3/_4`, `SAFE_SUB`, `SAFE_DIV`) hat noch keine Adapter-Variante
    — `Uebung_011b4..011b7_AX` deshalb am 2026-09-10 aus `test_AX` entfernt.**
    Geprüft: kein `.fbt` in `.lib` bietet einen AUDI/AX-Adapter-Ersatz für
    diese Bausteine (anders als z.B. `F_SEL`→`AUDI_AX_SEL_AUDI` oder
    `F_UINT_TO_UDINT`(Konstante)→`initval_AUDI`, die es für die
    Rand-Konvertierung schon gibt). Die reine Rand-Brücken-Lösung
    (`NumericValue_IDA`→`AD_TO_AUDI`→`AUDI_UDI_TO_UDINT`→**plain**
    `SAFE_ADD_2`→`AUDI_UDINT_TO_UDI`→`Q_NumericValue_AUDI`) wurde verworfen,
    weil sie im Kern weiterhin plain rechnet - genau das Muster, das test_AX
    NICHT lehren soll. `test_B/Uebungen/Uebung_011b4..011b7.SUB` bleiben die
    einzige Heimat für diese Übungen, bis es Adapter-typisierte SAFE-Bausteine
    gibt. Offene Frage für später: eigene `AUDI_SAFE_ADD_2`/`_SUB`/`_MUL_2`/
    `_DIV`-Familie in `adapter-3.0.0` entwerfen (Sockets `IN1`/`IN2: AUDI`,
    Plug `OUT: AUDI`, `LIMIT_HIT` bleibt plain BOOL-Event-Ausgang oder wird
    selbst zu einem AX-Adapter) - erst dann können 011b4-011b7 nach AX
    portiert werden, im vollen Adapter-Stil wie `Uebung_015_AX`.

12. **QI-gegatete ILOCK-Übung — noch nicht entschieden, ob gewollt.**
    Ausgelagert aus Punkt 6 am 2026-09-07: kein ILOCK-Baustein (7 Grundtypen,
    14 Dateien mit AX-Varianten) hat einen generellen Freigabe-/Qualitäts-
    Eingang - einmal verdrahtet, arbitriert ein ILOCK immer aktiv, ohne
    Möglichkeit, ihn von außen einzufrieren (Wartungsmodus, übergeordnete
    Sicherheitsfreigabe, Signalqualitätsverlust).

    Zwei diskutierte Umsetzungen, keine davon bisher beschlossen:
    - **Nativ pro Baustein**: jeden der 13 `.fbt`s einzeln um ein
      `QI`-EventInput/ECC-Gate erweitern - der Zustandsautomat selbst wird
      eingefroren, aber 13 bestehende, verifizierte Dateien anfassen, mit
      echtem Risiko fürs etablierte Verhalten.
    - **Generischer QI-Gate-Wrapper**: eine SubApp, die die
      `UP_OUT`/`DOWN_OUT`(/`TRIP_OUT`) eines beliebigen bestehenden
      ILOCK-Bausteins per UND mit `QI` maskiert - kein bestehender `.fbt`
      wird angefasst, funktioniert sofort mit allen 13 Varianten, passt zum
      "SUB style"-Prinzip der Bibliothek. Nachteil: der interne
      Zustandsautomat läuft im Hintergrund weiter, nur die Ausgänge werden
      stumm geschaltet (matcht aber das übliche `QI`-Verhalten anderswo im
      Projekt, z.B. `logiBUS_IXA`/`AI_IDA` - dort ist `QI` auch nur ein Gate,
      kein State-Reset).

    Zurückgestellt, bis geklärt ist, ob das Training das überhaupt braucht.

## Außerhalb des Fokus / niedrigere Priorität

- ~~`Q_ChildPosition`/Scaling-Flag-Familie — laut Doku bewusst nativer Stub,
  keine Übungslücke.~~ **Korrigiert 2026-09-07**: falsch. Das `xScale`-Flag
  wird bereits real getestet - `Uebung_225_AX` (test_AX), `Uebung_225b`/`_AX`
  (test_B/test_AX) und `Uebung_227_AX` setzen `xScale="TRUE"` auf
  `PositionMarkerFS`/`FSA` (`Marker_Dreieck`), der Dreieck-Sollwertmarker
  bewegt sich dadurch tatsächlich mit dem DataMask-Scaling-Faktor
  multipliziert statt 1:1 - siehe Kommentar in `Uebung_225b.SUB` (test_B).
  (Nebenbei am selben Tag korrigiert: `Uebung_225_AX`/`Uebung_225b_AX`
  hießen fälschlich so, obwohl sie klassisch/nicht adapter-basiert waren -
  jetzt als `Uebung_225`/`Uebung_225b` nach test_B verschoben, die
  tatsächlichen Adapter-Varianten `Uebung_225_AXA`/`_225b_AXA` entsprechend
  zu `Uebung_225_AX`/`_225b_AX` umbenannt.) Nur die zugrundeliegende
  Multiplikation selbst läuft nativ in FORTE (siehe
  `SCALING_FLAG_KONZEPT.md`), aber das Flag/Vertrag ist über diese Übungen
  bereits abgedeckt, nicht ungeübt.
- Volle 3-Wege-Verriegelung — echte neue `.fbt`-Arbeit, keine reine fehlende
  Übung.
