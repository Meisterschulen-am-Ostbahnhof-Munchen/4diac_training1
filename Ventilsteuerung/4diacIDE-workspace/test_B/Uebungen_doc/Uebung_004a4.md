# Uebung_004a4: mit E_SPLIT

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von T-Flipflops in Kombination mit einem Ereignis-Splitter zur Steuerung von digitalen Ausgängen. Die Anwendung zeigt, wie ein einzelnes Eingangsereignis auf mehrere Flipflops verteilt werden kann.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalInput_CLK_I1** (Typ: logiBUS_IE)
  - Eingangsbaustein für Taster-Ereignisse
  - Konfiguriert für Einzelklick-Ereignisse (BUTTON_SINGLE_CLICK)
  - Verbunden mit Eingang I1 der logiBUS-Hardware

- **E_SPLIT** (Typ: E_SPLIT)
  - Ereignisverteiler
  - Teilt ein eingehendes Ereignis auf zwei Ausgänge auf

- **E_T_FF_Q1** und **E_T_FF_Q2** (Typ: E_T_FF)
  - T-Flipflops mit Ereignissteuerung
  - Wechseln ihren Zustand bei jedem Takt-Ereignis

- **DigitalOutput_Q1** und **DigitalOutput_Q2** (Typ: logiBUS_QX)
  - Digitale Ausgabebausteine
  - Steuern die Ausgänge Q1 und Q2 der logiBUS-Hardware

## Programmablauf und Verbindungen

### Ereignisverbindungen:
1. Der Taster-Eingang (DigitalInput_CLK_I1) sendet bei jedem Klick ein IND-Ereignis an E_SPLIT
2. E_SPLIT verteilt das Ereignis gleichzeitig an beide T-Flipflops (E_T_FF_Q1.CLK und E_T_FF_Q2.CLK)
3. Jedes T-Flipflop sendet nach Zustandsänderung ein EO-Ereignis an den entsprechenden Ausgabebaustein

### Datenverbindungen:
- Die Q-Ausgänge der T-Flipflops sind mit den OUT-Eingängen der Digitalausgänge verbunden
- Dadurch wird der aktuelle Zustand der Flipflops direkt an die Hardware-Ausgänge weitergegeben

### Lernziele:
- Verständnis von T-Flipflops und deren Verhalten
- Einsatz von Ereignis-Splittern zur Signalverteilung
- Parallelverarbeitung von Ereignissen
- Steuerung digitaler Ausgänge über Flipflop-Zustände

### Schwierigkeitsgrad:
- Einfach bis mittel

### Benötigte Vorkenntnisse:
- Grundlagen der IEC 61499
- Verständnis von Ereignis- und Datenverbindungen
- Kenntnisse über Flipflop-Funktionalität

### Start der Übung:
Die Übung wird durch Betätigen des Tasters an Eingang I1 gestartet. Jeder Klick wechselt den Zustand beider Ausgänge Q1 und Q2 gleichzeitig.

## Zusammenfassung
Diese Übung zeigt eine einfache aber effektive Anwendung von T-Flipflops in paralleler Schaltung. Durch den Einsatz des E_SPLIT-Bausteins kann ein einzelnes Eingangsereignis synchron auf mehrere Flipflops verteilt werden, was zu einer gleichzeitigen Zustandsänderung der Ausgänge führt. Die Übung vermittelt grundlegende Konzepte der Ereignisverteilung und paralleler Signalverarbeitung in IEC 61499-Systemen.