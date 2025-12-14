# Uebung_035a: Ampelschaltung International

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine internationale Ampelschaltung für den Fahrzeugverkehr. Die Ampel durchläuft einen standardisierten Zyklus mit den Phasen Rot, Rot-Orange, Grün und Orange. Die Steuerung erfolgt über einen Taster, der den Ampelzyklus startet.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_CLK_I1** (logiBUS_IE): Digitaler Eingang für Tasterbetätigung
- **sequence_T_04_loop** (sequence_T_04_loop): Sequenzer für Ampelphasensteuerung
- **E_TimeOut** (E_TimeOut): Zeitsteuerung für Sequenzer
- **CAR_RED_LIGHT** (logiBUS_QX): Ausgang für rotes Ampellicht
- **CAR_ORANGE_LIGHT** (logiBUS_QX): Ausgang für oranges Ampellicht  
- **CAR_GREEN_LIGHT** (logiBUS_QX): Ausgang für grünes Ampellicht

### Sub-Bausteine:

#### RED
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **OR_RED**: OR_2
    - Parameter: keine
    - Ereigniseingänge: REQ
    - Ereignisausgänge: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgänge: OUT
- **Funktionsweise**: Kombiniert die Signale für die Rotphase (S1) und Rot-Orange-Phase (S2) mittels ODER-Verknüpfung

#### ORANGE
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **OR_ORANGE**: OR_2
    - Parameter: keine
    - Ereigniseingänge: REQ
    - Ereignisausgänge: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgänge: OUT
- **Funktionsweise**: Kombiniert die Signale für die Rot-Orange-Phase (S2) und Orange-Phase (S4) mittels ODER-Verknüpfung

## Programmablauf und Verbindungen

Der Programmablauf startet mit der Betätigung des Tasters (DigitalInput_CLK_I1), der den Sequenzer sequence_T_04_loop initialisiert. Der Sequenzer durchläuft folgende Phasen mit festgelegten Zeitintervallen:

- **S1 (Rot)**: 6 Sekunden
- **S2 (Rot+Orange)**: 2 Sekunden  
- **S3 (Grün)**: 8 Sekunden
- **S4 (Orange)**: 2 Sekunden

Die Ereignis- und Datenverbindungen sind wie folgt aufgebaut:
- Der Taster löst über IND den START_S1 des Sequenzers aus
- Die Phasenausgänge EO_S1-EO_S4 und DO_S1-DO_S4 steuern die entsprechenden Sub-Bausteine und Ausgänge
- Die Sub-Bausteine RED und ORANGE kombinieren die Phasensignale für die gemeinsamen Lichtzustände
- Die finalen Signale werden an die Ausgänge CAR_RED_LIGHT, CAR_ORANGE_LIGHT und CAR_GREEN_LIGHT weitergeleitet
- Der E_TimeOut-Baustein sorgt für die zeitliche Steuerung des Sequenzers

**Lernziele**: Verständnis von Zustandsautomaten, Zeitsteuerung, ODER-Verknüpfungen und modularem Aufbau mit Sub-Bausteinen

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignissteuerung

**Start der Übung**: Die Übung wird durch Betätigen des Tasters I1 gestartet

## Zusammenfassung
Diese Übung demonstriert eine praxisnahe Anwendung einer Ampelschaltung mit internationalem Standard. Die modulare Struktur mit Sub-Bausteinen ermöglicht eine übersichtliche Implementierung der komplexen Phasensteuerung. Die Verwendung eines Sequenzers mit Zeitsteuerung und die Kombination von Phasensignalen durch ODER-Verknüpfungen sind zentrale Konzepte dieser Übung.