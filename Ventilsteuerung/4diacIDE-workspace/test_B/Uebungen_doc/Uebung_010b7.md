# Uebung_010b7: Toggle Flip-Flop mit IE Button_A1 BT_RELEASED_UNLATCHED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Verbindung mit einem Taster. Der T-FF ändert seinen Ausgangszustand bei jedem Tastendruck, was typisch für Toggle-Funktionen in der Digitaltechnik ist.

## Verwendete Funktionsbausteine (FBs)

### Button_IE (Button_A1)
- **Typ**: Button_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::Button_A1 (Button-Identifikation)
  - InputEvent = ButtonActivationCode::BT_RELEASED_UNLATCHED (Taster löst bei Loslassen aus)

### E_T_FF (Toggle Flip-Flop)
- **Typ**: E_T_FF
- **Funktionsweise**: Ändert den Ausgangszustand Q bei jedem ansteigenden Flanke des CLK-Ereigniseingangs

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (Ausgangskanal für die digitale Ausgabe)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK (Tasterereignis löst Flip-Flop aus)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop Ausgangsereignis triggert Ausgabe)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop Zustand wird an Ausgang übertragen)

**Ablauf:**
1. Beim Loslassen des Tasters (BT_RELEASED_UNLATCHED) wird das IND-Ereignis ausgelöst
2. Dieses Ereignis triggert den CLK-Eingang des Toggle Flip-Flops
3. Der E_T_FF ändert seinen Ausgangszustand Q (von 0 auf 1 oder umgekehrt)
4. Das EO-Ereignis wird ausgelöst und triggert die Ausgabe
5. Der Digitalausgang Q1 zeigt den aktuellen Zustand des Flip-Flops an

**Lernziele:**
- Verständnis von Toggle Flip-Flop Funktionsweise
- Umgang mit Tasterereignissen in 4diac
- Ereignisgesteuerte Programmierung
- Digitale Ein-/Ausgabesteuerung

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen digitale Schaltungen

## Zusammenfassung
Diese Übung zeigt eine typische Toggle-Funktion, bei der ein Taster als Eingabe dient und ein digitaler Ausgang den Zustand eines Toggle Flip-Flops anzeigt. Die Implementierung folgt dem ereignisgesteuerten Paradigma der IEC 61499 Norm und demonstriert grundlegende Konzepte der Steuerungstechnik.