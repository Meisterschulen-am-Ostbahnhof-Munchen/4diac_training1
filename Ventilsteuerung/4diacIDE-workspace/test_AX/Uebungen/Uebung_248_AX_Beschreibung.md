# Übung 248: Hoch/Runter-Sollwert mit echtem PWM-Ausgang zum Nachmessen

## Thema: Von der VT-Anzeige zur echten Hardware — 3-Stufen-Sollwert auf 13-Bit-PWM-Tastgrad

### Situationsbeschreibung

`Uebung_246_AX` hat die drei Sollwerte (75/50/25 %) nur auf dem VT-Zahlenfeld sichtbar gemacht.
Diese Übung ist eine Kopie von `Uebung_246_AX` mit einem zusätzlichen, echten
`logiBUS_QDA_PWM`-Ausgang auf `Q1` — damit lässt sich das Ergebnis direkt mit Multimeter oder
Oszilloskop nachmessen, statt es nur auf dem VT zu prüfen. Zusammen mit `Uebung_247_AX` deckt das
beide Bausteine einer typischen Heben/Senken-Funktion mit Taster-Sollwertvorgabe ab: dort Taster →
75/50/25 %-Sollwert (wie hier), hier zusätzlich die Umsetzung in ein echtes PWM-Signal.

### Funktionsbeschreibung

- **Unverändert wie `Uebung_246_AX`:** `I1`(Hoch)/`I2`(Runter) über `logiBUS_IXA`, zwei
  verkettete `AR_AX_SEL_AR` liefern 75/50/25 % je nach Tasterzustand.
- **Verzweigen mit `AR_SPLIT_2`:** genau wie in `Uebung_247_AX` fächert `AR_SPLIT_2` den
  Sollwert auf das VT-Feld `N3` (`OUT1`, unverändert) und die neue PWM-Kette (`OUT2`) auf.
- **Prozent auf 13-Bit-Tastgrad:** `AR_MUL_2` mit `initval_AR = REAL#81,91` (= 8191/100) skaliert
  0-100 % auf 0-8191 — siehe `Uebung_247_AX` für die Herleitung.
- **REAL nach DWORD:** `AR_TO_AD_NUM` (numerische Wandlung über internen `UDINT`-Schritt, siehe
  `Uebung_247_AX_Beschreibung.md`). Nicht das bit-reinterpretierende `AR_TO_AD` verwenden.
- **Echter Ausgang:** `logiBUS_QDA_PWM` auf `Output_Q1`.

**Messen:** Mittelwert an `Q1` gegen GND = Tastgrad% × Versorgungsspannung. Da hier keine
Korrektur stattfindet, sollten `I1` gehalten 75 % (0,75 × U_DC), `I2` gehalten 25 % (0,25 × U_DC)
und Neutralstellung 50 % (0,50 × U_DC) ergeben — direkt vergleichbar mit den erwarteten
PVEA-Sollspannungen aus einer entsprechenden Kompensationsrechnung.

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_248_AX` an (bereits als Referenzlösung vorhanden).
2. Schließen Sie ein Messgerät an `Q1` gegen GND an.
3. Halten Sie `I1` bzw. `I2` und prüfen Sie den gemessenen Mittelwert gegen die erwarteten 75 %
   bzw. 25 % Ihrer Versorgungsspannung; loslassen → 50 %.
4. Vergleichen Sie mit `Uebung_247_AX`: dort wird derselbe PWM-Aufbau von einem korrigierten statt
   einem rohen Sollwert gespeist — messen Sie den Unterschied direkt am Ausgang.

### Referenzlösung

`Uebung_248_AX.SUB`. Basiert auf `Uebung_246_AX`. Verwandte Übung: `Uebung_247_AX` (derselbe
PWM-Messaufbau, aber mit dem Korrekturfaktor aus `Uebung_245_AX`).
