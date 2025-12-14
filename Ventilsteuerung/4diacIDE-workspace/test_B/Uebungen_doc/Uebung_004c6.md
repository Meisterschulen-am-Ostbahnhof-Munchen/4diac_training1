# Uebung_004c6: Toggle Flip-Flop mit IE mit BUTTON_MULTIPLE_CLICK (3-fach Klick)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops (T-FF) in Kombination mit einer speziellen Eingabeauswertung. Der Schwerpunkt liegt auf der Erkennung eines 3-fachen Klicks (BUTTON_MULTIPLE_CLICK) an einem digitalen Eingang und der daraus resultierenden Steuerung eines digitalen Ausgangs.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE2
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verwendet Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_MULTIPLE_CLICK (3-fach Klick Erkennung)
  - arg = 3 (Anzahl der Klicks für Auslösung)

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop)
- **Funktionsweise**: Wechselt den Ausgangszustand bei jedem eingehenden Taktimpuls

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (steuert Ausgang Q1)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK (3-fach Klick löst Takt aus)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Toggle-Ergebnis steuert Ausgang)


**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Toggle-Zustand zum Ausgang)

**Lernziele:**
- Verständnis von Toggle Flip-Flops
- Umgang mit speziellen Eingabeereignissen (Mehrfachklick)
- Flip-Flop-Typen (E_T_FF)
- Ereignisgesteuerte Programmierung in 4diac

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der digitalen Schaltungstechnik, Basiswissen 4diac-IDE

**Start der Übung**: Die Übung wird durch Betätigen des Eingangs I1 mit einem 3-fachen Klick gestartet

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Toggle Flip-Flops, das durch einen 3-fachen Tastendruck ausgelöst wird. Die Kombination aus Eingabeereigniserkennung, Flip-Flop-Logik und Ausgabesteuerung vermittelt wichtige Konzepte der ereignisgesteuerten Automatisierungstechnik. Die zusätzliche SR-Flip-Flop-Komponente erweitert die Steuerungsmöglichkeiten und demonstriert die Vernetzung verschiedener Logikbausteine.