# Uebung_004c3: Toggle Flip-Flop mit IE mit BUTTON_LONG_PRESS_UP

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops mit spezieller Ereignisauslösung. Das System verwendet einen langen Tastendruck als Auslöser für den Toggle-Vorgang.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verwendet digitalen Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_LONG_PRESS_UP (reagiert auf Loslassen nach langem Tastendruck)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop mit Ereignissteuerung)
- **Funktionsweise**: Wechselt den Ausgangszustand bei jedem eingehenden CLK-Ereignis

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

**Ablauf:**
1. Ein langer Tastendruck auf Eingang I1 wird erkannt
2. Beim Loslassen der Taste (BUTTON_LONG_PRESS_UP) sendet DigitalInput_CLK_I1 ein IND-Ereignis
3. Dieses Ereignis triggert den CLK-Eingang des Toggle Flip-Flops
4. Der E_T_FF wechselt seinen Ausgangszustand (Q)
5. Das EO-Ereignis aktiviert die Ausgabe an DigitalOutput_Q1
6. Der neue Zustand wird an Ausgang Q1 geschrieben

**Lernziele:**
- Verständnis von Toggle Flip-Flops
- Umgang mit speziellen Eingabeereignissen (BUTTON_LONG_PRESS_UP)
- Ereignisgesteuerte Programmierung in 4diac

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Ein- und Ausgänge

**Starten der Übung**: Das System wird automatisch aktiviert (QI=TRUE) und wartet auf langen Tastendruck an I1

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops mit ereignisbasierter Steuerung. Besonders hervorzuheben ist die Verwendung des BUTTON_LONG_PRESS_UP-Ereignisses, das eine robuste Bedienung durch Vermeidung von versehentlichen Kurzimpulsen ermöglicht. Die Übung vermittelt grundlegende Konzepte der ereignisgesteuerten Automatisierungstechnik.