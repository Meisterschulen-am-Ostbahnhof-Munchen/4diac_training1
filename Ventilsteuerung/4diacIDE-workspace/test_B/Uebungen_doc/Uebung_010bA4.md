# Uebung_010bA4: Toggle Flip-Flop mit IE AuxFunction2_X1 AuxHeld_START

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Verbindung mit einer speziellen Tasterfunktion. Der Schwerpunkt liegt auf der Verwendung eines Hilfsfunktionstasters, der nur einmalig ein Ereignis sendet, unabhängig von der Betätigungsart.

## Verwendete Funktionsbausteine (FBs)

### Button_A1
- **Typ**: Aux_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::AuxFunction2_X1 (verwendet Hilfsfunktion 2)
  - InputEvent = AuxiliaryState::AuxHeld_START (reagiert auf START-Haltedruck)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop mit Ereignissteuerung)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Ausgang)
  - Output = logiBUS_DO::Output_Q1 (weist Ausgang Q1 zu)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK (Tasterereignis triggert Flip-Flop)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop Ausgangsereignis aktiviert Ausgang)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop Zustand wird an Ausgang Q1 weitergeleitet)

**Besonderheiten:**
- Der AuxHeld_START Event wird nur einmalig gesendet, unabhängig davon, wie der Taster betätigt wird
- Der Toggle Flip-Flop ändert seinen Zustand bei jedem eingehenden Taktimpuls
- Die Ausgabe Q1 schaltet bei jedem Tastendruck zwischen Ein und Aus

**Lernziele:**
- Verständnis von Toggle Flip-Flop Funktionsweise
- Umgang mit speziellen Tasterfunktionen (Auxiliary Functions)
- Ereignisgesteuerte Programmierung in 4diac

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen über Funktionsbausteine

**Starten der Übung**: Nach dem Laden der Anwendung wird der Ausgang Q1 durch Betätigen des START-Tasters (AuxFunction2_X1) getoggelt.

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops mit ereignisgesteuerter Ausgabe. Der spezielle Auxiliary-Taster ermöglicht eine zuverlässige Triggerung unabhängig von der Betätigungsdauer. Die einfache Schaltung demonstriert grundlegende Prinzipien der speichernden Schaltungen in der Automatisierungstechnik.