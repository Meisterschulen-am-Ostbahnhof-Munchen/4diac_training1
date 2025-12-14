# Uebung_071b: WBSD auf UT ausgeben, Q1 Schalten wenn Speed &gt;0

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von radbasierten Maschinendaten. Die Anwendung liest Geschwindigkeits- und Distanzdaten von einem Radsensor aus und steuert einen digitalen Ausgang basierend auf bestimmten Bedingungen.

## Verwendete Funktionsbausteine (FBs)

### I_WBSD
- **Typ**: I_WBSD (Wheel Based Speed/Distance Input)
- **Parameter**: QI = TRUE
- **Funktionsweise**: Liest radbasierte Maschinendaten (Geschwindigkeit und Distanz) ein

### Q_NumberVariable_Wheel_based_machine_speed
- **Typ**: Q_NumericValue
- **Parameter**: u16ObjId = DefaultPool_TECU::NumberVariable_Wheel_based_machine_speed
- **Funktionsweise**: Schreibt die aktuelle Maschinengeschwindigkeit in eine numerische Variable

### Q_NumberVariable_Wheel_based_machine_distance
- **Typ**: Q_NumericValue
- **Parameter**: u16ObjId = DefaultPool_TECU::NumberVariable_Wheel_based_machine_distance
- **Funktionsweise**: Schreibt die aktuelle Maschinendistanz in eine numerische Variable

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**: 
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den digitalen Ausgang Q1

### RangeBasedPulse
- **Typ**: signalprocessing::distance::RangeBasedPulse
- **Parameter**:
  - DIST_HIGH = 5000
  - DIST_LOW = 5000
- **Funktionsweise**: Erzeugt Impulse basierend auf Distanzschwellwerten

### E_D_FF
- **Typ**: E_D_FF (D-Flip-Flop)
- **Funktionsweise**: Speichert den Zustand des digitalen Ausgangs

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- I_WBSD.IND → Q_NumberVariable_Wheel_based_machine_speed.REQ
- I_WBSD.IND → Q_NumberVariable_Wheel_based_machine_distance.REQ
- I_WBSD.IND → RangeBasedPulse.REQ
- RangeBasedPulse.CNF → E_D_FF.CLK
- E_D_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- I_WBSD.WHEELBASEDMACHINESPEED → Q_NumberVariable_Wheel_based_machine_speed.u32NewValue
- I_WBSD.WHEELBASEDMACHINEDISTANCE → Q_NumberVariable_Wheel_based_machine_distance.u32NewValue
- I_WBSD.WHEELBASEDMACHINEDISTANCE → RangeBasedPulse.DIST_IN
- RangeBasedPulse.Q → E_D_FF.D
- E_D_FF.Q → DigitalOutput_Q1.OUT

**Lernziele:**
- Verarbeitung von Sensordaten (Geschwindigkeit und Distanz)
- Verwendung von Distanz-basierten Impulserzeugung
- Steuerung digitaler Ausgänge basierend auf Sensordaten
- Einsatz von Flip-Flops zur Zustandsspeicherung

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundkenntnisse in 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen

## Zusammenfassung
Die Übung zeigt eine typische Anwendung zur Verarbeitung von Maschinendaten, bei der Geschwindigkeits- und Distanzinformationen eines Radsensors ausgelesen, verarbeitet und zur Steuerung eines digitalen Ausgangs verwendet werden. Der RangeBasedPulse-Baustein erzeugt dabei Impulse bei bestimmten Distanzschwellwerten, die über einen D-Flip-Flop den Ausgang Q1 schalten.