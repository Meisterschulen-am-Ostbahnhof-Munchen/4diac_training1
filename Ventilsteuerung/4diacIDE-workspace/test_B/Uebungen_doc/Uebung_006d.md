# Uebung_006d: SR-Flip-Flop mit 2x IE und Doppelklick.

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines SR-Flip-Flops mit zwei Eingabeereignissen. Besonderheit ist die Verwendung unterschiedlicher Tastendruck-Erkennungen (Einzelklick und Doppelklick) auf demselben physischen Eingang.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_DOUBLE_CLICK
- **Funktionsweise**: Erkennt Doppelklick-Ereignisse auf Eingang I1

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erkennt Einzelklick-Ereignisse auf Eingang I1

### E_SR
- **Typ**: E_SR (SR-Flip-Flop)
- **Funktionsweise**: Setzt den Ausgang Q bei S-Eingang, resetet bei R-Eingang

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den physischen Ausgang Q1 an

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_SR.S (Doppelklick setzt Flip-Flop)
- DigitalInput_CLK_I2.IND → E_SR.R (Einzelklick resetet Flip-Flop)
- E_SR.EO → DigitalOutput_Q1.REQ (Auslöser für Ausgangsaktualisierung)

**Datenverbindungen:**
- E_SR.Q → DigitalOutput_Q1.OUT (Flip-Flop Zustand zum Ausgang)

**Lernziele:**
- Verständnis von SR-Flip-Flops
- Umgang mit verschiedenen Eingabeereignissen
- Verwendung desselben physischen Eingangs für unterschiedliche Funktionen
- Ereignisgesteuerte Programmierung

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignisbausteinen

**Starten der Übung**: Die Übung wird in der 4diac-IDE geladen und auf ein kompatibles Steuerungssystem deployt. Der physische Eingang I1 kann sowohl mit Einzel- als auch Doppelklicks bedient werden.

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung eines SR-Flip-Flops, bei der durch unterschiedliche Tastendruck-Arten (Einzelklick vs. Doppelklick) auf denselben physischen Eingang verschiedene Funktionen ausgelöst werden. Die Flip-Flop-Funktionalität ermöglicht ein speicherndes Verhalten, bei dem der Ausgangszustand durch die zuletzt empfangene Aktion bestimmt wird.