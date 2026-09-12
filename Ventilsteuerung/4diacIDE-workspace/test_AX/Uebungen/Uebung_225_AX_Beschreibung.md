# Übung 225 AX: Dreieck-Sollwertmarker mit AR-Adapter (reine Adapter-Kette)

## Thema: Virtual-Terminal-Objektpositionierung — reine AR/AI-Adapterkette

Adapter-Variante von [Übung 225](../../test_B/Uebungen/Uebung_225_Beschreibung.md) (test_B): identische Funktion, aber
**vollständig** über Adapter verdrahtet — kein einziges plain Event/DataConnection in der SubApp.
Sollwert-Lesen und Istwert-Schreiben laufen über `NumericValue_PHYSA`/`Q_NumericValue_PHYSA`, die
Dreieck-Bewegung über eine reine Kette generischer Adapter-Bausteine statt eines eigenen
Composite-FBs.

### Verdrahtung

- `Sollwert_N` (`NumericValue_PHYSA`) liest `InputNumber_Sollwert`, liefert den Wert als AR-Plug `rPhys`.
- `Split` (`AR_SPLIT_2`) verteilt diesen einen AR-Wert sauber auf zwei Verbraucher (ein Adapter darf
  nicht direkt auf mehrere Ziele zeigen — siehe `iec61499-creator`-Skill, Regel 8):
  - `Split.OUT2 → Istwert_N.rPhys` — Istwert unverändert zurückschreiben (`Q_NumericValue_PHYSA`).
  - `Split.OUT1 → AR_ADD_2.IN1` — Sollwert in die Center-Addition.
- `AR_ADD_2` addiert den Center-Offset (`initval_AR`, konstant `REAL#42.0`) rein im Adapter-Bereich.
- `AR_TO_AI` konvertiert das Ergebnis von einem AR- (REAL) in ein AI- (INT) Adapter-Signal — die
  Adapter-native Entsprechung von `F_REAL_TO_INT`.
- `Q_ChildPosition_Dreieck` (`Q_ChildPosition_AI`) bewegt das Dreieck: `s16Xposition` kommt von
  `AR_TO_AI.AI_OUT`, `s16Yposition` ist über `initval_AI` (konstant `0`) fest verdrahtet — beide als
  eigener AI-Adapter-Socket statt als plain INT-Eingang.

### Referenzlösung

`Uebung_225_AX.SUB` — validiert gegen `subapptype.xsd`. Verwendete Bausteine:
`isobus::UT::io::NumericValue::NumericValue_PHYSA`, `adapter::events::unidirectional::AR_SPLIT_2`,
`adapter::iec61131::arithmetic::AR_ADD_2`, `adapter::types::unidirectional::AR::initval::initval_AR`,
`adapter::conversion::unidirectional::AR_TO_AI`, `isobus::UT::Q::Q_ChildPosition_AI`,
`adapter::types::unidirectional::AI::initval::initval_AI`, `isobus::UT::Q::Q_NumericValue_PHYSA`.
