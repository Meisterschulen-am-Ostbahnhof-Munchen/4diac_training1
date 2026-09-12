# Übung 246: Hoch/Runter auf 3-Stufen-Sollwert — zwei AR_AX_SEL_AR verkettet

## Thema: Digitale Taster als "3-Stufen-Joystick", Kaskadierung von binären AR-Selektoren

### Situationsbeschreibung

Viele reale Funktionen (siehe `Uebung_245_AX` und die zugehörige PVEA-Kompensationsrechnung)
brauchen keinen echten stufenlosen Analogeingang, sondern nur zwei einfache Taster "Hoch" und
"Runter", deren Zustand auf drei feste Sollwerte abgebildet wird: gedrückt "Hoch" → oberer
Wert, gedrückt "Runter" → unterer Wert, keiner gedrückt (bzw. losgelassen) → Neutralwert in der
Mitte. Das ist die digitale Vorstufe zu einem echten Proportional-Joystick — z.B. für ein
Heben/Senken-Funktion mit einem Danfoss-PVEA-Proportionalventil, bei der 25 %/50 %/75 % von
`U_DC` als die drei Sollwerte dienen.

### Funktionsbeschreibung

- **Eingabe:** `I1` (Hoch) und `I2` (Runter) werden wie in `Uebung_001_AX` über `logiBUS_IXA`
  gelesen — deren `IN`-Plug ist ein AX-Adapter (kontinuierlicher Pegel, kein Tastenimpuls).
- **Feste Sollwerte als AR-Konstanten:** drei `initval_AR`-Instanzen liefern `REAL#25.0`,
  `REAL#50.0`, `REAL#75.0` als AR-Adapter-Werte (siehe `Uebung_245_AX` für das Prinzip).
- **Kaskadierte Auswahl:** Es gibt keinen fertigen 3-Wege-AR-Selektor, deshalb zwei
  `AR_AX_SEL_AR` (binäre Auswahl: `G=FALSE`→`IN0`, `G=TRUE`→`IN1`) hintereinander:
  - **Innen** (`AR_AX_SEL_AR_Runter`): `G = I2`. `IN0 = 50` (Neutral), `IN1 = 25` (Runter).
    Ergebnis: 50, solange `I2` losgelassen ist, sonst 25.
  - **Außen** (`AR_AX_SEL_AR_Hoch`): `G = I1`. `IN0` = Ergebnis des inneren Selektors, `IN1 = 75`
    (Hoch). Ergebnis: der innere Wert, solange `I1` losgelassen ist, sonst 75.
- **Ausgabe:** `Q_NumericValue_PHYSA` schreibt das Endergebnis auf `OutputNumber_N3_N`.
- **Priorität bei gleichzeitigem Drücken:** Da `I1`s Selektor der äußere ist, gewinnt "Hoch" bei
  gleichzeitigem Drücken beider Taster (75 statt 25) — eine bewusste, aber willkürliche
  Entscheidung dieser Referenzlösung, keine zwingende Vorgabe. Genau wie bei `Uebung_229_AX`
  ("Last-Wins") ist der Konfliktfall hier explizit dokumentiert statt stillschweigend offen zu
  bleiben.

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_246_AX` an (bereits als Referenzlösung vorhanden).
2. Verdrahten Sie die drei `initval_AR`-Konstanten und die zwei `AR_AX_SEL_AR` wie beschrieben.
3. Testen Sie: `I1` halten → Anzeige 75; loslassen → Anzeige zurück auf 50. `I2` halten → Anzeige
   25; loslassen → Anzeige zurück auf 50. Beide gleichzeitig halten → Anzeige 75 (Hoch gewinnt).
4. Zusatzaufgabe: Tauschen Sie die Reihenfolge der Kaskade (Hoch innen, Runter außen) — wie
   ändert sich das Verhalten bei gleichzeitigem Drücken?

### Referenzlösung

`Uebung_246_AX.SUB`. Verwandte Übungen: `Uebung_001_AX` (`logiBUS_IXA`-Grundmuster),
`Uebung_245_AX` (`initval_AR`, feste AR-Konstanten).
