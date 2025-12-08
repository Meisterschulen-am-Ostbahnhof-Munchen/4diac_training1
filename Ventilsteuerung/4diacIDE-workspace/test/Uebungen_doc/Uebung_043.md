# Uebung_043: Scaling Function Block with limits Testing

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Skalierungs-Funktionsbausteins mit Begrenzungen. Der Baustein wandelt Eingangswerte innerhalb eines definierten Bereichs in einen entsprechenden Ausgangsbereich um, wobei zusätzliche Grenzwerte für die Eingangs- und Ausgangssignale berücksichtigt werden.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### SCALE_LIM
- **Typ**: signalprocessing::SCALE_LIM
- **Parameter**:
  - IN = 50.0
  - MAX_IN = 100.0
  - MIN_IN = 0.0
  - MAX_IN_LIM = 99.0
  - MIN_IN_LIM = 1.0
  - MAX_OUT = 85.0
  - MIN_OUT = 30.0
  - MAX_OUT_FIX = 100.0
  - MIN_OUT_FIX = 0.0

## Programmablauf und Verbindungen

Der Programmablauf beginnt mit dem DigitalInput_CLK_I1 Baustein, der auf einen Tastendruck (BUTTON_SINGLE_CLICK) wartet. Bei Erkennung eines Tastendrucks wird ein IND-Ereignis ausgelöst, das direkt an den SCALE_LIM Baustein weitergeleitet wird.

Die Ereignisverbindung erfolgt über:
- DigitalInput_CLK_I1.IND → SCALE_LIM.REQ

Der SCALE_LIM Baustein führt eine Skalierung mit folgenden Eigenschaften durch:
- Eingangsbereich: 0.0 bis 100.0
- Gültiger Eingangsbereich: 1.0 bis 99.0
- Ausgangsbereich: 30.0 bis 85.0
- Fester Ausgangsbereich: 0.0 bis 100.0
- Testwert: 50.0

Die Skalierung berücksichtigt sowohl den normalen Eingangsbereich als auch zusätzliche Grenzwerte, die die tatsächlich verwendeten Werte einschränken.

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit der Signalverarbeitung und Skalierung in 4diac. Sie zeigt, wie Eingangssignale innerhalb definierter Grenzen verarbeitet und in einen gewünschten Ausgangsbereich transformiert werden können. Die Verwendung von Ereignisverbindungen zwischen Funktionsbausteinen demonstriert die ereignisgesteuerte Programmierung im 61499-Standard.