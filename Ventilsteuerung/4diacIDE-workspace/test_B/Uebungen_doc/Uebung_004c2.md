# Uebung_004c2: Toggle Flip-Flop mit IE mit BUTTON_LONG_PRESS_START

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle-Flip-Flops mit spezieller Ereignisauslösung. Die Schaltung verwendet einen langen Tastendruck als Auslöser für den Toggle-Vorgang.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verwendet Digital-Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_LONG_PRESS_START (reagiert auf langen Tastendruck)

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flip-Flop)
- **Funktionsweise**: Wechselt den Ausgangszustand bei jedem eingehenden Clock-Signal

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (steuert Digital-Ausgang Q1)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Ein langer Tastendruck auf Eingang I1 löst das BUTTON_LONG_PRESS_START-Ereignis aus
2. Das Ereignis wird als Clock-Signal an den Toggle-Flip-Flop weitergeleitet
3. Der E_T_FF-Baustein wechselt seinen Ausgangszustand (Q)
4. Der neue Zustand wird an den Digitalausgang Q1 gesendet
5. Die Ausgabe Q1 schaltet entsprechend um (Ein/Aus)

**Lernziele:**
- Verständnis von Toggle-Flip-Flop-Funktionalität
- Umgang mit speziellen Eingabeereignissen (BUTTON_LONG_PRESS_START)
- Aufbau von Ereignis- und Datenverbindungen zwischen FBs

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Digitale Ein- und Ausgänge

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle-Flip-Flops, der durch lange Tastendrücke gesteuert wird. Die Schaltung demonstriert die Verknüpfung von Ereignis-basierten Eingängen mit logischen Schaltfunktionen und deren Ausgabe auf physischen Ausgängen.