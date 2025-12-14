# Uebung_006b: RS-Flip-Flop mit 2x IE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines RS-Flip-Flops mit zwei Eingabe-Ereignisbausteinen. Im Vergleich zur ähnlichen Übung 006 wird hier ein RS-Flip-Flop anstelle eines SR-Flip-Flops verwendet.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_RS
- **Typ**: E_RS (RS-Flip-Flop)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I2.IND → E_RS.S (Set-Eingang)
- DigitalInput_CLK_I1.IND → E_RS.R (Reset-Eingang)
- E_RS.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_RS.Q → DigitalOutput_Q1.OUT

**Funktionsweise:**
Die Übung verwendet zwei digitale Eingänge (I1 und I2), die als Taster mit Einzelklick-Erkennung konfiguriert sind. Eingang I2 steuert den Set-Eingang (S) des RS-Flip-Flops, während Eingang I1 den Reset-Eingang (R) kontrolliert. Der Ausgang Q des Flip-Flops wird an den digitalen Ausgang Q1 weitergeleitet.

**Lernziele:**
- Verständnis der Funktionsweise eines RS-Flip-Flops
- Umgang mit Ereignis-gesteuerten Funktionsbausteinen
- Unterschied zwischen RS- und SR-Flip-Flops
- Anwendung von digitalen Ein- und Ausgängen in 4diac

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Flip-Flops

**Starten der Übung**: Das Programm wird nach dem Kompilieren und Übertragen auf das Zielsystem automatisch gestartet. Die Taster I1 und I2 können zur Steuerung des Flip-Flops verwendet werden.

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit einem RS-Flip-Flop in einer ereignisgesteuerten Steuerungsumgebung. Die Verwendung von zwei separaten Eingängen für Set- und Reset-Funktionen ermöglicht eine klare Demonstration des Flip-Flop-Verhaltens und zeigt den Unterschied zu ähnlichen Schaltungen wie dem SR-Flip-Flop.