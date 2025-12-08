# Uebung_010bA2: Toggle Flip-Flop mit IE AuxFunction2_X1 AuxEnabled

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle-Flip-Flops mit einem speziellen Hilfsfunktionstyp (Auxiliary Function Type 2). Der Schwerpunkt liegt auf dem Verhalten von nicht-latchenden Schaltern und deren Ereignisauslösung.

## Verwendete Funktionsbausteine (FBs)

### Button_A1
- **Typ**: Aux_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::AuxFunction2_X1 (verwendet Hilfsfunktion Typ 2)
  - InputEvent = AuxiliaryState::AuxEnabled (reagiert auf Aktivierungsereignis)

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flip-Flop)
- **Funktionsweise**: Wechselt den Ausgangszustand bei jedem Taktsignal

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (Ausgang Q1 des logiBUS)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK (Takteingang des Flip-Flops)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Auslösung der Ausgabaanforderung)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Übertragung des Flip-Flop-Zustands)

**Besonderheiten:**
- Bei Auxiliary Type 2 (Bool_NonLatched) wird das AuxEnabled-Ereignis nicht wiederholt
- Langer Tastendruck erzeugt nur ein Ereignis
- Im Vergleich zu Type 0 (Bool_Latched) mit wiederholten Ereignissen

**Lernziele:**
- Verständnis von Toggle-Flip-Flop-Verhalten
- Unterschied zwischen latching und non-latching Schaltern
- Ereignisbehandlung mit Auxiliary Functions

**Schwierigkeitsgrad**: Einsteiger

## Zusammenfassung
Diese Übung zeigt die praktische Anwendung eines Toggle-Flip-Flops in Verbindung mit einem nicht-latchenden Schalter (Auxiliary Type 2). Der Flip-Flop ändert seinen Zustand bei jedem Tastendruck, unabhängig von der Dauer des Drucks. Die Übung verdeutlicht wichtige Unterschiede in der Ereignisbehandlung verschiedener Schaltertypen.