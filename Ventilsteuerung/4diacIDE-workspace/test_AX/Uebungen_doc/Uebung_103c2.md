Hier ist die Dokumentation für die Übung `Uebung_103c2` basierend auf den bereitgestellten Daten.

# Uebung_103c2

![Uebung_103c2](Uebung_103c2.png)

* * * * * * * * * *

## Einleitung

Die Übung **Uebung_103c2** demonstriert die Verarbeitung von Signalen zwischen einem digitalen Eingang (`DigitalInput_I1`) und einem digitalen Ausgang (`DigitalOutput_Q1`). Der Fokus liegt hierbei auf der Verwendung von Adapter-Verbindungen ("Plug and Socket") sowie dem Einsatz von Multiplexern (`AX_MUX`) und Demultiplexern (`AX_DEMUX`), um den Signalfluss durch verschiedene Sub-Applikationen (`SubApps`) zu leiten. Das System unterscheidet dabei zwischen "tastenden" und "rastenden" Verarbeitungslogiken.

## Verwendete Funktionsbausteine (FBs)

In diesem Netzwerk werden folgende Hauptkomponenten verwendet:

*   **DigitalInput_I1** (`logiBUS::io::DI::logiBUS_IXA`): Stellt die Schnittstelle zur Hardware für das Eingangssignal I1 dar.
    *   Parameter `QI`: `TRUE`
    *   Parameter `Input`: `Input_I1`
*   **DigitalOutput_Q1** (`logiBUS::io::DQ::logiBUS_QXA`): Stellt die Schnittstelle zur Hardware für das Ausgangssignal Q1 dar.
    *   Parameter `QI`: `TRUE`
    *   Parameter `Output`: `Output_Q1`
*   **AX_DEMUX_3** (`adapter::selection::unidirectional::AX_DEMUX_3`): Ein Adapter-Demultiplexer, der eine eingehende Adapter-Verbindung auf drei mögliche Ausgänge aufteilt.
*   **AX_MUX_3** (`adapter::selection::unidirectional::AX_MUX_3`): Ein Adapter-Multiplexer, der drei eingehende Adapter-Verbindungen auf einen gemeinsamen Ausgang zusammenführt.

### Sub-Bausteine

Die Übung verwendet spezifische Sub-Applikationen aus der Bibliothek `MyLib`, um die Logik zu kapseln.

### Sub-Baustein: tastend (Instanzen: `tastend`, `tastend2`)
*   **Typ**: `MyLib::sys::tastend`
*   **Verwendete interne FBs**:
    *   *Hinweis: Die internen FBs sind in der vorliegenden Definition gekapselt und nicht explizit sichtbar. Es wird davon ausgegangen, dass hier Standard-Logikbausteine zur Signalweiterleitung verwendet werden.*
*   **Funktionsweise**:
    Diese Sub-Applikation (`tastend`) implementiert eine tastende Logik (Momentkontakt). Das Signal liegt am Ausgang nur so lange an, wie es am Eingang aktiv ist (bzw. wie es durch den Adapter definiert wird). In dieser Übung wird der Baustein zweimal instanziiert (als `tastend` und `tastend2`).

### Sub-Baustein: rastend (Instanz: `rastend`)
*   **Typ**: `MyLib::sys::rastend`
*   **Verwendete interne FBs**:
    *   *Hinweis: Die internen FBs sind in der vorliegenden Definition gekapselt und nicht explizit sichtbar.*
*   **Funktionsweise**:
    Diese Sub-Applikation (`rastend`) implementiert eine rastende Logik (Schalterverhalten). Das Signal behält seinen Zustand bei oder schaltet bei Betätigung um, im Gegensatz zum reinen Tastverhalten.

## Programmablauf und Verbindungen

Der Programmablauf zeichnet sich durch eine parallele Strukturierung des Signalflusses über Adapter-Verbindungen aus:

1.  **Eingangssignal**: Das Signal startet am `DigitalInput_I1`.
2.  **Verzweigung (Demultiplexing)**: Der Adapter-Ausgang des Eingangsbausteins (`IN`) ist mit dem Eingang des `AX_DEMUX_3` verbunden. Dieser Baustein stellt das Eingangssignal an drei verschiedenen Ausgängen zur Verfügung:
    *   **Pfad 1**: Von `AX_DEMUX_3.OUT1` geht das Signal in die Sub-App `tastend`.
    *   **Pfad 2**: Von `AX_DEMUX_3.OUT2` geht das Signal in die Sub-App `rastend`.
    *   **Pfad 3**: Von `AX_DEMUX_3.OUT3` geht das Signal in die Sub-App `tastend2`.
3.  **Verarbeitung**: Die Signale durchlaufen die jeweilige Logik der Sub-Apps (tastend oder rastend).
4.  **Zusammenführung (Multiplexing)**: Die Ausgänge der drei Sub-Apps werden am `AX_MUX_3` wieder zusammengeführt:
    *   `tastend.OUT` -> `AX_MUX_3.IN1`
    *   `rastend.OUT` -> `AX_MUX_3.IN2`
    *   `tastend2.OUT` -> `AX_MUX_3.IN3`
5.  **Ausgangssignal**: Der gesammelte Ausgang des Multiplexers (`AX_MUX_3.OUT`) ist schließlich mit dem `DigitalOutput_Q1` verbunden, um das Ergebnis physikalisch auszugeben.

Diese Struktur ermöglicht es, verschiedene Verhaltensweisen (Taster vs. Schalter) modular in den Signalpfad einzubinden und über die Mux/Demux-Bausteine zu organisieren.

## Zusammenfassung

Die Übung `Uebung_103c2` zeigt eine fortgeschrittene Verschaltung von Ein- und Ausgängen unter Nutzung von Adapter-Technologie. Durch den Einsatz von `AX_DEMUX_3` und `AX_MUX_3` wird der Signalfluss in drei parallele Pfade aufgespalten, die durch wiederverwendbare Sub-Applikationen (`tastend` und `rastend`) definiert sind. Dies fördert den modularen Aufbau von Steuerungssoftware und demonstriert die Flexibilität von IEC 61499 Adapter-Verbindungen.