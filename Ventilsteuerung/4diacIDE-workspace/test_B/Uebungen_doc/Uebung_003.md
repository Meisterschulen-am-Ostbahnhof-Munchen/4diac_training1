# Uebung_003: DigitalInput_I1/_I2 auf DigitalOutput_Q1/_I2

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung von digitalen Eingängen mit digitalen Ausgängen in der 4diac-IDE. Es handelt sich um eine einfache Steuerung, bei der zwei digitale Eingangssignale direkt auf zwei entsprechende digitale Ausgänge geschaltet werden.

## Verwendete Funktionsbausteine (FBs)

Die Übung verwendet vier grundlegende Funktionsbausteine:

- **DigitalInput_I1** (Typ: logiBUS_IX)
- **DigitalInput_I2** (Typ: logiBUS_IX) 
- **DigitalOutput_Q1** (Typ: logiBUS_QX)
- **DigitalOutput_Q2** (Typ: logiBUS_QX)

### Baustein-Konfiguration:

**DigitalInput Bausteine:**
- **QI Parameter**: TRUE (aktiviert den Baustein)
- **Input Parameter**: 
  - DigitalInput_I1: logiBUS_DI::Input_I1
  - DigitalInput_I2: logiBUS_DI::Input_I2

**DigitalOutput Bausteine:**
- **QI Parameter**: TRUE (aktiviert den Baustein)
- **Output Parameter**:
  - DigitalOutput_Q1: logiBUS_DO::Output_Q1
  - DigitalOutput_Q2: logiBUS_DO::Output_Q2

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → DigitalOutput_Q1.REQ
- DigitalInput_I2.IND → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → DigitalOutput_Q1.OUT
- DigitalInput_I2.IN → DigitalOutput_Q2.OUT

**Lernziele:**
- Grundlegendes Verständnis der IEC 61499-Funktionsbausteine
- Verknüpfung von Eingängen und Ausgängen
- Umgang mit logiBUS-IO-Bausteinen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad:** Einsteiger

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von digitalen Ein-/Ausgängen
- Basiswissen über Funktionsbausteine

**Starten der Übung:**
Die Übung wird in der 4diac-IDE geladen und auf ein kompatibles Steuerungssystem mit logiBUS-Interface deployed.

## Zusammenfassung
Diese einfache Übung vermittelt die grundlegenden Prinzipien der Signalverarbeitung in 4diac. Sie zeigt, wie digitale Eingangssignale direkt auf Ausgänge weitergeleitet werden können und dient als Basis für komplexere Steuerungsaufgaben. Die klare Trennung von Ereignis- und Datenverbindungen entspricht dem IEC 61499-Standard und bildet die Grundlage für ereignisgesteuerte Steuerungssysteme.