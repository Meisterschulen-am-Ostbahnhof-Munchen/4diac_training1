# Uebung_010b8: Toggle Flip-Flop mit IE Button_A1 BT_PRESSED_LATCHED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-Flip-Flop) in Verbindung mit einem Taster-Eingabemodul. Die Schaltung ermöglicht das Umschalten eines digitalen Ausgangs bei jedem Tastendruck.

## Verwendete Funktionsbausteine (FBs)

### Button_IE (Button_A1)
- **Typ**: Button_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::Button_A1 (Button-Objekt-ID)
  - InputEvent = ButtonActivationCode::BT_PRESSED_LATCHED (verriegelter Tastendruck)

### E_T_FF (Toggle Flip-Flop)
- **Typ**: E_T_FF
- **Funktionsweise**: Ein T-Flip-Flop ändert seinen Ausgangszustand bei jedem anliegenden Taktimpuls (CLK-Ereignis)

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (physikalischer Ausgang Q1)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK (Tasterereignis löst Takt des Flip-Flops aus)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop Ereignis aktiviert Ausgangsanforderung)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop Ausgangszustand wird an digitalen Ausgang weitergeleitet)

**Lernziele:**
- Verständnis der Funktionsweise eines Toggle Flip-Flops
- Implementierung von Tastereingaben mit verriegelten Ereignissen
- Ansteuerung digitaler Ausgänge über das logiBUS-System
- Ereignisgesteuerte Programmabläufe in IEC 61499

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, Verständnis von digitalen Ein-/Ausgängen

**Starten der Übung**: Nach dem Laden der Anwendung wird der Taster A1 bei jedem Druck den Ausgang Q1 umschalten (Ein/Aus).

## Zusammenfassung
Diese Übung zeigt eine grundlegende Toggle-Funktionalität, bei der ein Taster als Taktsignal für einen Flip-Flop dient. Bei jedem Tastendruck wechselt der Ausgang Q1 seinen Zustand, was typische Anwendungen wie Lichtschalter oder Zustandsumschaltungen demonstriert. Die Verwendung von BT_PRESSED_LATCHED gewährleistet eine zuverlässige Erkennung jedes Tastendrucks.