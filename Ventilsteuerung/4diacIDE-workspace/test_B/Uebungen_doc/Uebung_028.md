# Uebung_028: Analog-Eingang

* * * * * * * * * *

## Einleitung
Diese Übung beschäftigt sich mit der Verarbeitung von analogen Eingangssignalen in der 4diac-IDE. Es werden sowohl digitale als auch analoge Eingänge verarbeitet und entsprechende Ausgänge gesteuert.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktionsweise**: Liest digitale Eingangssignale vom Eingang I1 ein

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert digitale Ausgänge am Ausgang Q1

### AnalogInput_I4
- **Typ**: logiBUS_AI_ID
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_AI::AnalogInput_I4
  - AnalogInput_hysteresis = 50
- **Funktionsweise**: Verarbeitet analoge Eingangssignale vom Eingang I4 mit einer Hysterese von 50

### AnalogInput_I7
- **Typ**: logiBUS_AI_ID
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_AI::AnalogInput_I7
  - AnalogInput_hysteresis = 50
- **Funktionsweise**: Verarbeitet analoge Eingangssignale vom Eingang I7 mit einer Hysterese von 50

### F_DWORD_TO_UDINT_I4
- **Typ**: F_DWORD_TO_UDINT
- **Funktionsweise**: Konvertiert DWORD-Daten in UDINT-Datentyp für Eingang I4

### F_DWORD_TO_UDINT_I7
- **Typ**: F_DWORD_TO_UDINT
- **Funktionsweise**: Konvertiert DWORD-Daten in UDINT-Datentyp für Eingang I7

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → DigitalOutput_Q1.REQ
- DigitalInput_I1.IND → AnalogInput_I4.REQ
- DigitalInput_I1.IND → AnalogInput_I7.REQ
- AnalogInput_I4.IND → F_DWORD_TO_UDINT_I4.REQ
- AnalogInput_I4.CNF → F_DWORD_TO_UDINT_I4.REQ
- AnalogInput_I7.IND → F_DWORD_TO_UDINT_I7.REQ
- AnalogInput_I7.CNF → F_DWORD_TO_UDINT_I7.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → DigitalOutput_Q1.OUT
- AnalogInput_I4.IN → F_DWORD_TO_UDINT_I4.IN
- AnalogInput_I7.IN → F_DWORD_TO_UDINT_I7.IN

Das Programm startet mit dem digitalen Eingang I1, der sowohl den digitalen Ausgang Q1 direkt steuert als auch die beiden analogen Eingänge I4 und I7 aktiviert. Die analogen Eingänge verwenden eine Hysterese von 50 zur Signalglättung und konvertieren die analogen Signale über die F_DWORD_TO_UDINT Bausteine in den entsprechenden Datentyp.

## Zusammenfassung
Diese Übung demonstriert die grundlegende Verarbeitung von analogen und digitalen Signalen in 4diac. Sie zeigt die Verwendung von Hysterese-Funktionen bei analogen Eingängen und die notwendige Datentyp-Konvertierung für die weitere Signalverarbeitung. Die Übung eignet sich für Einsteiger in die analoge Signalverarbeitung mit 4diac.