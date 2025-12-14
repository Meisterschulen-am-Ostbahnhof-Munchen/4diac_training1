# Uebung_010bA3: Toggle Flip-Flop mit IE AuxFunction2_X1 AuxHeld

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Verbindung mit einer speziellen Auxiliary-Funktion. Der Schwerpunkt liegt auf der Verwendung eines nicht-latchierenden Zweipositionsschalters (AuxFunction2_X1), der bei Betätigung einen Blinkeffekt erzeugt.

## Verwendete Funktionsbausteine (FBs)

### Button_A1
- **Typ**: Aux_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::AuxFunction2_X1
  - InputEvent = AuxiliaryState::AuxHeld

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Funktionsweise:**
Der Aux_IE-Baustein (Button_A1) überwacht den AuxFunction2_X1-Schalter im Zustand "AuxHeld". Bei jeder Betätigung des Schalters wird ein IND-Ereignis ausgelöst, das als Takt (CLK) für den Toggle Flip-Flop (E_T_FF) dient. Der T-FF ändert seinen Ausgangszustand (Q) bei jedem Taktimpuls. Der Ausgangswert wird an die digitale Ausgabe (DigitalOutput_Q1) weitergeleitet, wodurch ein Blinkeffekt entsteht.

**Besonderheit:** Der verwendete AuxFunction2_X1 ist ein nicht-latchierender Zweipositionsschalter (Bool_NonLatched = 2), der nach Loslassen automatisch in die Ausgangsposition zurückkehrt.

**Lernziele:**
- Verständnis der Toggle Flip-Flop Funktionsweise
- Umgang mit Auxiliary-Funktionen und Events
- Implementierung von Blinkfunktionen
- Arbeit mit nicht-latchierenden Schaltern

**Schwierigkeitsgrad:** Einsteiger

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von Ereignis- und Datenverbindungen
- Kenntnisse über digitale Ein- und Ausgänge

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung eines Toggle Flip-Flops in Kombination mit einer Auxiliary-Funktion. Durch die Verwendung des AuxFunction2_X1-Schalters im "AuxHeld"-Zustand wird ein wiederholtes Toggeln des Ausgangs erreicht, was zu einem Blinkeffekt führt. Die Übung vermittelt grundlegende Konzepte der Ereignisverarbeitung und Zustandsänderungen in IEC 61499-Systemen.