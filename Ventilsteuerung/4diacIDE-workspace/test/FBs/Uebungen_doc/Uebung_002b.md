# Uebung_002b

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren logische Verknüpfung zur Steuerung eines digitalen Ausgangs. Die Schaltung kombiniert UND- sowie ODER-Verknüpfungen mit Signalverarbeitung.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalInput_I1** (Typ: logiBUS_IX)
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I1
  - Ereigniseingang: -
  - Ereignisausgang: IND
  - Dateneingang: -
  - Datenausgang: IN

- **DigitalInput_I2** (Typ: logiBUS_IX)
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I2
  - Ereigniseingang: -
  - Ereignisausgang: IND
  - Dateneingang: -
  - Datenausgang: IN

- **DigitalInput_I3** (Typ: logiBUS_IX)
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I3
  - Ereigniseingang: -
  - Ereignisausgang: IND
  - Dateneingang: -
  - Datenausgang: IN

- **AND_2** (Typ: AND_2)
  - Ereigniseingang: REQ
  - Ereignisausgang: CNF
  - Dateneingänge: IN1, IN2
  - Datenausgang: OUT

- **OR_2** (Typ: OR_2)
  - Ereigniseingang: REQ
  - Ereignisausgang: CNF
  - Dateneingänge: IN1, IN2
  - Datenausgang: OUT

- **BOOL2BOOL** (Typ: BOOL2BOOL)
  - Ereigniseingang: REQ
  - Ereignisausgang: CNF
  - Dateneingang: IN
  - Datenausgang: OUT

- **DigitalOutput_Q1** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q1
  - Ereigniseingang: REQ
  - Ereignisausgang: -
  - Dateneingang: OUT
  - Datenausgang: -

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- DigitalInput_I1.IND → AND_2.REQ
- DigitalInput_I2.IND → AND_2.REQ
- DigitalInput_I3.IND → OR_2.REQ
- AND_2.CNF → BOOL2BOOL.REQ
- BOOL2BOOL.CNF → OR_2.REQ
- OR_2.CNF → DigitalOutput_Q1.REQ

### Datenverbindungen:
- DigitalInput_I1.IN → AND_2.IN1
- DigitalInput_I2.IN → AND_2.IN2
- AND_2.OUT → BOOL2BOOL.IN
- BOOL2BOOL.OUT → OR_2.IN1
- DigitalInput_I3.IN → OR_2.IN2
- OR_2.OUT → DigitalOutput_Q1.OUT

### Funktionsweise:
Die drei digitalen Eingänge I1, I2 und I3 werden verarbeitet:
- I1 und I2 werden durch eine UND-Verknüpfung (AND_2) kombiniert
- Das Ergebnis der UND-Verknüpfung wird durch BOOL2BOOL verarbeitet
- Das verarbeitete Signal wird mit Eingang I3 durch eine ODER-Verknüpfung (OR_2) kombiniert
- Das Endergebnis steuert den digitalen Ausgang Q1

**Schwierigkeitsgrad**: Einfach  
**Benötigte Vorkenntnisse**: Grundverständnis von logischen Verknüpfungen und 4diac-IDE  
**Start der Übung**: Das Programm wird automatisch ausgeführt, sobald es in der 4diac-Runtime geladen ist

## Zusammenfassung
Diese Übung vermittelt grundlegende Kenntnisse in der Verknüpfung digitaler Signale mit logischen Operationen. Sie zeigt die Kombination von UND- und ODER-Verknüpfungen sowie die Signalverarbeitungskette von Eingängen über Verarbeitungsbausteine bis zum Ausgang.