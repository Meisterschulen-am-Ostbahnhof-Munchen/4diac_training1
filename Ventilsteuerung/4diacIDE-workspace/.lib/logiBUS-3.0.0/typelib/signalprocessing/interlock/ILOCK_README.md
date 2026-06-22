# Interlock-Bausteine – Übersicht & Bewertung

## Bibliothekstypen (7 Typen, 13 Dateien mit AX-Varianten)

| Baustein | Strategie | Dead-Time | Konfliktverhalten | AX |
|---|---|---|---|---|
| `ILOCK_BLOCK` | First-Wins | Nein | Ignoriert | ✓ |
| `ILOCK_BLOCK_PROTECT` | First-Wins | Ja (`DT_PROTECT`) | Ignoriert | ✓ |
| `ILOCK_SWITCH` | Last-Wins | Nein | Schaltet sofort um | ✓ |
| `ILOCK_SWITCH_PROTECT` | Last-Wins | Ja (`DT_PROTECT`) | Schaltet verzögert | ✓ |
| `ILOCK_CONFLICT_TRIP` | First-Wins | Nein | TRIP (Reset nötig) | ✓ |
| `ILOCK_FB_SR` | Set-Dominant Latch | – | AX2-Adapter | ✓ |
| `ILOCK_FB_RS` | Reset-Dominant Latch | – | AX2-Adapter | ✓ |
| `ILOCK_2_E` | Event-gesteuert | Nein | Bistabil/Toggle | ✓ |
| `ILOCK_T_FF` | Toggle-FlipFlop | – | AE2-Adapter, sperrbar | ✓ |

## Details zu jedem Baustein

### ILOCK_BLOCK / ILOCK_BLOCK_AX
Priorisiert den ersten aktiven Eingang. Nachfolgende widersprüchliche Signale werden ignoriert, bis der erste Eingang freigegeben wird.

- **Eingänge**: `EI_UP` (mit `DI_UP:BOOL`), `EI_DOWN` (mit `DI_DOWN:BOOL`)
- **Ausgänge**: `EO_UP` (mit `DO_UP:BOOL`), `EO_DOWN` (mit `DO_DOWN:BOOL`)
- **AX**: Adapter `UP_IN`, `DOWN_IN` (Sockets), `UP_OUT`, `DOWN_OUT` (Plugs, Typ `AX`)

### ILOCK_BLOCK_PROTECT / ILOCK_BLOCK_PROTECT_AX
Wie ILOCK_BLOCK, jedoch mit konfigurierbarer Totzeit (`DT_PROTECT:TIME`, Default `T#50ms`) nach Freigabe eines Signals, bevor eine neue Richtung aktiviert werden kann.

- **Zusätzlicher Eingang**: `DT_PROTECT:TIME`
- **Intern**: Nutzt `iec61499::events::ATimeOut`-Adapter
- **AX**: Adapter-Schnittstelle wie ILOCK_BLOCK_AX

### ILOCK_SWITCH / ILOCK_SWITCH_AX
Priorisiert den letzten aktiven Eingang („Last-Wins"). Schaltet sofort auf die neue Richtung um.

- **Eingänge**: `EI_UP` (mit `DI_UP:BOOL`), `EI_DOWN` (mit `DI_DOWN:BOOL`)
- **Ausgänge**: `EO_UP` (mit `DO_UP:BOOL`), `EO_DOWN` (mit `DO_DOWN:BOOL`)
- **AX**: Adapter-Schnittstelle wie ILOCK_BLOCK_AX

### ILOCK_SWITCH_PROTECT / ILOCK_SWITCH_PROTECT_AX
Wie ILOCK_SWITCH, jedoch mit Schutz-Totzeit (`DT_PROTECT:TIME`, Default `T#50ms`) vor dem Umschalten.

- **Zusätzlicher Eingang**: `DT_PROTECT:TIME`
- **Intern**: Nutzt `iec61499::events::ATimeOut`-Adapter
- **AX**: Adapter-Schnittstelle, zusätzlich mit `DT_PROTECT` auf den Eingangs-Events

### ILOCK_CONFLICT_TRIP / ILOCK_CONFLICT_TRIP_AX
Priorisiert den ersten aktiven Eingang und löst bei Konflikt (beide Eingänge gleichzeitig aktiv) einen TRIP aus. Erfordert RESET zum Zurücksetzen.

- **Eingänge**: `EI_UP` (mit `DI_UP:BOOL`), `EI_DOWN` (mit `DI_DOWN:BOOL`), `EI_RESET`
- **Ausgänge**: `EO_UP`, `EO_DOWN`, `EO_TRIP` (mit `DO_TRIP:BOOL`)
- **AX**: Adapter `UP_IN`, `DOWN_IN`, `TRIP_OUT` (Plugs), `UP_OUT`, `DOWN_OUT` (Plugs), Reset als Event `EI_RESET`

### ILOCK_2_E / ILOCK_2_E_AX
Event-gesteuertes Bistabil und Toggle mit gegenseitiger Verriegelung (abgeleitet von `E_SR`).

- **Eingänge**: `SET1`, `CLK1`, `SET2`, `CLK2`, `R` (alles Events)
- **Ausgänge**: `EO` (mit `OUT1:BOOL`, `OUT2:BOOL`)
- **AX**: Ausgänge als AX-Plugs (`OUT1`, `OUT2`)

### ILOCK_T_FF
Composite-FB für ein verriegelbares Toggle-FlipFlop mit AE2-Adapter-Schnittstelle.

- **Eingänge**: `IND` (Event)
- **Ausgänge**: `EO` (Event, `Q:BOOL`)
- **Adapter**: `PLUG:AE2`, `SOCKET:AE2` (bidirektional)
- **Intern**: `E_SR`, `E_SWITCH`, AE2-Konvertierungsbausteine

## Übungsabdeckung

### Standard-Reihe (test_B)

| Übung | Baustein | Beschreibung |
|---|---|---|
| Uebung_201 | ILOCK_BLOCK | Gegenseitige Verriegelung |
| Uebung_201b | ILOCK_BLOCK | Motor Rechts/Linkslauf mit Low-Side Treiber |
| Uebung_202 | ILOCK_BLOCK_PROTECT | Verriegelung mit Schutzzeit |
| Uebung_202b | ILOCK_BLOCK_PROTECT | Motor Reversierung mit Schutzzeit |
| Uebung_203 | ILOCK_SWITCH | Umschalt-Priorität Last-Wins |
| Uebung_203b | ILOCK_SWITCH | Motor Reversierung Priorität Last-Wins |
| Uebung_204 | ILOCK_CONFLICT_TRIP | Trip bei Konflikt mit Reset |
| Uebung_204b | ILOCK_CONFLICT_TRIP | Motor-Sicherheitsabschaltung mit Reset |
| Uebung_205 | ILOCK_SWITCH_PROTECT | Umschalt-Priorität mit Schutzzeit |
| Uebung_205b | ILOCK_SWITCH_PROTECT | Motor Reversierung Priorität mit Schutzzeit |
| Uebung_206 | ILOCK_T_FF | Verriegelbares Toggle-FlipFlop (2er Kette) |
| Uebung_206b | ILOCK_T_FF | Verriegelbares Toggle-FlipFlop (3er Kette) |
| Uebung_207 | ILOCK_2_E | Event-basiertes Bistabil mit Verriegelung |
| Uebung_208 | ILOCK_FB_SR | Set-Dominantes Latch mit AX2-Verriegelung |
| Uebung_209 | ILOCK_FB_RS | Reset-Dominantes Latch mit AX2-Verriegelung |

### AX-Reihe (test_AX)

| Übung | Baustein |
|---|---|
| Uebung_201_AX | ILOCK_BLOCK_AX |
| Uebung_201b_AX | ILOCK_BLOCK_AX |
| Uebung_202_AX | ILOCK_BLOCK_PROTECT_AX |
| Uebung_202b_AX | ILOCK_BLOCK_PROTECT_AX |
| Uebung_203_AX | ILOCK_SWITCH_AX |
| Uebung_203b_AX | ILOCK_SWITCH_AX |
| Uebung_204_AX | ILOCK_CONFLICT_TRIP_AX |
| Uebung_204b_AX | ILOCK_CONFLICT_TRIP_AX |
| Uebung_205_AX | ILOCK_SWITCH_PROTECT_AX |
| Uebung_205b_AX | ILOCK_SWITCH_PROTECT_AX |
| Uebung_206_AX | ILOCK_T_FF_AX |
| Uebung_207_AX | ILOCK_2_E_AX |
| Uebung_208_AX | ILOCK_FB_SR_AX |
| Uebung_209_AX | ILOCK_FB_RS_AX |

### Nicht in Übungen verwendet
- `ILOCK_T_FF_SR` / `ILOCK_T_FF_SR_AX` — (Varianten ohne eigene Übung)

## Bewertung: Was fehlt?

| Thema | Status |
|---|---|
| 2-Wege-Verriegelung (UP/DOWN) | Vollständig abgedeckt |
| First-Wins / Last-Wins | Beide Strategien vorhanden |
| Schutzzeit (Dead-Time) | Für BLOCK und SWITCH vorhanden |
| Sicherheits-Trip (Konflikt) | Vorhanden (CONFLICT_TRIP) |
| Event-gesteuerte Verriegelung | Vorhanden (ILOCK_2_E) |
| Toggle mit Sperre | Vorhanden (ILOCK_T_FF) |
| **3-Wege-Verriegelung** | **Fehlt** (nur 2-Kanal) |
| **CONFLICT_TRIP mit Dead-Time** | **Fehlt** (Trip hat keinen DT_PROTECT) |
| **QI (Enable/Qualität)-Eingang** | **Fehlt** (kein genereller Freigabe-Eingang) |
| **Entprellung/Hysterese** | **Fehlt** |
| **Rückmeldeüberwachung** | **Fehlt** (keine Aktor-Plausibilisierung) |
| Integration Not-Halt | Bewusst extern (Sicherheitskette) |
| Übungen für ILOCK_2_E | Vollständig abgedeckt |

## Fazit

Für eine Ventilsteuerungs-Schulung bietet die Bibliothek eine solide Abdeckung der 2-kanaligen Verriegelungsszenarien. Die fehlenden Punkte (3-Wege, Trip+Protect, QI, Entprellung) können bei Bedarf ergänzt werden.
prellung) können bei Bedarf ergänzt werden.
