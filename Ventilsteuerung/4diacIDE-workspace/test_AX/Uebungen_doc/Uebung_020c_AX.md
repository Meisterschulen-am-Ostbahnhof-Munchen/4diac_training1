Hier ist die Dokumentationsseite für die Übung `Uebung_020c_AX`, basierend auf den bereitgestellten XML-Daten.

# Uebung_020c_AX

![Uebung_020c_AX Bild](Uebung_020c_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine einschaltverzögerte Logik unter Verwendung von Adaptern. Das Ziel ist es, das Signal eines digitalen Eingangs (`Input_I1`) zu lesen, es um eine definierte Zeit zu verzögern und anschließend auf einen digitalen Ausgang (`Output_Q1`) zu schalten. Hierbei kommt der Baustein `AX_TON` zum Einsatz, der speziell für die Verwendung mit Adapter-Verbindungen (Adapter Connections) ausgelegt ist.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden folgende Funktionsbausteine im Netzwerk verschaltet:

### Sub-Bausteine: DigitalInput_I1
- **Typ**: `logiBUS::io::DI::logiBUS_IXA`
- **Funktionsweise**: Dieser Baustein stellt die Schnittstelle zum physischen digitalen Eingang dar. Er verwendet Adapter-Technologie.
- **Parameter**:
    - `QI` = `TRUE`
    - `Input` = `Input_I1`

### Sub-Bausteine: AX_TON
- **Typ**: `adapter::events::unidirectional::timers::AX_TON`
- **Funktionsweise**: Ein Einschaltverzögerungs-Timer (Timer On-Delay), der über Adapter-Schnittstellen verfügt. Er verzögert das Weiterleiten des `TRUE`-Signals vom Eingang zum Ausgang.
- **Parameter**:
    - `PT` = `T#5s` (5 Sekunden Verzögerungszeit)

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Funktionsweise**: Dieser Baustein stellt die Schnittstelle zum physischen digitalen Ausgang dar. Er empfängt das Signal über eine Adapter-Verbindung.
- **Parameter**:
    - `QI` = `TRUE`
    - `Output` = `Output_Q1`

## Programmablauf und Verbindungen

Der Programmablauf wird durch Adapter-Verbindungen (`AdapterConnections`) realisiert, was den Plan übersichtlicher gestaltet, da Daten- und Ereignisflüsse gebündelt werden.

1.  **Eingangsverarbeitung**:
    - Der Baustein `DigitalInput_I1` erfasst den Status von `Input_I1`.
    - Über den Adapter-Port `IN` ist er mit dem Adapter-Port `IN` des Timers `AX_TON` verbunden.

2.  **Verzögerungslogik**:
    - Sobald das Eingangssignal anliegt, startet der `AX_TON` Timer.
    - Die Verzögerungszeit (`PT`) ist auf **5 Sekunden** eingestellt.

3.  **Ausgangssteuerung**:
    - Nach Ablauf der 5 Sekunden schaltet der Adapter-Ausgang `Q` des `AX_TON` durch.
    - Dieser ist mit dem Adapter-Eingang `OUT` des `DigitalOutput_Q1` verbunden, wodurch der physische Ausgang `Output_Q1` aktiviert wird.

**Zusatzinformationen:**
*   **Lernziele**: Verständnis von Adapter-Verbindungen in 4diac und Nutzung von adapterbasierten Timern (`AX_TON`).
*   **Schwierigkeitsgrad**: Einsteiger bis Fortgeschritten (Fokus auf Adapter-Konzept).

## Zusammenfassung
Die `Uebung_020c_AX` zeigt eine klassische Einschaltverzögerung von 5 Sekunden zwischen einem digitalen Eingang und einem digitalen Ausgang. Die Besonderheit liegt in der Verwendung von Adapter-Bausteinen (`logiBUS_IXA`, `logiBUS_QXA`, `AX_TON`), wodurch die Verbindungen im Netzwerkdiagramm auf einzelne Adapter-Linien reduziert werden.