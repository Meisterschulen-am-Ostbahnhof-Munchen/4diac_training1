# Uebung_002a5_AX: DigitalInput_I1-3 mit OR auf DigitalOutput_Q1, mit Plug and Socket

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von digitalen Eingängen und einem ODER-Baustein zur Steuerung eines digitalen Ausgangs. Die Schaltung verbindet drei digitale Eingänge über einen 3-fach ODER-Baustein mit einem digitalen Ausgang, wobei Plug-and-Socket-Verbindungen verwendet werden.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_I1**, **DigitalInput_I2**, **DigitalInput_I3** (Typ: logiBUS_IXA)
- **AX_OR_3** (Typ: AX_OR_3)
- **DigitalOutput_Q1** (Typ: logiBUS_QXA)

### Sub-Bausteine: AX_OR_3
- **Typ**: AX_OR_3
- **Verwendete interne FBs**: Keine weiteren internen FBs angegeben
- **Funktionsweise**: Der Baustein realisiert eine logische ODER-Verknüpfung mit drei Eingängen. Wenn mindestens einer der drei Eingänge aktiv ist, wird der Ausgang auf TRUE gesetzt.

## Programmablauf und Verbindungen

**Verbindungen:**
- DigitalInput_I1.IN → AX_OR_3.IN1
- DigitalInput_I2.IN → AX_OR_3.IN2  
- DigitalInput_I3.IN → AX_OR_3.IN3
- AX_OR_3.OUT → DigitalOutput_Q1.OUT

**Parameterkonfiguration:**
- Alle DigitalInput-Bausteine haben QI = TRUE
- DigitalInput_I1 nutzt logiBUS_DI::Input_I1
- DigitalInput_I2 nutzt logiBUS_DI::Input_I2  
- DigitalInput_I3 nutzt logiBUS_DI::Input_I3
- DigitalOutput_Q1 nutzt logiBUS_DO::Output_Q1

**Lernziele:**
- Verständnis der logischen ODER-Verknüpfung
- Umgang mit digitalen Ein- und Ausgängen
- Anwendung von Plug-and-Socket-Verbindungen
- Konfiguration von Bus-Systemparametern

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der digitalen Logik, Basiswissen 4diac-IDE

**Starten der Übung**: Die Übung kann direkt in der 4diac-IDE geladen und auf einem kompatiblen Zielsystem ausgeführt werden.

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der digitalen Signalverarbeitung mit ODER-Verknüpfungen. Durch die Verwendung von drei Eingängen und der entsprechenden Verknüpfungstechnik lernen Anwender die Prinzipien der logischen Verknüpfung und die Ansteuerung von Ausgängen in industriellen Steuerungssystemen kennen.