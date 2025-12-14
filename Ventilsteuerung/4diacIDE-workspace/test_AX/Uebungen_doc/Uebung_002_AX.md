# Uebung_002_AX: DigitalInput_I1 auf DigitalOutput_Q1/_Q2, mit Plug and Socket 

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von Adapterverbindungen (Plug and Socket) in 4diac-IDE zur Signalverteilung. Ein digitales Eingangssignal wird auf zwei digitale Ausgänge verteilt.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_I1** (Typ: logiBUS_IXA)
- **DigitalOutput_Q1** (Typ: logiBUS_QXA)
- **DigitalOutput_Q2** (Typ: logiBUS_QXA)
- **AX_SPLIT_2** (Typ: AX_SPLIT_2)

### Sub-Bausteine: AX_SPLIT_2
- **Typ**: AX_SPLIT_2
- **Verwendete interne FBs**: Keine internen FBs (Adapterbaustein)
- **Funktionsweise**: Verteilt ein eingehendes Signal auf zwei Ausgänge (OUT1 und OUT2)

## Programmablauf und Verbindungen

**Verbindungsstruktur:**
- DigitalInput_I1.IN → AX_SPLIT_2.IN
- AX_SPLIT_2.OUT1 → DigitalOutput_Q1.OUT
- AX_SPLIT_2.OUT2 → DigitalOutput_Q2.OUT

**Parameterkonfiguration:**
- Alle Bausteine haben QI = TRUE (aktiviert)
- DigitalInput_I1: Input = logiBUS_DI::Input_I1
- DigitalOutput_Q1: Output = logiBUS_DO::Output_Q1
- DigitalOutput_Q2: Output = logiBUS_DO::Output_Q2

**Lernziele:**
- Verständnis von Adapterverbindungen (Plug and Socket)
- Signalverteilung auf mehrere Ausgänge
- Konfiguration von logiBUS-Ein-/Ausgängen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von digitalen Ein-/Ausgängen
- Basiswissen über Funktionsbausteine

**Start der Übung:**
Das Programm wird automatisch aktiviert, da alle QI-Parameter auf TRUE gesetzt sind. Bei Aktivierung des digitalen Eingangs I1 werden beide Ausgänge Q1 und Q2 synchron geschaltet.

## Zusammenfassung
Diese Übung zeigt eine grundlegende Signalverteilung mittels Adapterverbindungen. Der AX_SPLIT_2-Baustein ermöglicht die einfache Verteilung eines Eingangssignals auf mehrere Ausgänge, was in der Praxis häufig für parallele Steuerungsaufgaben benötigt wird.