# Uebung_056: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren Übertragung auf digitale Ausgänge über Byte-Operationen. Die vier digitalen Eingänge I1-I4 werden zu einem Byte zusammengefasst und anschließend wieder in vier separate Ausgangssignale für Q1-Q4 aufgeteilt.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_I1, I2, I3, I4** (Typ: logiBUS_IX)
  - Lesen digitale Eingangssignale von logiBUS
  - Parameter: QI = TRUE (aktiviert), Input = entsprechender logiBUS-Eingang

- **DigitalOutput_Q1, Q2, Q3, Q4** (Typ: logiBUS_QX)
  - Schreiben digitale Ausgangssignale auf logiBUS
  - Parameter: QI = TRUE (aktiviert), Output = entsprechender logiBUS-Ausgang

- **ASSEMBLE_BYTE_FROM_QUARTERS** (Typ: ASSEMBLE_BYTE_FROM_QUARTERS)
  - Fasst vier Quarter-Bytes zu einem kompletten Byte zusammen

- **SPLIT_BYTE_INTO_QUARTERS** (Typ: SPLIT_BYTE_INTO_QUARTERS)
  - Teilt ein Byte in vier Quarter-Bytes auf

### Konvertierungs-Funktionsbausteine:
- **BOOL_TO_Q_I1, I2, I3, I4** (Typ: BOOL_TO_QUARTER)
  - Wandeln BOOL-Werte in Quarter-Bytes um

- **Q_TO_BOOL_Q1, Q2, Q3, Q4** (Typ: QUARTER_TO_BOOL)
  - Wandeln Quarter-Bytes in BOOL-Werte um

- **Q_TO_STR_STATUS**-Bausteine (Typ: QUARTER_TO_STR_STATUS)
  - Konvertieren Quarter-Bytes in String-Status für Anzeigezwecke

## Programmablauf und Verbindungen

### Signalfluss:
1. **Eingangsverarbeitung:**
   - Digitale Eingänge I1-I4 werden über logiBUS_IX-Bausteine gelesen
   - BOOL_TO_QUARTER-Bausteine wandeln die BOOL-Signale in Quarter-Bytes um
   - ASSEMBLE_BYTE_FROM_QUARTERS fasst die vier Quarter-Bytes zu einem Byte zusammen

2. **Byte-Verarbeitung:**
   - Das zusammengesetzte Byte wird an SPLIT_BYTE_INTO_QUARTERS weitergeleitet
   - Dieser Baustein teilt das Byte wieder in vier Quarter-Bytes auf

3. **Ausgangsverarbeitung:**
   - QUARTER_TO_BOOL-Bausteine wandeln die Quarter-Bytes zurück in BOOL-Signale
   - Die BOOL-Signale werden über logiBUS_QX-Bausteine auf die Ausgänge Q1-Q4 geschrieben

### Ereignisverbindungen:
- Die Bausteine sind über CNF (Confirmation) und REQ (Request) Ereignisse verkettet
- Ein durchgängiger Ereignisfluss gewährleistet die synchrone Verarbeitung

### Datenverbindungen:
- IN/OUT-Verbindungen für Signalübertragung
- IB-Verbindungen für Statusinformationen
- QUARTER_BYTE-Verbindungen für die Byte-Zusammensetzung und -Aufteilung

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Signalverarbeitung in IEC 61499-Systemen. Sie zeigt die Umwandlung zwischen verschiedenen Datentypen (BOOL ↔ Quarter-Bytes ↔ Byte) und demonstriert die strukturierte Verkettung von Funktionsbausteinen für komplexere Signalverarbeitungsaufgaben. Die Verwendung von Status-Bausteinen ermöglicht zudem die Visualisierung des Signalflusses.