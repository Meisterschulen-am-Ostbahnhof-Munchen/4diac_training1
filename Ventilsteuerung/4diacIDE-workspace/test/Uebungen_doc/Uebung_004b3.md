# Uebung_004b3: Toggle Flip-Flop mit IE / Split / Verriegelt

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flop-Systems mit Eingabeereignisverarbeitung und gegenseitiger Verriegelung. Die Schaltung implementiert zwei Flip-Flop-Einheiten, die über Ereignisschalter miteinander verbunden sind und sich gegenseitig beeinflussen.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalInput_CLK_I1** (Typ: logiBUS_IE)
  - Parameter: QI = TRUE, Input = LogiBUS_DI::Input_I1, InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
  - Ereignisausgang: IND
  - Funktion: Verarbeitet Eingabeereignisse von Taster I1

- **DigitalInput_CLK_I2** (Typ: logiBUS_IE)
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I2, InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
  - Ereignisausgang: IND
  - Funktion: Verarbeitet Eingabeereignisse von Taster I2

- **E_SWITCH_I1** (Typ: E_SWITCH)
  - Ereigniseingang: EI
  - Ereignisausgänge: EO0, EO1
  - Dateneingang: G
  - Funktion: Ereignisverteiler basierend auf dem G-Steuersignal

- **E_SWITCH_I2** (Typ: E_SWITCH)
  - Ereigniseingang: EI
  - Ereignisausgänge: EO0, EO1
  - Dateneingang: G
  - Funktion: Ereignisverteiler basierend auf dem G-Steuersignal

- **E_SR_I1** (Typ: E_SR)
  - Ereigniseingänge: S (Set), R (Reset)
  - Ereignisausgang: EO
  - Datenausgang: Q
  - Funktion: Set-Reset Flip-Flop für Ausgang Q1

- **E_SR_I2** (Typ: E_SR)
  - Ereigniseingänge: S (Set), R (Reset)
  - Ereignisausgang: EO
  - Datenausgang: Q
  - Funktion: Set-Reset Flip-Flop für Ausgang Q2

- **DigitalOutput_Q1** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q1
  - Ereigniseingang: REQ
  - Dateneingang: OUT
  - Funktion: Steuert die physische Ausgabe Q1

- **DigitalOutput_Q2** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q2
  - Ereigniseingang: REQ
  - Dateneingang: OUT
  - Funktion: Steuert die physische Ausgabe Q2

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- DigitalInput_CLK_I1.IND → E_SWITCH_I1.EI
- E_SWITCH_I1.EO0 → E_SR_I1.S
- E_SWITCH_I1.EO1 → E_SR_I1.R
- E_SWITCH_I2.EO0 → E_SR_I2.S
- E_SWITCH_I2.EO1 → E_SR_I2.R
- E_SR_I1.EO → DigitalOutput_Q1.REQ
- E_SR_I2.EO → DigitalOutput_Q2.REQ
- DigitalInput_CLK_I2.IND → E_SWITCH_I2.EI
- Kreuzverbindungen: E_SWITCH_I2.EO0 → E_SR_I1.R und E_SWITCH_I1.EO0 → E_SR_I2.R

### Datenverbindungen:
- E_SR_I1.Q → DigitalOutput_Q1.OUT
- E_SR_I1.Q → E_SWITCH_I1.G
- E_SR_I2.Q → E_SWITCH_I2.G
- E_SR_I2.Q → DigitalOutput_Q2.OUT

### Funktionsweise:
Die Schaltung implementiert ein verriegeltes Toggle-System:
1. Bei Betätigung von Taster I1 wird das Ereignis an E_SWITCH_I1 weitergeleitet
2. E_SWITCH_I1 leitet das Ereignis basierend auf dem Zustand von E_SR_I1.Q entweder an S oder R von E_SR_I1
3. Gleichzeitig wird über die Kreuzverbindung der andere Flip-Flop zurückgesetzt
4. Das gleiche Prinzip gilt für Taster I2 und die zweite Flip-Flop-Einheit
5. Die Ausgänge Q1 und Q2 sind somit immer gegensätzlich und verhindern gleichzeitiges Einschalten

**Schwierigkeitsgrad**: Mittel  
**Benötigte Vorkenntnisse**: Grundverständnis von Flip-Flops, Ereignisverarbeitung und Bus-Systemen  
**Start der Übung**: Programm in 4diac-IDE laden und auf entsprechende Hardware deployen

## Zusammenfassung
Diese Übung verdeutlicht die Implementierung eines verriegelten Toggle-Flip-Flop-Systems mit gegenseitiger Ausschaltung. Die Kreuzverbindungen zwischen den beiden Flip-Flop-Einheiten gewährleisten, dass immer nur eine Ausgabe aktiv sein kann, was typische Anwendungsfälle wie Wechselschaltungen oder gegenseitige Verriegelungen abbildet. Die Verwendung von Ereignisschaltern ermöglicht eine flexible Steuerung der Flip-Flop-Zustände basierend auf den aktuellen Ausgabewerten.