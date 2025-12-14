# Uebung_003b2: Funk 16 Tasten auf DataPanel 16

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Ansteuerung eines DataPanels mit 16 Tasten über Funk. Es handelt sich um eine strukturierte Anwendung, die die Verwendung von Sub-Applikationen und die Kommunikation zwischen verschiedenen Hardwarekomponenten zeigt.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_003b2_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: Funk_IX
        - Parameter: QI = TRUE
        - Ereignisausgang: IND
        - Dateneingang: Input
    - **QX**: DataPanel_MI_QX
        - Parameter: QI = TRUE
        - Ereigniseingang: REQ
        - Datenausgang: OUT
        - Dateneingänge: u8SAMember, Output
- **Funktionsweise**: Der Sub-Baustein verbindet einen Funk-Eingang (IX) mit einem DataPanel-Ausgang (QX). Bei einer Statusänderung des Funk-Eingangs wird ein Ereignis ausgelöst, das die Aktualisierung des DataPanel-Ausgangs anstößt.

## Programmablauf und Verbindungen
Die Hauptapplikation besteht aus 15 identischen Sub-Applikationen (F1-F15), die jeweils den Sub-Baustein "Uebung_003b2_sub" instanziieren. Jede Sub-Applikation ist konfiguriert mit:

- **Input**: Funk_DI::DigitalInput_Key_01 (gemeinsamer Funk-Eingang für alle Instanzen)
- **u8SAMember**: MI::MI_00 (SA-Member-Konfiguration)
- **Output**: Unterschiedliche DataPanel-Ausgänge (DigitalOutput_1A bis DigitalOutput_8A)

**Verbindungen:**
- Jede Sub-Applikation empfängt denselben Funk-Eingangssignal
- Die Verarbeitung erfolgt parallel in allen 15 Instanzen
- Jede Instanz steuert einen spezifischen Ausgang am DataPanel an

**Lernziele:**
- Verständnis der Sub-Applikations-Struktur
- Umgang mit parametrisierbaren Funktionsbausteinen
- Parallelverarbeitung von Signalen
- Kommunikation zwischen Funk-Eingängen und DataPanel-Ausgängen

**Schwierigkeitsgrad**: Einfach bis Mittel
**Benötigte Vorkenntnisse**: Grundkenntnisse in 4diac-IDE, Verständnis von Funktionsbausteinen und Event-basierter Programmierung

## Zusammenfassung
Diese Übung zeigt eine skalierbare Lösung zur Ansteuerung mehrerer DataPanel-Ausgänge über einen gemeinsamen Funk-Eingang. Die modulare Struktur mit wiederverwendbaren Sub-Bausteinen ermöglicht eine effiziente und übersichtliche Programmierung. Die parallele Verarbeitung in 15 Instanzen demonstriert die Leistungsfähigkeit der IEC 61499-Architektur für verteilte Steuerungsaufgaben.