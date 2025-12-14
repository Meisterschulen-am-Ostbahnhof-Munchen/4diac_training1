# Uebung_049: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung von digitalen Eingängen mit digitalen Ausgängen in einem 4diac-System. Es werden vier digitale Eingangssignale direkt auf entsprechende digitale Ausgangssignale abgebildet.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1-I4
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_I1 bis Input_I4 (Hardware-Eingänge)
- **Ereignisausgang**: IND (Input Data Event)
- **Datenaustritt**: IN (Eingangswert)

### DigitalOutput_Q1-Q4
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 bis Output_Q4 (Hardware-Ausgänge)
- **Ereigniseingang**: REQ (Request Event)
- **Dateneingang**: OUT (Ausgangswert)

## Programmablauf und Verbindungen

Das Programm besteht aus vier identischen Signalwegen:
- Jeder digitale Eingang (I1-I4) ist direkt mit dem entsprechenden digitalen Ausgang (Q1-Q4) verbunden
- Ereignisverbindungen: IND → REQ (triggert die Ausgabe)
- Datenverbindungen: IN → OUT (überträgt den Signalwert)

**Lernziele**:
- Grundlegende Verwendung von logiBUS-Ein-/Ausgabebausteinen
- Verständnis von Ereignis- und Datenverbindungen
- Direkte Signalweiterleitung in 4diac

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**:
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Basiswissen über Ereignissteuerung

**Starten der Übung**:
1. System in 4diac-IDE öffnen
2. Auf FORTE-Runtime deployen
3. Digitale Eingänge I1-I4 aktivieren
4. Entsprechende Ausgänge Q1-Q4 beobachten

## Zusammenfassung
Diese Übung vermittelt die grundlegende Prinzipien der Signalverarbeitung in 4diac durch direkte Verknüpfung von Eingangs- und Ausgangssignalen. Sie dient als Einstieg in die Verwendung von Hardware-Ein-/Ausgängen und demonstriert das Zusammenspiel von Ereignis- und Datenverbindungen in einem einfachen Steuerungssystem.