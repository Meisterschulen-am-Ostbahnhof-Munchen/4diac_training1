Hier ist die Dokumentation für die Übung `Uebung_004a3_AX` im gewünschten Format.

# Uebung_004a3_AX

![Uebung_004a3_AX Bild](Uebung_004a3_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung realisiert eine Schaltung, bei der ein Ausgang (Q1) über zwei verschiedene Eingänge (I1, I2) umgeschaltet (getoggelt) werden kann. Dies entspricht einer Wechselschaltung oder Stromstoßschaltung.

Das Besondere an dieser Variante ist, dass im Vergleich zu ähnlichen Übungen (wie `Uebung_004a2`) auf den expliziten Einsatz eines `E_MERGE`-Bausteins verzichtet wird. Stattdessen werden die Ereignislinien direkt zusammengeführt. Zudem wird ein T-Flip-Flop mit Adapter-Schnittstelle (`AX_T_FF`) verwendet.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden Bausteine aus der `logiBUS`-Bibliothek sowie ein spezieller Adapter-Baustein verwendet.

### Sub-Bausteine: Uebung_004a3_AX

Diese Übung selbst ist als SubAppType definiert und beinhaltet folgende interne Logik:

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **DigitalInput_CLK_I1**: `logiBUS::io::DI::logiBUS_IE`
        - Parameter: `Input` = `Input_I1`
        - Parameter: `InputEvent` = `BUTTON_SINGLE_CLICK`
        - Ereignisausgang: `IND` (Indication - Signal bei Tastendruck)
    - **DigitalInput_CLK_I2**: `logiBUS::io::DI::logiBUS_IE`
        - Parameter: `Input` = `Input_I2`
        - Parameter: `InputEvent` = `BUTTON_SINGLE_CLICK`
        - Ereignisausgang: `IND` (Indication - Signal bei Tastendruck)
    - **E_T_FF**: `adapter::events::unidirectional::AX_T_FF`
        - Typ: Toggle Flip-Flop mit Adapter-Ausgang
        - Ereigniseingang: `CLK` (Clock)
        - Adapterausgang: `Q`
    - **DigitalOutput_Q1**: `logiBUS::io::DQ::logiBUS_QXA`
        - Parameter: `Output` = `Output_Q1`
        - Adaptereingang: `OUT`

- **Funktionsweise**:
    Die beiden digitalen Eingänge sind so konfiguriert, dass sie auf einen einfachen Klick (`BUTTON_SINGLE_CLICK`) reagieren. Die Ereignisse beider Eingänge werden auf den Takteingang des Flip-Flops geleitet. Das Flip-Flop wechselt bei jedem Signal seinen Zustand und gibt diesen über eine Adapter-Verbindung an den digitalen Ausgang weiter.

## Programmablauf und Verbindungen

Der Ablauf der Steuerung gestaltet sich wie folgt:

1.  **Eingabeverarbeitung**:
    *   Sowohl `DigitalInput_CLK_I1` als auch `DigitalInput_CLK_I2` überwachen die konfigurierten Taster.
    *   Wird einer der Taster einfach geklickt, wird das `IND`-Event am jeweiligen Baustein ausgelöst.

2.  **Implizites Event-Merge**:
    *   Die `IND`-Ausgänge beider Eingangsbausteine sind direkt mit dem `CLK`-Eingang des `E_T_FF` Bausteins verbunden.
    *   Dies demonstriert eine Besonderheit in IEC 61499 / 4diac: Mehrere Event-Quellen können auf ein Event-Ziel geschaltet werden. Dies wirkt wie ein logisches ODER (implizites Merge). Es ist kein separater `E_MERGE`-Baustein notwendig, um die Signale zusammenzuführen.

3.  **Verarbeitung im Flip-Flop**:
    *   Sobald ein Signal am `CLK`-Eingang des `E_T_FF` ankommt, wechselt der interne Zustand des T-Flip-Flops (von TRUE auf FALSE oder umgekehrt).

4.  **Ausgabe über Adapter**:
    *   Der Ausgang des Flip-Flops `Q` ist über eine Adapter-Verbindung (erkennbar am doppelten Pfeil oder speziellen Farbgebung in der IDE) mit dem Eingang `OUT` des `DigitalOutput_Q1` verbunden.
    *   Adapter-Verbindungen bündeln Daten und Events. In diesem Fall wird der Status (An/Aus) direkt an den Hardware-Ausgang `Output_Q1` übertragen.

**Lernziele:**
*   Verständnis von impliziten Event-Verbindungen (Fan-In) ohne `E_MERGE`.
*   Verwendung von Adapter-basierten Funktionsbausteinen (`AX`, `QXA`).
*   Realisierung einer Stromstoßschaltung mit zwei Bedienstellen.

## Zusammenfassung
Die Übung `Uebung_004a3_AX` zeigt eine effiziente Implementierung einer Lichtsteuerung mit zwei Tastern. Durch den Verzicht auf den `E_MERGE`-Baustein wird die Event-Verdrahtung vereinfacht, indem die Fähigkeit der IDE genutzt wird, mehrere Events auf einen Eingang zu legen. Die Verwendung von Adapter-Bausteinen (`AX_T_FF` und `logiBUS_QXA`) reduziert zudem die Anzahl der sichtbaren Verbindungen im Netzwerk, da Daten und Events in einer Verbindung gekapselt werden.