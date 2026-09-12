# Übung 235: Zweipunktregler mit Hysterese (VT-Variante)

## Thema: `DualHysteresis_AR_A2X` — Totzone + Hysterese um einen Mittelwert, Messwert und Rückmeldung komplett auf dem VT

### Situationsbeschreibung

Klassisches Thermostat-/Füllstandsschalter-Muster: ein analoger Messwert wird gegen einen
Mittelwert `MI` mit Totzone (`DEAD`) und Hysterese (`HYSTERESIS`) geprüft und schaltet darüber
zwei entgegengesetzte Aktoren (z.B. Heizen/Kühlen oder Befüllen/Entleeren) — nie beide
gleichzeitig. Im Pool `Workspace_Dreieck` simuliert der Bediener den Messwert über
`InputNumber_Messwert` (VT-Objekt 9002, Bereich 0–1000) statt über einen echten Analogsensor;
`OutputString_UP`/`OutputString_DOWN` (VT-Objekte 11001/11002) zeigen per Hintergrundfarbe an,
welcher der beiden Aktoren gerade aktiv wäre.

### Funktionsbeschreibung

- **Messwert lesen:** `Messwert_N` (`NumericValue_PHYSA`, `stObj := InputNumber_Messwert_N`)
  liefert bei jeder Änderung von `InputNumber_Messwert` den physikalischen Wert bereits direkt als
  `AR`-Adapter-Plug (`rPhys`) — anders als die reine Event-/Datenvariante `NumericValue_PHYS`
  braucht es hier keine separate Umwandlung in einen Adapter, `rPhys` wird direkt an
  `DualHysteresis_AR_A2X.INPUT` angeschlossen.
- **Regeln:** `DualHysteresis_AR_A2X` vergleicht den Messwert gegen `MI` (hier fest 500.0 über
  `HysteresisParams_AR`, im echten Einsatz parametrierbar): steigt der Wert über
  `MI + DEAD + HYSTERESIS` (hier 550), schaltet `UP`; fällt er unter `MI - DEAD - HYSTERESIS`
  (hier 450), schaltet `DOWN`. Ausgeschaltet wird erst innerhalb der reinen Totzone `MI ± DEAD`
  (480–520) — die Differenz zwischen Ein- und Ausschaltpunkt verhindert Flattern.
- **Anzeigen:** `DualHysteresis.OUT` liefert `UP`/`DOWN` gebündelt als ein `A2X`-Signal.
  `A2X_2X_TO_2AX` entbündelt es wieder in zwei einzelne `AX`-Signale, weil
  `GreenWhiteBackground1_AX` pro Instanz nur einen `DI1`-Eingang hat — je eine Instanz färbt
  `OutputString_UP` bzw. `OutputString_DOWN` grün/weiß.

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_235_AX` an (bereits als Referenzlösung vorhanden).
2. Lesen Sie `InputNumber_Messwert` (VT-Objekt 9002) mit einer `NumericValue_PHYSA`-Instanz
   (`Messwert_N`, `stObj := InputNumber_Messwert_N` aus `DefaultPool_Dreieck_Numeric.gcf`) — sie
   liefert den Wert bereits direkt als `AR`-Adapter-Plug (`rPhys`).
3. Verbinden Sie `Messwert_N.rPhys` direkt mit `DualHysteresis_AR_A2X.INPUT` (keine separate
   Umwandlung nötig). `MI`/`DEAD`/`HYSTERESIS` über eine `HysteresisParams_AR`-Instanz setzen
   (Standardwerte 500.0/20.0/30.0).
4. Entbündeln Sie `DualHysteresis.OUT` mit `A2X_2X_TO_2AX` und speisen Sie `UP`/`DOWN` in je eine
   `GreenWhiteBackground1_AX`-Instanz (`u16ObjId := OutputString_UP` bzw. `OutputString_DOWN`
   aus `DefaultPool_Dreieck.gcf`).
5. Am echten Terminal testen: `InputNumber_Messwert` auf einen Wert deutlich über 550 setzen →
   `OutputString_UP` wird grün, `OutputString_DOWN` bleibt weiß. Wert deutlich unter 450 →
   umgekehrt. Wert zwischen 480 und 520 → beide weiß. Werte zwischen 520–550 bzw. 450–480
   (innerhalb der Hysterese, außerhalb der Totzone) zeigen das Hysterese-Verhalten: der zuletzt
   aktive Zustand bleibt erhalten, bis die jeweilige Totzonen-Grenze erreicht wird.

### Referenzlösung

`Uebung_235_AX.SUB`. Für die reine Hardware-Variante (Analogsensor statt VT-Eingabe, physische
Ausgänge statt Hintergrundfarbe) siehe `Uebung_234_AX`. Die neuen VT-Objekte
(`InputNumber_Messwert` 9002, `NumberVariable_Messwert` 21002, `OutputString_UP` 11001,
`OutputString_DOWN` 11002) liegen in
`Ventilsteuerung\ISO-DesignerProjects\Workspace_Dreieck\DefaultPool\DefaultPool.jop`, platziert
auf `DataMask_M1` unterhalb der bestehenden Sollwert-/Istwert-Felder; die zugehörigen Konstanten
in `DefaultPool_Dreieck.gcf`/`DefaultPool_Dreieck_Numeric.gcf`.
