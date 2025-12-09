# Uebung_120: Übung zu ISOBUS Name

* * * * * * * * * *

## Einleitung
Diese Übung behandelt die Arbeit mit ISOBUS-Namensfeldern und demonstriert die Verwendung von strukturierten Datentypen in der 4diac-IDE. Die Übung zeigt, wie Namensfelder gesetzt und verarbeitet werden können.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **STRUCT_DEMUX** - Struktur-Demultiplexer für NAMEFIELD_T
- **STRUCT_MUX** - Struktur-Multiplexer für NAMEFIELD_T  
- **STRUCT_DEMUX_1** - Struktur-Demultiplexer für NAMEFIELD_T
- **STRUCT_MUX_1** - Struktur-Multiplexer für NAMEFIELD_T
- **NmSetName** - ISOBUS Namenssetzungs-Baustein
- **NmSetNameField** - ISOBUS Namensfeld-Setzungs-Baustein
- **NmGetCfInfo** - ISOBUS Konfigurationsinformations-Baustein

### Sub-Bausteine: Keine Sub-Bausteine vorhanden

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- STRUCT_MUX.CNF → STRUCT_DEMUX.REQ
- NmSetName.CNF → NmSetNameField.REQ  
- STRUCT_MUX_1.CNF → NmSetName.REQ
- NmSetNameField.CNF → STRUCT_DEMUX_1.REQ

### Datenverbindungen:
- STRUCT_MUX.OUT → STRUCT_DEMUX.IN
- NmSetName → NmSetNameField.au8IsoName
- NmSetNameField → STRUCT_DEMUX_1.IN
- STRUCT_MUX_1.OUT → NmSetName.psNameField

### Programmablauf:
1. Die STRUCT_MUX Bausteine sammeln strukturierte Daten vom Typ NAMEFIELD_T
2. NmSetName verarbeitet die Namensinformationen
3. NmSetNameField setzt die ISOBUS-Namensfelder
4. STRUCT_DEMUX Bausteine verteilen die strukturierten Daten
5. NmGetCfInfo steht für zusätzliche Konfigurationsinformationen bereit

## Lernziele
- Verständnis der ISOBUS-Namensfeldverarbeitung
- Umgang mit strukturierten Datentypen in 4diac
- Arbeit mit Multiplexer- und Demultiplexer-Bausteinen
- Implementierung von ISOBUS-spezifischen Funktionen

## Schwierigkeitsgrad
Mittel - Grundkenntnisse in 4diac und ISOBUS-Standards werden vorausgesetzt

## Vorkenntnisse
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen und Ereignissteuerung
- Grundkenntnisse über ISOBUS-Standards

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen im Umgang mit ISOBUS-Namensfeldern und strukturierten Datentypen. Sie zeigt die Integration von ISOBUS-spezifischen Funktionalitäten in 4diac-Applikationen und demonstriert den Datenfluss zwischen verschiedenen Funktionsbausteinen zur Namensverwaltung in ISOBUS-Systemen.