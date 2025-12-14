# Uebung_002: DigitalInput_I1 auf DigitalOutput_Q1/_Q2

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung digitaler Signale in der 4diac-IDE. Es handelt sich um eine einfache Schaltung, bei der ein digitaler Eingangssignal auf zwei digitale Ausgänge verteilt wird.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalInput_I1** (Typ: logiBUS_IX)
  - Parameter: QI = TRUE
  - Parameter: Input = logiBUS_DI::Input_I1
  - Ereignisausgang: IND
  - Dateneingang: IN

- **DigitalOutput_Q1** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE
  - Parameter: Output = logiBUS_DO::Output_Q1
  - Ereigniseingang: REQ
  - Datenausgang: OUT

- **DigitalOutput_Q2** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE
  - Parameter: Output = logiBUS_DO::Output_Q2
  - Ereigniseingang: REQ
  - Datenausgang: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → DigitalOutput_Q1.REQ
- DigitalInput_I1.IND → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → DigitalOutput_Q1.OUT
- DigitalInput_I1.IN → DigitalOutput_Q2.OUT

**Lernziele:**
- Verständnis der grundlegenden Signalverarbeitung
- Kennenlernen der logiBUS-Komponenten
- Aufbau einfacher Verbindungen zwischen Eingangs- und Ausgangsbausteinen
- Verwendung von Ereignis- und Datenverbindungen

**Schwierigkeitsgrad:** Einfach

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis digitaler Ein- und Ausgänge

**Starten der Übung:**
Die Übung wird durch Aktivieren des DigitalInput_I1 gestartet. Bei einer Statusänderung des Eingangssignals werden beide Ausgänge (Q1 und Q2) synchron aktualisiert.

## Zusammenfassung
Diese Übung zeigt eine grundlegende Signalverteilung, bei der ein digitaler Eingang gleichzeitig zwei digitale Ausgänge ansteuert. Die Verwendung der logiBUS-Komponenten ermöglicht eine einfache Integration mit physischen Ein- und Ausgängen. Die parallele Verarbeitung demonstriert die gleichzeitige Ausführung von Funktionsbausteinen in IEC 61499-Systemen.