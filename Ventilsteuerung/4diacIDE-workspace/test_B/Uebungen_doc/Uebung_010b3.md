# Uebung_010b3: Toggle Flip-Flop mit IE AuxFunction2_X1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Verbindung mit einer Hilfsfunktion. Das System verwendet einen Ereignis-getriggerten Toggle-Flip-Flop, der durch eine Auxiliary-Funktion angesteuert wird und dessen Ausgangszustand eine digitale Ausgabe schaltet.

## Verwendete Funktionsbausteine (FBs)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Identifier aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zuweisung zum physikalischen Ausgang Q1)

### AuxFunction2_X1_UP
- **Typ**: Aux_IE (Auxiliary Input Event)
- **Parameter**:
  - QI = TRUE (Qualified Identifier aktiviert)
  - u16ObjId = DefaultPool::AuxFunction2_X1 (Objekt-ID der Hilfsfunktion)
  - InputEvent = AuxiliaryState::AuxDisabled_START (Ereignis bei Start der deaktivierten Hilfsfunktion)

### E_T_FF
- **Typ**: E_T_FF (Event-Triggered Toggle Flip-Flop)
- **Parameter**: Keine zusätzlichen Parameter konfiguriert

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- AuxFunction2_X1_UP.IND → E_T_FF.CLK (Hilfsfunktions-Ereignis triggert den Toggle-Flip-Flop)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop Ausgangsereignis fordert Ausgabeschaltung an)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop Ausgangszustand steuert digitale Ausgabe)

**Lernziele:**
- Verständnis der Funktionsweise eines Toggle Flip-Flops
- Implementierung von ereignisgesteuerten Schaltungen
- Integration von Auxiliary-Funktionen in Steuerungsabläufe
- Umgang mit digitalen Ausgabebausteinen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis von Ereignis- und Datenverbindungen
- Basiswissen über Flip-Flop-Schaltungen

**Starten der Übung:**
Die Übung wird durch Aktivieren der Auxiliary-Funktion X1 gestartet. Bei jedem Trigger-Ereignis der Hilfsfunktion toggelt der Flip-Flop seinen Zustand und schaltet die digitale Ausgabe Q1 entsprechend ein oder aus.

## Zusammenfassung
Diese Übung zeigt eine kompakte Implementierung eines Toggle Flip-Flops, der durch eine Auxiliary-Funktion gesteuert wird. Der Flip-Flop ändert bei jedem empfangenen Trigger-Ereignis seinen Zustand und gibt diesen über eine digitale Ausgabe aus. Die Übung vermittelt grundlegende Konzepte der ereignisgesteuerten Programmierung und der Zustandssteuerung in IEC 61499-Systemen.