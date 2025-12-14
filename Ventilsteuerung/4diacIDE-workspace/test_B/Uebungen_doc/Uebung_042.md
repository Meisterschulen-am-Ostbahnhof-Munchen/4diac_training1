# Uebung_042: Scaling Function Block Testing

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines Skalierungs-Funktionsbausteins zur Signalverarbeitung. Der Fokus liegt auf der Umwandlung von Eingangswerten in einen normierten Ausgangsbereich.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### SCALE
- **Typ**: signalprocessing::SCALE
- **Parameter**:
  - IN = 10.0
  - MAX_IN = 20.0
  - MIN_IN = 4.0
  - MAX_OUT = 100.0
  - MIN_OUT = 0.0

## Programmablauf und Verbindungen

Der DigitalInput_CLK_I1 Baustein dient als Eingabequelle und erfasst Einzelklick-Ereignisse eines Tasters. Bei Erkennung eines Tastenklicks wird ein IND-Ereignis ausgelöst, das direkt an den SCALE-Baustein weitergeleitet wird.

Der SCALE-Baustein führt eine lineare Skalierung durch:
- Eingangsbereich: 4.0 bis 20.0
- Ausgangsbereich: 0.0 bis 100.0
- Aktueller Eingangswert: 10.0

Die Skalierungsfunktion transformiert den Eingangswert proportional in den definierten Ausgangsbereich. Bei einem REQ-Ereignis berechnet der Baustein den entsprechenden skalierten Ausgangswert.

**Ereignisverbindung**:
- DigitalInput_CLK_I1.IND → SCALE.REQ

## Zusammenfassung
Diese Übung vermittelt grundlegende Kenntnisse in der Signalverarbeitung und Skalierung von Werten. Sie zeigt die praktische Anwendung eines Skalierungsbausteins zur Normierung von Eingangssignalen auf einen definierten Ausgangsbereich. Die Übung eignet sich für Einsteiger in die Signalverarbeitung mit 4diac.