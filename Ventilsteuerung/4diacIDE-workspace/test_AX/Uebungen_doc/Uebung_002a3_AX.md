# Uebung_002a3_AX: DigitalInput_I1/_I2 mit OR auf DigitalOutput_Q1, mit Plug and Socket

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von digitalen Ein- und Ausgängen mit einer ODER-Verknüpfung in der 4diac-IDE. Die Übung zeigt die Anwendung von Plug-and-Socket-Verbindungen zwischen Funktionsbausteinen zur Realisierung einer einfachen logischen Schaltung.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1 / DigitalInput_I2
- **Typ**: logiBUS_IXA
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 (bzw. Input_I2)
- **Funktion**: Liest digitale Eingangssignale von den entsprechenden Eingängen des logiBUS-Systems

### DigitalOutput_Q1
- **Typ**: logiBUS_QXA
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt das Ausgangssignal auf den entsprechenden Ausgang des logiBUS-Systems

### AX_OR_2
- **Typ**: AX_OR_2
- **Funktion**: Realisiert eine ODER-Verknüpfung mit zwei Eingängen

## Programmablauf und Verbindungen

**Verbindungsstruktur:**
- DigitalInput_I1.IN → AX_OR_2.IN1
- DigitalInput_I2.IN → AX_OR_2.IN2
- AX_OR_2.OUT → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Die digitalen Eingänge I1 und I2 werden kontinuierlich eingelesen
2. Die ODER-Verknüpfung verarbeitet die Eingangssignale
3. Das Ergebnis wird auf den digitalen Ausgang Q1 geschrieben
4. Q1 wird aktiviert, wenn mindestens einer der beiden Eingänge (I1 oder I2) aktiv ist

**Lernziele:**
- Verständnis digitaler Ein- und Ausgänge in 4diac
- Anwendung von logischen Verknüpfungen (ODER)
- Umgang mit Plug-and-Socket-Verbindungen
- Grundlagen der Signalverarbeitung in IEC 61499

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis digitaler Signale

**Starten der Übung**: Die Übung kann direkt in der 4diac-IDE geladen und auf einem kompatiblen Zielsystem ausgeführt werden.

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der digitalen Signalverarbeitung mit 4diac. Sie zeigt anschaulich, wie digitale Eingangssignale mittels einer ODER-Verknüpfung verarbeitet und auf einen Ausgang geschrieben werden. Die Verwendung von standardisierten Bus-Funktionsbausteinen und Plug-and-Socket-Verbindungen demonstriert praxisnahe Anwendungsmöglichkeiten in der Automatisierungstechnik.