Hier ist die Dokumentation für die Übung `Uebung_020e_AX` basierend auf den bereitgestellten Daten.

# Uebung_020e_AX

![Uebung_020e_AX](Uebung_020e_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine logische Schaltung, die ein digitales Eingangssignal (Input_I1) auf ein digitales Ausgangssignal (Output_Q1) überträgt, wobei eine Ausschaltverzögerung (TOF - Timer Off-Delay) verwendet wird. Die Besonderheit dieser Übung liegt in der Verwendung von Adapter-Verbindungen (`AdapterConnections`) anstelle von separaten Event- und Datenverbindungen, was durch den Baustein `AX_TOF` realisiert wird.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden verschiedene Bausteine verschaltet, um die gewünschte Zeitverzögerung zwischen Ein- und Ausgabe zu erreichen.

### Sub-Bausteine: Uebung_020e_AX

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **DigitalInput_I1**: logiBUS::io::DI::logiBUS_IXA
        - **Beschreibung**: Dieser Baustein repräsentiert den digitalen Eingang. Er liest den physikalischen Eingang `Input_I1`.
        - **Parameter**: 
            - `QI` = TRUE (Baustein ist aktiviert)
            - `Input` = Input_I1 (Logische Zuweisung des Eingangs)
        - **Verbindungen**: Der Adapter-Ausgang `.IN` liefert das Signal.

    - **AX_TOF**: adapter::events::unidirectional::timers::AX_TOF
        - **Beschreibung**: Ein ausschaltverzögerter Timer-Baustein, der für die Verwendung mit Adaptern ausgelegt ist.
        - **Parameter**: 
            - `PT` = T#5s (Die Verzögerungszeit ist auf 5 Sekunden eingestellt).
        - **Funktionsweise**: Wenn das Eingangssignal von TRUE auf FALSE wechselt, bleibt der Ausgang für die Zeitdauer `PT` noch auf TRUE, bevor er ebenfalls auf FALSE wechselt.

    - **DigitalOutput_Q1**: logiBUS::io::DQ::logiBUS_QXA
        - **Beschreibung**: Dieser Baustein repräsentiert den digitalen Ausgang. Er steuert den physikalischen Ausgang `Output_Q1`.
        - **Parameter**: 
            - `QI` = TRUE (Baustein ist aktiviert)
            - `Output` = Output_Q1 (Logische Zuweisung des Ausgangs)
        - **Verbindungen**: Der Adapter-Eingang `.OUT` empfängt das Signal.

## Programmablauf und Verbindungen

Der Programmablauf innerhalb dieser Sub-Applikation ist linear und nutzt Adapter-Verbindungen zur Vereinfachung des Netzwerks:

1.  **Signaleingang**: Der Baustein `DigitalInput_I1` erfasst den Zustand des Hardware-Eingangs.
2.  **Verbindung zum Timer**: Über eine Adapter-Verbindung (`Connection`) wird der Port `DigitalInput_I1.IN` direkt mit dem Eingang `AX_TOF.IN` verbunden.
3.  **Zeitverarbeitung (Ausschaltverzögerung)**:
    *   Solange der Eingang `TRUE` ist, ist auch der Ausgang des Timers `TRUE`.
    *   Fällt der Eingang auf `FALSE` ab, startet der Timer. Der Ausgang bleibt für weitere **5 Sekunden** (`PT=T#5s`) auf `TRUE`.
    *   Nach Ablauf der 5 Sekunden fällt auch der Ausgang auf `FALSE`.
4.  **Signalausgang**: Der Ausgang des Timers `AX_TOF.Q` ist über eine Adapter-Verbindung mit dem Eingang `DigitalOutput_Q1.OUT` verbunden, wodurch der physikalische Ausgang geschaltet wird.

**Lernziele:**
*   Verständnis von Adapter-Bausteinen (`AX_...`) in 4diac.
*   Anwendung einer Ausschaltverzögerung (TOF).
*   Verknüpfung von Hardware-IOs über logiBUS Bausteine.

## Zusammenfassung
Die `Uebung_020e_AX` zeigt eine effiziente Implementierung einer Ausschaltverzögerung von 5 Sekunden. Durch die Nutzung der `AX_TOF` Variante und Adapter-Verbindungen wird die grafische Darstellung des Netzwerks im Vergleich zu klassischen IEC 61499 Event/Daten-Verbindungen deutlich übersichtlicher gestaltet, da weniger Linien (Verbindungen) notwendig sind.