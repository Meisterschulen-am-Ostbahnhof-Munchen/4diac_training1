# Uebung_089: Beispiel für E_R_TRIG

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert den Unterschied zwischen einem flankengesteuerten Trigger (E_R_TRIG) und einem Event-Switch (E_SWITCH) in der 4diac-IDE. Die Anwendung zeigt, wie diese beiden Bausteine auf Eingangssignale reagieren und Ausgänge steuern.

## Verwendete Funktionsbausteine (FBs)

- **DigitalInput_I1** und **DigitalInput_I2** (Typ: logiBUS_IX)
  - Parameter: QI = TRUE
  - Parameter: Input = logiBUS_DI::Input_I1 bzw. logiBUS_DI::Input_I2
  - Funktion: Lesen digitaler Eingänge vom logiBUS-System

- **OR_2** (Typ: OR_2)
  - Funktion: Logisches ODER-Gatter mit zwei Eingängen

- **E_R_TRIG** (Typ: E_R_TRIG)
  - Funktion: Erkennung steigender Flanke

- **E_T_FF_Q1** und **E_T_FF_1_Q2** (Typ: E_T_FF)
  - Funktion: Toggle-Flipflops

- **E_SWITCH** (Typ: E_SWITCH)
  - Funktion: Event-Weiche

- **DigitalOutput_Q1** und **DigitalOutput_Q2** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE
  - Parameter: Output = logiBUS_DO::Output_Q1 bzw. logiBUS_DO::Output_Q2
  - Funktion: Schalten digitaler Ausgänge am logiBUS-System

## Programmablauf und Verbindungen

**Event-Verbindungen:**
- DigitalInput_I1.IND → OR_2.REQ
- DigitalInput_I2.IND → OR_2.REQ
- OR_2.CNF → E_R_TRIG.EI
- E_R_TRIG.EO → E_T_FF_Q1.CLK
- E_T_FF_Q1.EO → DigitalOutput_Q1.REQ
- OR_2.CNF → E_SWITCH.EI
- E_SWITCH.EO1 → E_T_FF_1_Q2.CLK
- E_T_FF_1_Q2.EO → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → OR_2.IN1
- DigitalInput_I2.IN → OR_2.IN2
- OR_2.OUT → E_R_TRIG.QI
- E_T_FF_Q1.Q → DigitalOutput_Q1.OUT
- OR_2.OUT → E_SWITCH.G
- E_T_FF_1_Q2.Q → DigitalOutput_Q2.OUT

**Besonderheiten:**
- Der E_R_TRIG-Baustein reagiert nur auf echte steigende Flanken
- Der E_SWITCH-Baustein schaltet auch bei anderen Event-Quellen
- Zwei parallele Signalwege zeigen den Unterschied zwischen flankengesteuerter und direkter Event-Verarbeitung

**Schwierigkeitsgrad:** Mittel
**Benötigte Vorkenntnisse:** Grundlagen der 4diac-IDE, digitale Ein-/Ausgänge, Event-Verarbeitung

## Zusammenfassung
Diese Übung verdeutlicht praktisch den Unterschied zwischen flankengesteuerter und direkter Event-Verarbeitung in IEC 61499-Systemen. Die parallele Implementierung mit E_R_TRIG und E_SWITCH ermöglicht einen direkten Vergleich des Verhaltens beider Ansätze und zeigt deren spezifische Einsatzgebiete in der Automatisierungstechnik.