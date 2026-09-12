# Übung 247: Korrekturfaktor mit echtem PWM-Ausgang zum Nachmessen

## Thema: Von der VT-Anzeige zur echten Hardware — REAL-Prozent auf 13-Bit-PWM-Tastgrad, AR_SPLIT_2 zum Verzweigen

### Situationsbeschreibung

`Uebung_245_AX` hat den Korrekturfaktor nur auf dem VT-Zahlenfeld sichtbar gemacht. Diese Übung
ist eine Kopie von `Uebung_245_AX` mit einem zusätzlichen, echten `logiBUS_QDA_PWM`-Ausgang auf
`Q1` — damit lässt sich der korrigierte Wert nicht nur ablesen, sondern mit Multimeter oder
Oszilloskop direkt am Ausgang nachmessen. Das ist derselbe letzte Schritt, der auch in einer
realen PWM-auf-PVEA-Kette (siehe `RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB` in `MyLib_AX-1.0.0`)
den Sollwert an die Hardware bringt.

### Funktionsbeschreibung

- **Unverändert wie `Uebung_245_AX`:** `NumericValue_PHYSA` (`I3`) → `AR_MUL_2`
  (`F_MUL_KORREKTUR`, `IN2` fest über `initval_AR` auf `REAL#1,17619`) liefert den korrigierten
  Prozentwert.
- **Verzweigen mit `AR_SPLIT_2`:** Ein AR-Adapter-Plug kann nur an EINEN Socket angeschlossen
  werden (dieselbe 1:1-Regel wie bei den anderen Adapter-Typen, siehe z.B. `AX_SPLIT_n` in der
  `Softkey_Aux_IXA_TO_Remote_WRITE`-Familie). `AR_SPLIT_2` fächert den korrigierten Wert
  auf zwei Ziele auf: `OUT1` weiter zum VT-Feld `N3` (wie bisher), `OUT2` neu zur PWM-Kette.
- **Prozent auf 13-Bit-Tastgrad:** ein zweiter `AR_MUL_2` (mit `initval_AR = REAL#81,91`, das ist
  8191/100) skaliert den 0-100%-Wert auf den 13-Bit-LEDC-Tastgrad 0-8191 — exakt dieselbe
  Umrechnung, die in `RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB` (`MyLib_AX-1.0.0`) über
  `F_MUL_TO_PWM13BIT`/`F_DIV_TO_PWM13BIT` läuft, hier aber als reine AR-Multiplikation mit einem
  einzigen festen Faktor (da wir schon in Prozent, nicht im ISO-11783-Rohwert 0-64255, rechnen).
- **REAL nach DWORD, aber richtig herum:** `AR_TO_AD_NUM` — numerische Wandlung `REAL`→`DWORD`
  über einen internen `UDINT`-Zwischenschritt (`F_REAL_TO_UDINT` echter Cast, `F_UDINT_TO_DWORD`
  Bit-Reinterpretation, hier unproblematisch, weil `UDINT`/`DWORD` beide 32 Bit breit sind und
  denselben Wertebereich abbilden). **Vorsicht:** Es gibt auch ein direktes `AR_TO_AD` in
  derselben Bibliothek — das macht aber eine reine IEEE754-Bit-Reinterpretation (für
  Serialisierung gedacht), keine Zahlenumwandlung, und wäre hier falsch (siehe dessen eigener
  Comment-Text und, spiegelbildlich für die andere Richtung, `AD_TO_AR_NUM`s Dokumentation).
  `AR_TO_AD_NUM` ist neu (diese Übung war der erste Anwendungsfall) und packt genau die Kette
  ein, die man sonst von Hand über `AR_TO_AUDI` + `AUDI_TO_AD` verdrahten müsste.
- **Echter Ausgang:** `logiBUS_QDA_PWM` auf `Output_Q1` gibt den Tastgrad als echtes PWM-Signal
  aus (13-Bit-LEDC, 400 Hz laut ESP32-Firmware).

**Messen:** Mittelwert an `Q1` gegen GND (Multimeter im Gleichspannungs-Mittelwert-Modus, oder
Oszilloskop-Mittelwertfunktion) = Tastgrad% × Versorgungsspannung. Bei `I3 = 50` sollte der
korrigierte Tastgrad 58,81 % sein — bei z.B. 24 V Versorgung also ca. 14,1 V Mittelwert.

**Achtung:** Der korrigierte Wert wird hier NICHT geklemmt. Werte über `I3 ≈ 85` ergeben einen
Tastgrad über 100 % (>8191) — was am Ausgang passiert (Sättigung bei 100 %, Wraparound, oder ein
Fehlerstatus), ist absichtlich nicht vorgegeben: das selbst zu beobachten ist Teil der Übung.

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_247_AX` an (bereits als Referenzlösung vorhanden).
2. Schließen Sie ein Messgerät an `Q1` gegen GND an.
3. Geben Sie auf `I3` verschiedene Werte im Bereich 0-85 ein und vergleichen Sie den gemessenen
   Mittelwert mit der Anzeige auf `N3` (korrigierter Prozentwert) unter Berücksichtigung Ihrer
   Versorgungsspannung.
4. Geben Sie testweise einen Wert über 85 ein und beobachten Sie, was am Ausgang passiert.

### Referenzlösung

`Uebung_247_AX.SUB`. Basiert auf `Uebung_245_AX`. Verwandte Übung: `Uebung_248_AX` (derselbe
PWM-Messaufbau, aber mit dem Hoch/Runter-Sollwert aus `Uebung_246_AX`).
