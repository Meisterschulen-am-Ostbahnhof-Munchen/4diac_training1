# Uebung_010bA: Toggle Flip-Flop mit IE Button_A1 BT_STILL_HELD

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops mit einem speziellen Tasterereignis. Der Fokus liegt auf der Verwendung des BT_STILL_HELD_START-Events, das nur einmal bei längerem Drücken des Tasters ausgelöst wird.

## Verwendete Funktionsbausteine (FBs)

### Button_A1
- **Typ**: Button_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::Button_A1 (Taster-Objekt-ID)
  - InputEvent = ButtonActivationCode::BT_STILL_HELD_START (Ereignis bei längerem Drücken)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop)
- **Funktionsweise**: Wechselt den Ausgangszustand bei jedem Takt-Ereignis

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (Ausgangsadresse)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK (Tasterereignis triggert Toggle Flip-Flop)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Ausgangsereignis aktiviert Ausgang)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop Zustand wird an Ausgang weitergeleitet)

**Besonderheit:** Das BT_STILL_HELD_START-Event wird nicht wiederholt - langes Drücken des Tasters erzeugt nur ein einziges Ereignis.

**Schwierigkeitsgrad:** Einfach
**Benötigte Vorkenntnisse:** Grundlagen der IEC 61499, Funktionsbausteine, Ereignisverarbeitung

**Starten der Übung:** Nach dem Laden der Anwendung wird der Taster A1 aktiviert. Bei längerem Drücken des Tasters wechselt der Ausgang Q1 seinen Zustand.

## Zusammenfassung
Diese Übung verdeutlicht die Funktionsweise eines Toggle Flip-Flops in Kombination mit einem speziellen Tasterereignis. Der BT_STILL_HELD_START-Modus ermöglicht eine zuverlässige Zustandsänderung bei längerem Tastendruck ohne unerwünschte Mehrfachauslösungen. Die Übung zeigt grundlegende Prinzipien der Ereignisverarbeitung und Zustandssteuerung in IEC 61499-Systemen.