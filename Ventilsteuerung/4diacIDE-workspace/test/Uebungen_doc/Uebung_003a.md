# Uebung_003a: DigitalInput_I1/_I2 auf DigitalOutput_Q1/_I2

* * * * * * * * * *
## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung von digitalen Eingangssignalen zu digitalen Ausgangssignalen in einer 4diac-IDE Anwendung. Es werden zwei unabhängige Signalpfade realisiert, die jeweils einen digitalen Eingang mit einem digitalen Ausgang verbinden.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_003a_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: logiBUS_IX
        - Parameter: QI = TRUE
        - Ereignisausgang: IND
        - Dateneingang: Input
    - **QX**: logiBUS_QX
        - Parameter: QI = TRUE
        - Ereigniseingang: REQ
        - Datenausgang: Output

- **Funktionsweise**: Der Sub-Baustein verbindet einen digitalen Eingang (IX) mit einem digitalen Ausgang (QX). Bei einer Änderung des Eingangssignals (IND-Ereignis) wird das Signal über eine Ereignisverbindung an den Ausgangsbaustein weitergeleitet und das entsprechende Ausgangssignal gesetzt.

## Programmablauf und Verbindungen
Die Hauptanwendung besteht aus zwei Instanzen des Uebung_003a_sub Sub-Bausteins:
- **F1**: Verbindet Input_I1 mit Output_Q1
- **F2**: Verbindet Input_I2 mit Output_Q2

Die Verbindungen erfolgen über:
- Ereignisverbindung: IX.IND → QX.REQ
- Datenverbindung: IX.IN → QX.OUT
- Externe Parameterzuweisung der logiBUS-Schnittstellen

**Lernziele**: 
- Verständnis der grundlegenden Signalverarbeitung
- Umgang mit digitalen Ein- und Ausgängen
- Verwendung von Sub-Applikationen
- Parameterzuweisung für Hardware-Schnittstellen

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Signalen

**Starten der Übung**: Die Anwendung wird nach dem Kompilieren und Laden auf das Zielsystem automatisch aktiv. Die digitalen Eingänge I1 und I2 steuern direkt die entsprechenden Ausgänge Q1 und Q2.

## Zusammenfassung
Diese Übung vermittelt die grundlegenden Prinzipien der Signalverarbeitung in 4diac-IDE durch die direkte Verbindung von digitalen Eingängen mit digitalen Ausgängen. Die Verwendung von Sub-Applikationen ermöglicht eine modulare und wiederverwendbare Programmstruktur. Die beiden unabhängigen Signalpfade demonstrieren die parallele Verarbeitung von Signalen in Echtzeit-Steuerungssystemen.