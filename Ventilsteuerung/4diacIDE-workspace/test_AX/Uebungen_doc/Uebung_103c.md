Hier ist die Dokumentation für die Übung **Uebung_103c** basierend auf den bereitgestellten XML-Daten.

# Uebung_103c

![Uebung_103c Übersicht](Uebung_103c.png)

* * * * * * * * * *

## Einleitung
Die Übung **Uebung_103c** demonstriert die Verwendung von Adapter-Verbindungen (Plug and Socket) in Kombination mit Multiplexern (MUX) und Demultiplexern (DEMUX). Ziel der Schaltung ist es, ein digitales Eingangssignal (`DigitalInput_I1`) über verschiedene logische Pfade an einen digitalen Ausgang (`DigitalOutput_Q1`) zu leiten. Die Auswahl des aktiven Pfades erfolgt über einen Selektor.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden verschiedene Standard-Funktionsbausteine sowie spezifische Sub-Bausteine (SubApps) verwendet, um die Logik zu kapseln.

### Haupt-Netzwerk Bausteine:

*   **DigitalInput_I1** (`logiBUS::io::DI::logiBUS_IXA`):
    *   Stellt den digitalen Hardware-Eingang dar.
    *   Parameter: `QI = TRUE`, `Input = Input_I1`.
*   **DigitalOutput_Q1** (`logiBUS::io::DQ::logiBUS_QXA`):
    *   Stellt den digitalen Hardware-Ausgang dar.
    *   Parameter: `QI = TRUE`, `Output = Output_Q1`.
*   **AX_DEMUX_3** (`adapter::selection::unidirectional::AX_DEMUX_3`):
    *   Ein Adapter-Demultiplexer, der einen eingehenden Adapter-Strom auf einen von drei Ausgängen verteilt.
*   **AX_MUX_3** (`adapter::selection::unidirectional::AX_MUX_3`):
    *   Ein Adapter-Multiplexer, der einen von drei eingehenden Adapter-Strömen auf einen Ausgang durchschaltet.
*   **C2** (`iec61131::selection::F_MOVE`):
    *   Dient hier als Konstanten-Geber für die Auswahl des Kanals.
    *   Parameter: `IN = UINT#1`.

### Sub-Bausteine (SubApps)

In diesem Netzwerk werden drei Sub-Applikationen instanziiert, die unterschiedliche Schaltverhalten repräsentieren. Da die internen Definitionen dieser SubApps in der bereitgestellten Datei nicht enthalten sind, wird ihre Funktion basierend auf ihren Namen und ihrer Einbindung beschrieben.

#### Sub-Baustein: tastend
*   **Typ**: `MyLib::sys::tastend`
*   **Beschreibung**: Dieser Baustein realisiert eine tastende Funktion (Momentankontakt). Das Signal wird solange durchgeschleift, wie der Eingang aktiv ist.
*   **Verbindung**: Angeschlossen an Kanal 1 (OUT1/IN1) des MUX/DEMUX-Systems.

#### Sub-Baustein: rastend
*   **Typ**: `MyLib::sys::rastend`
*   **Beschreibung**: Dieser Baustein realisiert eine rastende Funktion (Schalterverhalten/Toggle oder Selbsthaltung). Ein Impuls aktiviert den Ausgang dauerhaft, ein weiterer (oder ein Rücksetzsignal) deaktiviert ihn.
*   **Verbindung**: Angeschlossen an Kanal 2 (OUT2/IN2) des MUX/DEMUX-Systems.

#### Sub-Baustein: tastend_TON_5s
*   **Typ**: `MyLib::sys::tastend_TON_5s`
*   **Beschreibung**: Dieser Baustein kombiniert eine tastende Funktion mit einer Zeitverzögerung (TON - Timer On Delay) von 5 Sekunden.
*   **Verbindung**: Angeschlossen an Kanal 3 (OUT3/IN3) des MUX/DEMUX-Systems.

## Programmablauf und Verbindungen

Der Datenfluss in dieser Übung basiert auf der Weiterleitung von Adapter-Signalen (Interface-Informationen statt reiner Daten/Events).

1.  **Kanalauswahl**:
    *   Der Baustein **C2** (`F_MOVE`) liefert den Wert `1` an die Eingänge `K` (Key/Selektor) sowohl des Demultiplexers (`AX_DEMUX_3`) als auch des Multiplexers (`AX_MUX_3`).
    *   Dadurch ist fest eingestellt, dass **Kanal 1** aktiv ist.

2.  **Signalpfad**:
    *   Das Signal kommt vom **DigitalInput_I1** und tritt in den **AX_DEMUX_3** ein.
    *   Aufgrund der Selektion (`K=1`) wird das Signal an `OUT1` ausgegeben.
    *   Von dort gelangt es in die SubApp **tastend**.
    *   Das verarbeitete Signal verlässt die SubApp und geht an den Eingang `IN1` des **AX_MUX_3**.
    *   Da auch hier `K=1` gesetzt ist, leitet der Multiplexer das Signal von `IN1` an seinen Ausgang `OUT` weiter.
    *   Schließlich steuert das Signal den **DigitalOutput_Q1**.

3.  **Inaktive Pfade**:
    *   Die SubApps **rastend** (Kanal 2) und **tastend_TON_5s** (Kanal 3) sind zwar vollständig verdrahtet, werden aber aufgrund der festen Einstellung des Selektors auf `1` aktuell ignoriert. Um diese Funktionen zu nutzen, müsste der Wert am Parameter `IN` des Bausteins `C2` auf `2` oder `3` geändert werden.

## Zusammenfassung

Die Übung **Uebung_103c** zeigt anschaulich, wie man komplexe Logikblöcke mithilfe von Adaptern und Multiplexern modular aufbaut. Durch einfaches Ändern einer Steuervariablen (Selektor) kann das Verhalten der Schaltung (tastend, rastend oder zeitverzögert) komplett ausgetauscht werden, ohne die eigentliche Verdrahtung zu ändern. In der aktuellen Konfiguration ist die **tastende** Funktion aktiv.