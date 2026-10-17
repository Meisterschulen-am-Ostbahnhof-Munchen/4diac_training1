# Optionsmanagement (Libs `Option` und `MyLib_AX_Option`)

Optionale I/O-Gruppen werden zur Laufzeit ueber den Adapter `Option::AOption`
freigeschaltet. Der Adapter fuehrt einen INIT-Request/Confirm-Handshake mit
`QI_OUT` (aktiv/inaktiv).

## Bausteine (`Option-1.0.0/typelib`)

| Baustein | Funktion |
|---|---|
| `selection/AOption_AUI_DEMUX_n`, `AOption_AD_DEMUX_n` | Index `K` waehlt einen von n Ausgaengen `OUTx` |
| `conversion/AOption_X_TO_EVENT` | AOption -> INIT_REQ + `QI_OUT` (Gruppe schaltet sich frei) |
| `conversion/AOption_EVENT_TO_X` | Event -> AOption (z.B. konstantes `QI_OUT=TRUE`, ohne DEMUX) |
| `splitting/AOption_T_2` | T-Stueck: `IN` -> `OUT1`, `OUT2` (OUT2 zuerst aktiv, OUT1 danach) |
| `merging/AOption_OR_2` | Fan-In: `IN1`, `IN2` -> `OUT`, `QI_OUT = IN1 OR IN2` |

Ein DEMUX-Ausgang darf nur an **einen** Socket. Soll ein Ausgang eine Gruppe
und zusaetzlich einen weiteren Baustein speisen, muss ein `AOption_T_2`
dazwischen.

## Optionsgruppen (`MyLib_AX_Option-1.0.0/typelib/sys`)

| SubApp | I/O | AOption |
|---|---|---|
| `OptionalGroup_001` / `_002` | I1/Q1 bzw. I2/Q2 | nur `AOption_IN` |
| `OptionalGroup_001a` / `_002a` | I1/Q1 bzw. I2/Q2 | `AOption_IN` + `AOption_OUT` (Daisy-Chain) |
| `OptionalGroup_001b` | I1/Q1 | nur `AOption_IN`, Endglied einer Kette |
| `DummyGroup` | - | Platzhalter fuer K=1 |

`*a`-Gruppen melden INIT_CNF erst zurueck, wenn die ganze nachgeschaltete
Kette bestaetigt hat.

## Uebungen (`test_AX/Uebungen`)

- `Uebung_094b3_AX`: K=1 Dummy, K=2 Gruppe 001, K=3 Gruppe 002.
- `Uebung_094b3e_AX`: wie b3, zusaetzlich `OptionalGroup_001b`, aktiv bei
  K=2 oder K=3 (je ein `AOption_T_2` hinter DEMUX, dann `AOption_OR_2`);
  bei K=1 (Dummy) bleibt sie aus.
- `Uebung_094b3f_AX`: wie b3e, aber ohne T-Stuecke - `OptionalGroup_001a` und
  `OptionalGroup_002a` reichen ueber `AOption_OUT` an `AOption_OR_2` weiter,
  dessen `OUT` die Gruppe `OptionalGroup_001b` aktiviert.
- `Uebung_094d_AX`: Gruppe ohne DEMUX, immer aktiv (`AOption_EVENT_TO_X`).

## Hinweise

- `001b` nutzt wie `001` die I/O I1/Q1; die Varianten b3e/b3f sind
  Verdrahtungstests (noch nicht auf dem Geraet geprueft).
- `AOption_OR_2` braucht `iec61131-3-bool` (`OR_BOOL_2`); die Abhaengigkeit
  steht in den MANIFEST.MF von `Option` und `MyLib_AX_Option`.
