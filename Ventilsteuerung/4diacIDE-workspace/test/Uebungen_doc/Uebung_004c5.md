# Uebung_004c5: Toggle Flip-Flop mit IE mit BUTTON_PRESS_END

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) mit spezifischer Ereignisauslösung. Der Schwerpunkt liegt auf der Verwendung eines Eingabeereignisses (BUTTON_PRESS_END) zur Steuerung des Toggle-Verhaltens.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verwendet digitalen Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_PRESS_END (löst bei Tastenloslass-Ereignis aus)

### E_T_FF
- **Typ**: E_T_FF (Ereignisgesteuerter Toggle Flip-Flop)
- **Ereigniseingang**: CLK (Clock-Eingang)
- **Ereignisausgang**: EO (Ereignisausgang)
- **Datenausgang**: Q (Ausgangswert des Flip-Flops)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (steuert digitalen Ausgang Q1 an)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Beim Loslassen einer Taste an Eingang I1 wird das BUTTON_PRESS_END-Ereignis ausgelöst
2. Dieses Ereignis triggert den Clock-Eingang des Toggle Flip-Flops
3. Der E_T_FF wechselt seinen Ausgangszustand (Q) bei jedem Ereignis
4. Der neue Zustand wird an den Digitalausgang Q1 weitergeleitet
5. Die LED an Ausgang Q1 ändert bei jedem Tastendruck ihren Zustand (Ein/Aus)

**Lernziele:**
- Verständnis von Toggle Flip-Flops
- Umgang mit spezifischen Eingabeereignissen
- Ereignisgesteuerte Programmierung in 4diac
- Verbindung von digitalen Ein- und Ausgängen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der digitalen Schaltungen, Basiswissen 4diac-IDE

**Starten der Übung**: Programm in 4diac-IDE laden und auf logi.CORE oder ähnliche Hardware deployen

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops mit ereignisgesteuerter Auslösung. Der BUTTON_PRESS_END-Event ermöglicht ein zuverlässiges Toggeln des Ausgangszustands bei jedem Tastenloslassen, was typische Anwendungsfälle wie Schaltfunktionen oder Zustandswechsel abbildet.