# Uebung_020i: DigitalInput_I1 auf DigitalOutput_Q1; E_PULSE; Impulsformend

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von digitalen Eingangssignalen und die Erzeugung von Impulsen mit konfigurierbarer Dauer. Das System verarbeitet Tastendrücke und Schalterstellungen zur Steuerung von Ausgängen und Zeitmessungen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfasst Einzelklick-Ereignisse von Eingang I1

### DigitalInput_I2
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
- **Funktionsweise**: Liest den digitalen Zustand von Eingang I2

### E_PULSE
- **Typ**: E_PULSE
- **Funktionsweise**: Erzeugt Impulse mit konfigurierbarer Dauer

### E_STOPWATCH
- **Typ**: E_STOPWATCH
- **Funktionsweise**: Führt Zeitmessungen durch

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktionsweise**: Schaltet zwischen verschiedenen Ereignisausgängen basierend auf dem Eingangswert

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den digitalen Ausgang Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_PULSE.REQ (Tastendruck löst Impulserzeugung aus)
- E_PULSE.CNF → DigitalOutput_Q1.REQ (Impulsbestätigung aktiviert Ausgang)
- DigitalInput_I2.IND → E_SWITCH.EI (Eingang I2 triggert Schalter)
- E_SWITCH.EO1 → E_STOPWATCH.START (Schalterposition 1 startet Stoppuhr)
- E_SWITCH.EO0 → E_STOPWATCH.STOP (Schalterposition 0 stoppt Stoppuhr)

**Datenverbindungen:**
- E_PULSE.Q → DigitalOutput_Q1.OUT (Impulssignal an Ausgang Q1)
- E_STOPWATCH.TD → E_PULSE.PT (Stoppuhr-Zeit als Impulsdauer)
- DigitalInput_I2.IN → E_SWITCH.G (Eingang I2 als Schaltersteuerung)

**Lernziele:**
- Verarbeitung von digitalen Eingangssignalen
- Impulserzeugung mit variabler Dauer
- Zeitmessung mit Stoppuhr-Funktionalität
- Ereignisgesteuerte Schaltlogik
- Verwendung von logiBUS-Schnittstellen

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Ein-/Ausgänge, Ereignisverarbeitung

**Start der Übung**: Die Übung wird durch Betätigen des Tasters an Eingang I1 gestartet, wobei die Impulsdauer durch die Stoppuhr gesteuert wird, die über Eingang I2 kontrolliert wird.

## Zusammenfassung
Diese Übung zeigt eine komplexe Steuerung, bei der Tastendrücke und Schalterstellungen kombiniert werden, um zeitgesteuerte Impulse zu erzeugen. Die Integration von Zeitmessung, Impulserzeugung und Schaltlogik demonstriert fortgeschrittene Automatisierungskonzepte in der 4diac-IDE.