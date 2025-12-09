# Uebung_002a6_AX: DigitalInput_I1-3 mit AND auf DigitalOutput_Q1, mit Plug and Socket

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von digitalen Ein- und Ausgängen mit einer logischen UND-Verknüpfung. Drei digitale Eingänge werden über einen 3-fach-AND-Baustein verknüpft und das Ergebnis an einen digitalen Ausgang ausgegeben. Die Übung verwendet Plug-and-Socket-Verbindungen für die Kommunikation zwischen den Funktionsbausteinen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1, DigitalInput_I2, DigitalInput_I3
- **Typ**: logiBUS_IXA
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 / Input_I2 / Input_I3

### DigitalOutput_Q1
- **Typ**: logiBUS_QXA
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

### AX_AND_3
- **Typ**: AX_AND_3
- **Funktionsweise**: Führt eine logische UND-Verknüpfung zwischen drei Eingangssignalen durch. Der Ausgang wird nur dann aktiv, wenn alle drei Eingänge gleichzeitig aktiv sind.

## Programmablauf und Verbindungen

**Verbindungen:**
- DigitalInput_I1.IN → AX_AND_3.IN1
- DigitalInput_I2.IN → AX_AND_3.IN2  
- DigitalInput_I3.IN → AX_AND_3.IN3
- AX_AND_3.OUT → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Die drei DigitalInput-Bausteine lesen die Zustände der physikalischen Eingänge I1, I2 und I3 ein
2. Die Eingangssignale werden an den AX_AND_3-Baustein weitergeleitet
3. Der AX_AND_3-Baustein führt die logische UND-Verknüpfung durch
4. Das Ergebnis wird an den DigitalOutput_Q1-Baustein gesendet
5. Der Ausgang Q1 wird entsprechend dem logischen Ergebnis geschaltet

**Lernziele:**
- Verständnis der logischen UND-Verknüpfung
- Umgang mit digitalen Ein- und Ausgängen
- Verwendung von Plug-and-Socket-Verbindungen
- Aufbau von einfachen logischen Schaltungen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der Digitaltechnik, Basiswissen 4diac-IDE

**Starten der Übung**: Das Programm wird automatisch nach dem Hochladen auf das Zielsystem gestartet. Die QI-Parameter sind auf TRUE gesetzt, was eine permanente Aktivierung der Bausteine gewährleistet.

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der digitalen Signalverarbeitung mit logischen Verknüpfungen. Durch die Verwendung von drei Eingängen und einer UND-Verknüpfung lernen Anwender, wie komplexere logische Bedingungen in SPS-Programmen realisiert werden können. Die Übung zeigt zudem die praktische Anwendung von Plug-and-Socket-Verbindungen in verteilten Automatisierungssystemen.