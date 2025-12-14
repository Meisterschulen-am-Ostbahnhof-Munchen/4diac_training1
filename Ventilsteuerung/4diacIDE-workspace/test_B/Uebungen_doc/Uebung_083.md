# Uebung_083: Beispiel für E_CTUD_UDINT

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CTUD_UDINT-Funktionsbausteins für Zählfunktionen. Das Beispiel zeigt einen Aufwärts-/Abwärts-Zähler mit verschiedenen Steuerungsmöglichkeiten und visueller Ausgabe des Zählerstands.

## Verwendete Funktionsbausteine (FBs)

### E_CTUD_UDINT
- **Typ**: E_CTUD_UDINT (Up/Down Counter)
- **Parameter**: 
  - PV = UINT#5 (Preset Value = 5)

### DigitalInput_CLK_I1 bis CLK_I4
- **Typ**: logiBUS_IE (Digital Input)
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 bis I4
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### DigitalOutput_Q1 und Q2
- **Typ**: logiBUS_QX (Digital Output)
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1 bzw. Output_Q2

### Q_NumericValue
- **Typ**: Q_NumericValue
- **Parameter**:
  - u16ObjId = DefaultPool::OutputNumber_N1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1 (I1) → E_CTUD_UDINT.CU (Count Up)
- DigitalInput_CLK_I2 (I2) → E_CTUD_UDINT.CD (Count Down)
- DigitalInput_CLK_I3 (I3) → E_CTUD_UDINT.R (Reset)
- DigitalInput_CLK_I4 (I4) → E_CTUD_UDINT.LD (Load)

**Ausgangsereignisse:**
- E_CTUD_UDINT.CO (Count Overflow) → DigitalOutput_Q1, DigitalOutput_Q2, Q_NumericValue
- E_CTUD_UDINT.RO (Reset Overflow) → DigitalOutput_Q1, DigitalOutput_Q2, Q_NumericValue
- E_CTUD_UDINT.LDO (Load Overflow) → DigitalOutput_Q1, DigitalOutput_Q2, Q_NumericValue

**Datenverbindungen:**
- E_CTUD_UDINT.QU → DigitalOutput_Q1.OUT (Up Count Status)
- E_CTUD_UDINT.QD → DigitalOutput_Q2.OUT (Down Count Status)
- E_CTUD_UDINT.CV → Q_NumericValue.u32NewValue (Current Counter Value)

**Funktionsweise:**
- I1: Erhöht den Zählerstand um 1 (Aufwärtszählen)
- I2: Verringert den Zählerstand um 1 (Abwärtszählen)
- I3: Setzt den Zähler auf 0 zurück
- I4: Lädt den Preset-Wert (5) in den Zähler
- Der aktuelle Zählerstand wird numerisch auf Q_NumericValue angezeigt
- Q1 und Q2 zeigen den Status des Zählers an

## Zusammenfassung
Diese Übung vermittelt praktische Kenntnisse im Umgang mit dem E_CTUD_UDINT-Zählerbaustein und demonstriert die Integration von digitalen Ein- und Ausgängen sowie numerischen Anzeigen. Das System ermöglicht sowohl manuelle Steuerung über Taster als auch visuelle Rückmeldung über Statusausgänge und numerische Anzeige des Zählerstands.