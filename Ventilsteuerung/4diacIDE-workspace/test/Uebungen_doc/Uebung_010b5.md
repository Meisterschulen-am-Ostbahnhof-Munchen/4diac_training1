# Uebung_010b5: SoftKey_F1-10 auf DigitalOutput_Q1-10

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Zuordnung von Softkeys zu digitalen Ausgängen in der 4diac-IDE. Zehn Softkeys (F1-F10) werden jeweils mit entsprechenden digitalen Ausgängen (Q1-Q10) verbunden, um eine grundlegende Steuerungslogik zu implementieren.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_010b5_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: Softkey_IX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: IND → QX.REQ
        - Datenausgang/-eingang: IN → QX.OUT, u16ObjId (Eingangsparameter)
    - **QX**: logiBUS_QX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: REQ (von IX.IND)
        - Datenausgang/-eingang: OUT (von IX.IN), Output (Eingangsparameter)
- **Funktionsweise**: Der Sub-Baustein verbindet einen Softkey-Input (IX) mit einem digitalen Ausgang (QX). Bei Betätigung des Softkeys wird ein Ereignis an den Ausgangsbaustein gesendet und der Signalzustand übertragen.

## Programmablauf und Verbindungen
Die Übung besteht aus zehn identischen Sub-Applikationen (F1-F10), die jeweils folgende Verbindungen implementieren:
- SoftKey_F1 → Output_Q1
- SoftKey_F2 → Output_Q2
- ...
- SoftKey_F10 → Output_Q10

Jede Sub-Applikation verwendet den generischen Sub-Baustein "Uebung_010b5_sub", der über Parameter konfiguriert wird:
- u16ObjId: Definiert die Object-ID des Softkeys (z.B. "DefaultPool::SoftKey_F1")
- Output: Definiert den Zielausgang (z.B. "logiBUS_DO::Output_Q1")

**Lernziele**:
- Verständnis der Parametrierung von Funktionsbausteinen
- Zuordnung von Eingängen zu Ausgängen
- Arbeit mit Softkeys und digitalen Ausgängen
- Wiederverwendung von Sub-Applikationen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**:
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Kenntnisse über Event- und Datenverbindungen

**Starten der Übung**: Die Übung kann direkt in der 4diac-IDE geladen und auf einem kompatiblen Zielsystem ausgeführt werden. Die Softkeys F1-F10 aktivieren jeweils die entsprechenden digitalen Ausgänge Q1-Q10.

## Zusammenfassung
Diese Übung vermittelt grundlegende Prinzipien der Signalverarbeitung in 4diac durch die direkte Zuordnung von Softkey-Eingängen zu digitalen Ausgängen. Die modulare Struktur mit wiederverwendbaren Sub-Bausteinen zeigt best practices für skalierbare Applikationsentwicklung. Die Parametrierung ermöglicht eine flexible Konfiguration ohne Änderungen an der grundlegenden Logik.