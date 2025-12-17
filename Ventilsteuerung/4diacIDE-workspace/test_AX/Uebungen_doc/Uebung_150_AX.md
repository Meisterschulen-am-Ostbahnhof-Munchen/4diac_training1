Hier ist die Dokumentation für die Übung `Uebung_150_AX` basierend auf den bereitgestellten Informationen.

# Uebung_150_AX

*[Bild der Übung Uebung_150_AX, falls vorhanden]*

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von Adapter-Technologie (Plug and Socket Konzept) innerhalb der IEC 61499 Umgebung. Ziel ist es, das Signal eines digitalen Eingangs (`DigitalInput_I1`) zu nutzen, um einen digitalen Ausgang (`DigitalOutput_Q1`) zu steuern. Dabei kommt eine spezielle Logikkomponente, ein Adapter-basiertes Toggle-Flip-Flop (`AX_T_FF`), zum Einsatz, welches den Zustand des Ausgangs bei jedem Klick umschaltet.

## Verwendete Funktionsbausteine (FBs)

In dieser SubApp werden verschiedene Funktionsbausteine instanziiert, um die Eingabe, Verarbeitung und Ausgabe zu realisieren.

### Sub-Bausteine: DigitalInput_I1
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Beschreibung**: Dieser Baustein repräsentiert einen digitalen Eingang, der Events generiert.
- **Parameter**:
    - `QI` = `TRUE` (Baustein ist aktiv)
    - `Input` = `Input_I1` (Hardware-Mapping auf Eingang 1)
    - `InputEvent` = `BUTTON_SINGLE_CLICK` (Reagiert auf einfachen Tastendruck)

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Beschreibung**: Dieser Baustein repräsentiert einen digitalen Ausgang, der über eine Adapter-Schnittstelle angesteuert wird (erkennbar am Suffix "QXA").
- **Parameter**:
    - `QI` = `TRUE`
    - `Output` = `Output_Q1` (Hardware-Mapping auf Ausgang 1)

### Sub-Bausteine: AX_T_FF
- **Typ**: `adapter::events::unidirectional::AX_T_FF`
- **Beschreibung**: Ein Toggle-Flip-Flop, das Adapter-Verbindungen nutzt. Es wechselt seinen internen Zustand bei jedem Eingangssignal und gibt diesen über einen Adapter-Ausgang weiter.
- **Eingang**: `CLK` (Event-Eingang für den Takt/Trigger)
- **Ausgang**: `Q` (Adapter-Ausgang)

### Sub-Bausteine: logiBUS_PI_ID
- **Typ**: `logiBUS::io::PI::logiBUS_PI_ID`
- **Beschreibung**: Ein Baustein zur Konfiguration eines Pulse-Inputs (Impulseingang), der in diesem Netzwerk instanziiert ist.
- **Parameter**:
    - `QI` = `TRUE`
    - `Input` = `PulseInput_I8`
    - `ImpulseDelta` = `100`
    - `TimeDelta` = `50000`

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich wie folgt beschreiben:

1.  **Eingabe**: Der Baustein `DigitalInput_I1` überwacht den Hardware-Eingang `Input_I1`. Wenn ein einfacher Klick (`BUTTON_SINGLE_CLICK`) erkannt wird, wird das Event `IND` ausgelöst.
2.  **Verarbeitung (Event)**: Das Event `IND` vom Eingang ist mit dem `CLK`-Eingang des Bausteins `AX_T_FF` verbunden.
3.  **Logik**: Das `AX_T_FF` (Toggle-Flip-Flop) ändert bei jedem empfangenen Event am `CLK`-Eingang seinen Zustand (von Ein auf Aus oder umgekehrt).
4.  **Ausgabe (Adapter)**: Der Ausgang `Q` des Flip-Flops ist über eine **Adapter-Verbindung** mit dem Eingang `OUT` des `DigitalOutput_Q1` verbunden. Im Gegensatz zu einfachen Daten- oder Eventverbindungen bündelt diese Adapter-Verbindung die notwendigen Informationen (Event und boolescher Wert), um den physikalischen Ausgang `Output_Q1` zu schalten.
5.  **Nebenläufige Konfiguration**: Der Baustein `logiBUS_PI_ID` initialisiert zusätzlich den `PulseInput_I8` mit spezifischen Delta-Werten, greift aber nicht aktiv in die Logik zwischen Taster I1 und Ausgang Q1 ein.

## Zusammenfassung
Die Übung `Uebung_150_AX` veranschaulicht erfolgreich, wie klassische Logikschaltungen (hier ein Stromstoßschalter bzw. T-Flip-Flop) mithilfe von Adaptern in 4diac realisiert werden können. Durch die Verwendung von `AX_T_FF` und `logiBUS_QXA` wird die Verdrahtung vereinfacht, da Daten und Events logisch gruppiert über Adapter-Schnittstellen übertragen werden.