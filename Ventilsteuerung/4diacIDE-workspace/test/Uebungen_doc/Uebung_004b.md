# Uebung_004b: Toggle Flip-Flop mit IE / E_SWITCH + E_SR

* * * * * * * * * *

## Einleitung
Diese Übung implementiert ein Toggle Flip-Flop mit Hilfe eines Eingabeereignisbausteins (IE), einem Schalterbaustein (E_SWITCH) und einem Set-Reset-Flipflop (E_SR). Die Schaltung ermöglicht es, durch Betätigen eines Tasters den Ausgangszustand umzuschalten.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfasst Einzelklick-Ereignisse von Taster I1 und gibt diese als IND-Ereignis aus

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktionsweise**: Leitet eingehende Ereignisse basierend auf dem G-Datenwert weiter (EO0 bei G=FALSE, EO1 bei G=TRUE)

### E_SR
- **Typ**: E_SR
- **Funktionsweise**: Set-Reset-Flipflop, das bei S-Ereignis den Ausgang Q auf TRUE setzt und bei R-Ereignis auf FALSE zurücksetzt

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den digitalen Ausgang Q1 basierend auf dem eingehenden OUT-Datenwert

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_SWITCH.EI
- E_SWITCH.EO0 → E_SR.S
- E_SWITCH.EO1 → E_SR.R
- E_SR.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_SR.Q → DigitalOutput_Q1.OUT
- E_SR.Q → E_SWITCH.G

**Ablauf:**
1. Bei jedem Tastendruck auf I1 wird ein IND-Ereignis ausgelöst
2. E_SWITCH leitet das Ereignis zu E_SR.S oder E_SR.R, abhängig vom aktuellen Q-Zustand
3. E_SR toggelt seinen Ausgangszustand bei jedem Ereignis
4. Der neue Zustand wird an den digitalen Ausgang Q1 und zurück an E_SWITCH.G gesendet

**Lernziele:**
- Verständnis von Toggle-Flipflop-Schaltungen
- Umgang mit Ereignis-basierten Funktionsbausteinen
- Implementierung von Zustandsautomaten
- Verwendung von Rückkopplungsschleifen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen

## Zusammenfassung
Diese Übung demonstriert die Realisierung eines Toggle-Flipflops mit standardisierten IEC 61499-Funktionsbausteinen. Die Schaltung nutzt eine Rückkopplung des Ausgangszustands, um bei jedem Tastendruck den Zustand umzuschalten. Die Implementierung zeigt elegante Ereignisverarbeitung und Zustandssteuerung innerhalb des 4diac-Frameworks.