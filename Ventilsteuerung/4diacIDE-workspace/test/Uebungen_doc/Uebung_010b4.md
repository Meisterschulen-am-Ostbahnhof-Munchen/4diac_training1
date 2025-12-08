# Uebung_010b4: SoftKey_F1-8 auf DigitalOutput_Q1-8

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verbindung von Softkeys (F1-F8) mit digitalen Ausgängen (Q1-Q8) in der 4diac-IDE. Die Anwendung zeigt grundlegende Prinzipien der Signalverarbeitung und Bus-Kommunikation in automatisierungstechnischen Systemen.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_010b4_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: Softkey_IX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: IND → QX.REQ
        - Datenausgang/-eingang: IN → QX.OUT, u16ObjId (Eingang)
    - **QX**: logiBUS_QX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: REQ (Eingang von IX.IND)
        - Datenausgang/-eingang: OUT (Eingang von IX.IN), Output (Ausgang)

- **Funktionsweise**: Der Sub-Baustein verbindet einen Softkey-Input (IX) mit einem digitalen Ausgang (QX). Bei Betätigung des Softkeys wird ein Ereignis an den Ausgangsbaustein gesendet, der den entsprechenden digitalen Ausgang schaltet.

## Programmablauf und Verbindungen
Die Hauptanwendung besteht aus 8 identischen Sub-Bausteinen (F1-F8), die jeweils folgende Zuordnungen realisieren:
- F1: SoftKey_F1 → Output_Q1
- F2: SoftKey_F2 → Output_Q2
- F3: SoftKey_F3 → Output_Q3
- F4: SoftKey_F4 → Output_Q4
- F5: SoftKey_F5 → Output_Q5
- F6: SoftKey_F6 → Output_Q6
- F7: SoftKey_F7 → Output_Q7
- F8: SoftKey_F8 → Output_Q8

**Lernziele**:
- Verständnis der Bus-Kommunikation mit logiBUS-Komponenten
- Umgang mit Softkey-Inputs und digitalen Ausgängen
- Parametrierung von Funktionsbausteinen
- Arbeit mit Sub-Applikationen in 4diac

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**:
- Grundlagen der 4diac-IDE
- Verständnis von Ereignis- und Datenverbindungen
- Kenntnisse über Bus-Systeme in der Automation

**Starten der Übung**: Die Anwendung wird in der 4diac-IDE geladen und auf ein kompatibles Zielsystem deployt. Die Softkeys F1-F8 können dann zur Steuerung der entsprechenden digitalen Ausgänge verwendet werden.

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Signalverarbeitung in Automatisierungssystemen. Sie zeigt, wie Softkey-Eingänge mit digitalen Ausgängen verbunden werden können und demonstriert die Verwendung von Bus-Kommunikationsbausteinen. Die modulare Struktur mit wiederverwendbaren Sub-Bausteinen ermöglicht eine skalierbare und wartbare Lösung.