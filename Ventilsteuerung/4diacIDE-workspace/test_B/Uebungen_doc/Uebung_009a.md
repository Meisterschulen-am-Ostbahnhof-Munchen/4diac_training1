# Uebung_009a: RampLimitFS

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Anwendung eines Rampenbegrenzungs-Funktionsbausteins (RampLimitFS) zur Steuerung eines numerischen Wertes. Das System ermöglicht es, einen Ausgabewert schrittweise zu erhöhen oder zu verringern, wobei zwischen langsamen und schnellen Änderungsraten unterschieden wird.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **RampLimitFS** (signalprocessing::RampLimitFS)
  - Parameter: 
    - VAL_ZERO = DINT#0
    - SLOW = DINT#1
    - FAST = DINT#10
    - VAL_FULL = DINT#100

- **Q_NumericValue** (Q_NumericValue)
  - Parameter: u16ObjId = DefaultPool::OutputNumber_N1

- **F_DINT_TO_UDINT** (F_DINT_TO_UDINT)
  - Datentyp-Konvertierungsbaustein

- **logiBUS_IE** Bausteine (Eingabebausteine):
  - ZERO (Input_I1, BUTTON_SINGLE_CLICK)
  - UP_SLOW (Input_I2, BUTTON_SINGLE_CLICK)
  - UP_FAST (Input_I2, BUTTON_LONG_PRESS_START)
  - DOWN_SLOW (Input_I3, BUTTON_SINGLE_CLICK)
  - DOWN_FAST (Input_I3, BUTTON_LONG_PRESS_START)
  - FULL (Input_I4, BUTTON_SINGLE_CLICK)

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- Tasterereignisse werden an den RampLimitFS-Baustein weitergeleitet:
  - ZERO.IND → RampLimitFS.ZERO
  - UP_SLOW.IND → RampLimitFS.UP_SLOW
  - UP_FAST.IND → RampLimitFS.UP_FAST
  - DOWN_SLOW.IND → RampLimitFS.DOWN_SLOW
  - DOWN_FAST.IND → RampLimitFS.DOWN_FAST
  - FULL.IND → RampLimitFS.FULL

- Signalverarbeitungskette:
  - RampLimitFS.CNF → F_DINT_TO_UDINT.REQ
  - F_DINT_TO_UDINT.CNF → Q_NumericValue.REQ

### Datenverbindungen:
- RampLimitFS.OUT → F_DINT_TO_UDINT.IN
- F_DINT_TO_UDINT.OUT → Q_NumericValue.u32NewValue

### Bedienung:
- **I1 (ZERO)**: Setzt den Wert auf 0
- **I2 Kurzdruck (UP_SLOW)**: Erhöht langsam um 1
- **I2 Langdruck (UP_FAST)**: Erhöht schnell um 10
- **I3 Kurzdruck (DOWN_SLOW)**: Verringert langsam um 1
- **I3 Langdruck (DOWN_FAST)**: Verringert schnell um 10
- **I4 (FULL)**: Setzt den Wert auf 100

Der Wertebereich ist auf 0-100 begrenzt, wobei die Änderungsraten durch die Parameter SLOW und FAST definiert sind.

## Zusammenfassung

Diese Übung vermittelt die Anwendung von Rampenbegrenzungsfunktionen in der Automatisierungstechnik. Sie zeigt, wie unterschiedliche Eingabesignale (Kurz- und Langdruck) verschiedene Geschwindigkeiten der Wertänderung auslösen können. Die Übung demonstriert zudem die Datenkonvertierung zwischen verschiedenen Integer-Datentypen und die Ausgabe von numerischen Werten auf einem Display.