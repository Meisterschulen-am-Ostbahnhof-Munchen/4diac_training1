# Uebung_010b2: Toggle Flip-Flop mit IE SoftKey_F1 SK_RELEASED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Verbindung mit einer Softkey-Eingabe. Der Schaltzustand wird bei jedem Loslassen der F1-Taste umgeschaltet und an einen digitalen Ausgang weitergeleitet.

## Verwendete Funktionsbausteine (FBs)

### SoftKey_UP_F1
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::SoftKey_F1 (verwendet Softkey F1)
  - InputEvent = SoftKeyActivationCode::SK_RELEASED (reagiert auf Tastenloslassen)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop mit Ereigniseingang)
- **Funktionsweise**: Schaltet den Ausgang Q bei jedem eingehenden Takt-Ereignis (CLK) um

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (weist Ausgang Q1 zu)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → E_T_FF.CLK (Tastenloslassen löst Takt aus)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop Ereignis löst Ausgangsanforderung aus)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop Zustand wird an Ausgang Q1 weitergeleitet)

**Lernziele:**
- Verständnis des Toggle Flip-Flop Prinzips
- Umgang mit Softkey-Ereignissen (SK_RELEASED)
- Kombination von Ereignis- und Datenverbindungen
- Ansteuerung digitaler Ausgänge

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignisgesteuerten Funktionsbausteinen

**Starten der Übung**: Nach dem Laden der Anwendung wird durch Loslassen der F1-Taste der Ausgang Q1 getoggelt.

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops, der durch Softkey-Ereignisse gesteuert wird. Der Schaltzustand wechselt bei jedem Loslassen der F1-Taste und wird visuell durch den digitalen Ausgang Q1 dargestellt. Die Übung vermittelt grundlegende Konzepte der ereignisgesteuerten Programmierung und der Zustandssteuerung in IEC 61499-Systemen.