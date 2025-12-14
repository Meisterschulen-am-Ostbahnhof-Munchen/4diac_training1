# Uebung_004c4: Toggle Flip-Flop mit IE mit BUTTON_LONG_PRESS_HOLD

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Kombination mit einem speziellen Eingabeereignis. Der Schwerpunkt liegt auf der Verwendung eines langen Tastendrucks als Trigger für den Toggle-Vorgang.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verwendet digitalen Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_LONG_PRESS_HOLD (reagiert auf langen Tastendruck)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop mit Ereignissteuerung)
- **Funktionsweise**: Wechselt seinen Ausgangszustand bei jedem eingehenden Clock-Ereignis

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (steuert digitalen Ausgang Q1)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Bei langem Druck auf Taste I1 (BUTTON_LONG_PRESS_HOLD) wird ein IND-Ereignis ausgelöst
2. Dieses Ereignis triggert den CLK-Eingang des Toggle Flip-Flops
3. Der E_T_FF wechselt seinen Ausgangszustand Q
4. Das EO-Ereignis des Flip-Flops aktiviert die Ausgabeanforderung an DigitalOutput_Q1
5. Der aktuelle Zustand Q wird an den digitalen Ausgang Q1 übertragen

**Lernziele:**
- Verständnis von Toggle Flip-Flops
- Umgang mit speziellen Eingabeereignissen (BUTTON_LONG_PRESS_HOLD)
- Ereignisgesteuerte Programmierung in 4diac
- Verbindung von Eingabe-, Verarbeitungs- und Ausgabebausteinen

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Ein- und Ausgänge

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops, der durch langen Tastendruck gesteuert wird. Der Ausgang Q1 wechselt bei jedem langen Druck auf Taste I1 seinen Zustand, was typische Anwendungen wie Ein-/Ausschaltfunktionen oder Zustandswechsel demonstriert. Die Verwendung des BUTTON_LONG_PRESS_HOLD-Ereignis ermöglicht eine robuste Bedienung ohne versehentliches Toggeln bei kurzen Tastendrücken.