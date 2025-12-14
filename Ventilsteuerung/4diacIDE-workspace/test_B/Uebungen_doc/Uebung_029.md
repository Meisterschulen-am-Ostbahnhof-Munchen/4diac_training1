# Uebung_029: LED_DO Blinkende LED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung von LEDs mit unterschiedlichen Blinkfrequenzen über digitale Eingänge. Es werden drei unabhängige LED-Schaltungen implementiert, die jeweils durch separate digitale Eingänge aktiviert werden können.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

**logiBUS_LED_DO_QX** (3 Instanzen)
- **LED_Q1_5HZ**: LED mit 5 Hz Blinkfrequenz
- **LED_Q1_1HZ**: LED mit 1 Hz Blinkfrequenz  
- **LED_Q1_ON**: Dauerhaft leuchtende LED

**logiBUS_IX** (3 Instanzen)
- **DigitalInput_I1**: Digitaler Eingang I1
- **DigitalInput_I2**: Digitaler Eingang I2
- **DigitalInput_I3**: Digitaler Eingang I3

## Programmablauf und Verbindungen

### Event-Verbindungen:
- DigitalInput_I1.IND → LED_Q1_5HZ.REQ
- DigitalInput_I2.IND → LED_Q1_1HZ.REQ  
- DigitalInput_I3.IND → LED_Q1_ON.REQ

### Datenverbindungen:
- DigitalInput_I1.IN → LED_Q1_5HZ.OUT
- DigitalInput_I2.IN → LED_Q1_1HZ.OUT
- DigitalInput_I3.IN → LED_Q1_ON.OUT

### Parameterkonfiguration:
- **LED_Q1_5HZ**: Output_Q1 mit 5 Hz Frequenz
- **LED_Q1_1HZ**: Output_Q2 mit 1 Hz Frequenz
- **LED_Q1_ON**: Output_Q3 mit Dauerlicht
- Alle digitalen Eingänge sind aktiviert (QI=TRUE)

### Funktionsweise:
Jeder digitale Eingang (I1, I2, I3) steuert eine separate LED-Ausgabe (Q1, Q2, Q3) mit unterschiedlichen Blinkmustern. Bei Betätigung eines Eingangssignals wird die entsprechende LED mit der konfigurierten Frequenz aktiviert.

## Lernziele
- Verständnis der LED-Ansteuerung mit verschiedenen Frequenzen
- Umgang mit digitalen Ein- und Ausgängen
- Implementierung paralleler Schaltungen
- Parametrierung von Funktionsbausteinen

## Schwierigkeitsgrad
Einfach - geeignet für Einsteiger in die 4diac-IDE

## Vorkenntnisse
- Grundlagen der 4diac-IDE
- Verständnis von Events und Datenverbindungen
- Basiswissen über digitale Ein-/Ausgänge

## Zusammenfassung
Diese Übung zeigt eine grundlegende Implementierung von LED-Steuerungen mit unterschiedlichen Blinkfrequenzen. Durch die parallele Anordnung von drei unabhängigen Schaltungen wird das Verständnis für die Steuerung mehrerer Ausgänge über separate Eingänge vermittelt. Die Übung demonstriert effektiv die Parametrierung von Frequenzen und die Verbindung von digitalen Ein- mit Ausgangssignalen.