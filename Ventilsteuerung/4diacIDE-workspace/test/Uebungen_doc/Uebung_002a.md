# Uebung_002a: DigitalInput_I1/_I2 mit AND auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung digitaler Eingangssignale mit einer logischen UND-Verknüpfung. Zwei digitale Eingänge (I1 und I2) werden über einen AND-Baustein verknüpft und das Ergebnis an einen digitalen Ausgang (Q1) ausgegeben.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1 / DigitalInput_I2
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE (Aktivierung des Bausteins)
  - Input = logiBUS_DI::Input_I1 / logiBUS_DI::Input_I2 (Zuweisung der physikalischen Eingänge)

### AND_2
- **Typ**: AND_2 (2-fach UND-Baustein)
- **Funktionsweise**: Führt eine logische UND-Verknüpfung der beiden Eingangssignale durch

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Aktivierung des Bausteins)
  - Output = logiBUS_DO::Output_Q1 (Zuweisung des physikalischen Ausgangs)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → AND_2.REQ
- DigitalInput_I2.IND → AND_2.REQ
- AND_2.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → AND_2.IN1
- DigitalInput_I2.IN → AND_2.IN2
- AND_2.OUT → DigitalOutput_Q1.OUT

**Lernziele:**
- Verständnis der grundlegenden logischen Verknüpfung (UND)
- Aufbau von einfachen Steuerungsschaltungen
- Umgang mit digitalen Ein- und Ausgängen
- Verkabelung von Funktionsbausteinen in 4diac-IDE

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der Digitaltechnik, erste Erfahrungen mit 4diac-IDE

**Starten der Übung**: Das Programm wird automatisch aktiviert, sobald es auf ein kompatibles Steuerungssystem geladen wurde. Die Eingänge I1 und I2 können über die Hardware oder Simulation getestet werden.

## Zusammenfassung
Diese Übung vermittelt die grundlegende Funktionsweise einer UND-Verknüpfung in der Automatisierungstechnik. Der Ausgang Q1 wird nur dann aktiviert, wenn beide Eingänge I1 und I2 gleichzeitig ein Signal führen. Dieses Prinzip bildet die Basis für viele Steuerungsaufgaben in der Industrieautomation.