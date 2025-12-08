# Uebung_055: DigitalInput_I1 auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung eines digitalen Eingangssignals und dessen Ausgabe auf einem digitalen Ausgang. Das System liest den Zustand eines digitalen Eingangs und gibt diesen direkt auf einem digitalen Ausgang aus.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktionsweise**: Liest den Zustand des physischen digitalen Eingangs I1

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Schreibt den empfangenen Wert auf den physischen digitalen Ausgang Q1

### BOOL_TO_Q
- **Typ**: BOOL_TO_QUARTER
- **Funktionsweise**: Konvertiert einen booleschen Wert in das QUARTER-Datenformat

### Q_TO_BOOL
- **Typ**: QUARTER_TO_BOOL
- **Funktionsweise**: Konvertiert einen QUARTER-Wert zurück in einen booleschen Wert

### Q_TO_STR_STATUS
- **Typ**: QUARTER_TO_STR_STATUS
- **Funktionsweise**: Wandelt QUARTER-Daten in einen Status-String für Anzeigezwecke

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → BOOL_TO_Q.REQ
- BOOL_TO_Q.CNF → Q_TO_BOOL.REQ
- BOOL_TO_Q.CNF → Q_TO_STR_STATUS.REQ
- Q_TO_BOOL.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → BOOL_TO_Q.I
- BOOL_TO_Q.QB → Q_TO_BOOL.IB
- BOOL_TO_Q.QB → Q_TO_STR_STATUS.IB
- Q_TO_BOOL.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Bei einer Zustandsänderung am digitalen Eingang I1 wird das IND-Ereignis ausgelöst
2. Der Eingangswert wird über BOOL_TO_Q in das QUARTER-Format konvertiert
3. Der konvertierte Wert wird parallel zu Q_TO_BOOL und Q_TO_STR_STATUS weitergeleitet
4. Q_TO_BOOL wandelt den Wert zurück in einen booleschen Wert
5. Der boolesche Wert wird an den digitalen Ausgang Q1 gesendet
6. Gleichzeitig wird der Status für Anzeigezwecke aufbereitet

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen
**Start der Übung**: Das System startet automatisch und überträgt kontinuierlich den Eingangszustand auf den Ausgang

## Zusammenfassung
Diese Übung vermittelt die grundlegende Handhabung digitaler Ein- und Ausgänge in 4diac. Sie zeigt die Signalverarbeitungskette von der Erfassung eines digitalen Eingangssignals über Datenkonvertierung bis zur Ausgabe auf einem digitalen Ausgang. Die Verwendung von Konvertierungsbausteinen demonstriert die Notwendigkeit von Datentyp-Anpassungen in verteilten Automatisierungssystemen.