# Uebung_003d: DigitalInput_I1/_I2 auf DigitalOutput_Q1/_I2

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung von digitalen Eingängen mit digitalen Ausgängen in der 4diac-IDE. Die Anwendung bildet zwei unabhängige Signalwege ab, bei denen jeweils ein digitaler Eingangswert direkt auf einen entsprechenden digitalen Ausgang geschaltet wird.

## Verwendete Funktionsbausteine (FBs)

Die Übung verwendet vier Haupt-Funktionsbausteine ohne Sub-Bausteine:

- **DigitalInput_I1** (Typ: logiBUS_IX)
- **DigitalInput_I2** (Typ: logiBUS_IX)
- **DigitalOutput_Q1** (Typ: logiBUS_QX)
- **DigitalOutput_Q2** (Typ: logiBUS_QX)

### Bausteindetails:

**DigitalInput Bausteine (logiBUS_IX):**
- **Parameter QI**: TRUE (aktiviert den Baustein)
- **Parameter Input**: Verweis auf physische Eingänge (logiBUS_DI::Input_I1 / Input_I2)
- **Ereignisausgang**: IND (Indication - signalisiert Eingangsänderung)
- **Datenaustgang**: IN (aktueller Eingangswert)

**DigitalOutput Bausteine (logiBUS_QX):**
- **Parameter QI**: TRUE (aktiviert den Baustein)
- **Parameter Output**: Verweis auf physische Ausgänge (logiBUS_DO::Output_Q1 / Output_Q2)
- **Ereigniseingang**: REQ (Request - triggert Ausgabesetzung)
- **Dateneingang**: OUT (Wert für den Ausgang)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → DigitalOutput_Q1.REQ
- DigitalInput_I2.IND → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → DigitalOutput_Q1.OUT
- DigitalInput_I2.IN → DigitalOutput_Q2.OUT

**Lernziele:**
- Grundlegende Verkabelung von Ein- und Ausgängen in 4diac
- Verständnis der Ereignis- und Datenflusssteuerung
- Umgang mit logiBUS-Schnittstellenbausteinen
- Implementierung paralleler Signalwege

**Schwierigkeitsgrad:** Einsteiger

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE Oberfläche
- Verständnis von Funktionsbausteinen
- Basiswissen über Ereignisgesteuerte Systeme

**Starten der Übung:**
Die Anwendung wird automatisch aktiviert, sobald sie auf ein kompatibles Zielsystem geladen wird. Die QI-Parameter sind standardmäßig auf TRUE gesetzt, wodurch alle Bausteine sofort betriebsbereit sind.

## Zusammenfassung
Diese Übung vermittelt die fundamentalen Prinzipien der Signalverarbeitung in 4diac durch direkte Verknüpfung von digitalen Eingängen mit Ausgängen. Die parallele Struktur mit zwei unabhängigen Signalwegen zeigt deutlich das ereignisgesteuerte Paradigma der IEC 61499, bei dem jede Eingangsänderung sofort die entsprechende Ausgangsaktion auslöst. Die Übung bildet eine wichtige Grundlage für komplexere Steuerungsaufgaben.