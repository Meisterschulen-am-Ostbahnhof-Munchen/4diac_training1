# Uebung_002a_AX: DigitalInput_I1/_I2 mit AND auf DigitalOutput_Q1, mit Plug and Socket

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verwendung von digitalen Ein- und Ausgängen in Verbindung mit einer logischen UND-Verknüpfung. Die Schaltung realisiert eine einfache Steuerungslogik, bei der zwei digitale Eingänge über einen AND-Baustein verknüpft werden und das Ergebnis an einen digitalen Ausgang weitergeleitet wird.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1 / DigitalInput_I2
- **Typ**: logiBUS_IXA
- **Parameter**: 
  - QI = TRUE (Aktivierung des Bausteins)
  - Input = logiBUS_DI::Input_I1 / logiBUS_DI::Input_I2 (Zuweisung der physikalischen Eingänge)

### DigitalOutput_Q1
- **Typ**: logiBUS_QXA
- **Parameter**:
  - QI = TRUE (Aktivierung des Bausteins)
  - Output = logiBUS_DO::Output_Q1 (Zuweisung des physikalischen Ausgangs)

### AX_AND_2
- **Typ**: AX_AND_2
- **Funktionsweise**: Führt eine logische UND-Verknüpfung zwischen zwei Eingangssignalen durch. Der Ausgang wird nur dann aktiviert, wenn beide Eingänge gleichzeitig aktiv sind.

## Programmablauf und Verbindungen

**Verbindungsstruktur:**
- DigitalInput_I1.IN → AX_AND_2.IN1
- DigitalInput_I2.IN → AX_AND_2.IN2  
- AX_AND_2.OUT → DigitalOutput_Q1.OUT

**Lernziele:**
- Grundlegende Verwendung von digitalen Ein-/Ausgangsbausteinen
- Implementierung logischer Verknüpfungen (UND-Funktion)
- Verständnis der Signalverarbeitung in 4diac-IDE
- Arbeiten mit Plug-and-Socket-Verbindungen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Basiswissen über logische Verknüpfungen
- Verständnis digitaler Signale

**Starten der Übung:**
1. Projekt in 4diac-IDE öffnen
2. Ressource auf entsprechendem Gerät bereitstellen
3. Anwendung starten
4. Digitale Eingänge I1 und I2 testweise aktivieren/deaktivieren
5. Verhalten des Ausgangs Q1 beobachten

## Zusammenfassung
Diese Übung vermittelt die grundlegenden Prinzipien der Signalverarbeitung mit digitalen Ein- und Ausgängen. Durch die UND-Verknüpfung wird demonstriert, wie einfache logische Operationen in der Steuerungstechnik eingesetzt werden können. Die Übung bildet eine wichtige Basis für komplexere Steuerungsaufgaben und zeigt die praktische Anwendung von Plug-and-Socket-Verbindungen in 4diac-IDE.