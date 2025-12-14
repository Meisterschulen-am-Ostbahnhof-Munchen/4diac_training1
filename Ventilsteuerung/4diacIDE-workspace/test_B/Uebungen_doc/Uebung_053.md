# Uebung_053: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren Ausgabe auf digitale Ausgänge über Byte-Konvertierung. Vier digitale Eingänge werden zu einem Byte zusammengefasst und anschließend wieder in vier separate Ausgangssignale aufgeteilt.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput Bausteine
- **DigitalInput_I1** (Typ: logiBUS_IX)
- **DigitalInput_I2** (Typ: logiBUS_IX) 
- **DigitalInput_I3** (Typ: logiBUS_IX)
- **DigitalInput_I4** (Typ: logiBUS_IX)

### DigitalOutput Bausteine
- **DigitalOutput_Q1** (Typ: logiBUS_QX)
- **DigitalOutput_Q2** (Typ: logiBUS_QX)
- **DigitalOutput_Q3** (Typ: logiBUS_QX)
- **DigitalOutput_Q4** (Typ: logiBUS_QX)

### Sub-Bausteine: ASSEMBLE_BYTE_FROM_BOOLS
- **Typ**: ASSEMBLE_BYTE_FROM_BOOLS
- **Funktionsweise**: Sammelt vier boolesche Eingangssignale und fasst sie zu einem Byte zusammen

### Sub-Bausteine: SPLIT_BYTE_INTO_BOOLS
- **Typ**: SPLIT_BYTE_INTO_BOOLS
- **Funktionsweise**: Teilt ein Byte in vier separate boolesche Ausgangssignale auf

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- Die IND-Ereignisse der vier DigitalInput-Bausteine (I1-I4) triggern den ASSEMBLE_BYTE_FROM_BOOLS Baustein
- Das CNF-Ereignis von ASSEMBLE_BYTE_FROM_BOOLS startet SPLIT_BYTE_INTO_BOOLS
- Das CNF-Ereignis von SPLIT_BYTE_INTO_BOOLS triggert alle vier DigitalOutput-Bausteine (Q1-Q4)

### Datenverbindungen:
- Die Eingangssignale I1-I4 werden als Bits 0-3 an ASSEMBLE_BYTE_FROM_BOOLS übergeben
- Das zusammengesetzte Byte wird von ASSEMBLE_BYTE_FROM_BOOLS an SPLIT_BYTE_INTO_BOOLS weitergeleitet
- Die Bits 0-3 von SPLIT_BYTE_INTO_BOOLS werden an die entsprechenden Ausgänge Q1-Q4 verteilt

### Parameterkonfiguration:
Alle DigitalInput- und DigitalOutput-Bausteine haben den QI-Parameter auf TRUE gesetzt und sind mit den entsprechenden Hardware-Ein-/Ausgängen verbunden.

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Signalverarbeitung in 4diac, insbesondere die Konvertierung zwischen einzelnen booleschen Signalen und Byte-Datenstrukturen. Sie zeigt die praktische Anwendung von Eingangs-/Ausgangsbausteinen und die Verknüpfung von Daten- und Ereignisflüssen in einem Automatisierungssystem.