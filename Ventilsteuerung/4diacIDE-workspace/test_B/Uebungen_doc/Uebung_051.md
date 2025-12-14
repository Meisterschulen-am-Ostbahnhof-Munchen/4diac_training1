# Uebung_051: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren direkte Ausgabe auf digitale Ausgänge unter Verwendung von Strukturbausteinen. Die Übung zeigt die Anwendung von Multiplex- und Demultiplex-Funktionalitäten in der Automatisierungstechnik.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:

**DigitalInput_I1, DigitalInput_I2, DigitalInput_I3, DigitalInput_I4**
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 bis Input_I4

**DigitalOutput_Q1, DigitalOutput_Q2, DigitalOutput_Q3, DigitalOutput_Q4**
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1 bis Output_Q4

**STRUCT_MUX**
- **Typ**: STRUCT_MUX
- **Parameter**:
  - StructuredType = ST04B

**STRUCT_DEMUX**
- **Typ**: STRUCT_DEMUX
- **Parameter**:
  - StructuredType = ST04B

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- Die IND-Ereignisse aller vier DigitalInput-Bausteine sind mit dem REQ-Eingang von STRUCT_MUX verbunden
- STRUCT_MUX.CNF ist mit STRUCT_DEMUX.REQ verbunden
- STRUCT_DEMUX.CNF ist mit den REQ-Eingängen aller vier DigitalOutput-Bausteine verbunden

### Datenverbindungen:
- Die IN-Datenausgänge der DigitalInput-Bausteine sind mit den entsprechenden Eingängen von STRUCT_MUX verbunden (B_00 bis B_03)
- STRUCT_MUX.OUT ist mit STRUCT_DEMUX.IN verbunden
- Die Ausgänge von STRUCT_DEMUX (B_00 bis B_03) sind mit den OUT-Eingängen der entsprechenden DigitalOutput-Bausteine verbunden

### Funktionsweise:
Die vier digitalen Eingangssignale (I1-I4) werden über STRUCT_MUX zu einer strukturierten Datenstruktur (ST04B) zusammengefasst. Diese strukturierten Daten werden dann über STRUCT_DEMUX wieder in einzelne Signale aufgeteilt und an die entsprechenden digitalen Ausgänge (Q1-Q4) weitergeleitet.

## Lernziele
- Verständnis der Signalverarbeitung mit Multiplex- und Demultiplex-Bausteinen
- Umgang mit strukturierten Datentypen in 4diac
- Implementierung direkter Signalübertragung zwischen Ein- und Ausgängen
- Anwendung der logiBUS-Schnittstellen für digitale Signale

## Schwierigkeitsgrad
Einfach - geeignet für Einsteiger in die 4diac-IDE

## Benötigte Vorkenntnisse
- Grundkenntnisse der 4diac-IDE
- Verständnis digitaler Ein- und Ausgänge
- Basiswissen über Funktionsbausteine

## Zusammenfassung
Diese Übung zeigt eine grundlegende Implementierung zur direkten Übertragung digitaler Eingangssignale auf digitale Ausgänge unter Verwendung von Strukturbausteinen. Die Verwendung von STRUCT_MUX und STRUCT_DEMUX ermöglicht eine strukturierte Datenverarbeitung und demonstriert effiziente Signalweiterleitung in Automatisierungssystemen.