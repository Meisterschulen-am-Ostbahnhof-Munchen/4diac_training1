Hier ist die Dokumentation für die Übung `Uebung_004b_AX` basierend auf den bereitgestellten XML-Daten.

# Uebung_004b_AX

![Uebung_004b_AX](Uebung_004b_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert ein **Toggle Flip-Flop** (Umschalter) unter Verwendung der Adapter-Technologie (`AX`). Die Schaltung nutzt eine Kombination aus einem Event-Switch (`AX_SWITCH`) und einem Set-Reset-Baustein (`AX_SR`), um den Zustand des Ausgangs bei jedem Eingangsimpuls zu wechseln.

**Besonderer Hinweis:** Im Quellcode ist ein Warnhinweis enthalten ("nicht empfohlen !!! viel zu viel Bausteine"). Diese Übung dient primär dem Verständnis von Adapter-Verbindungen und komplexer Logik-Konstruktion, stellt aber keine effiziente Lösung für ein einfaches Toggle-Flip-Flop dar (hierfür wäre ein `E_T_FF` besser geeignet).

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden verschiedene spezialisierte Bausteine verwendet, um die Logik über Adapter-Verbindungen zu realisieren.

### LogiBUS IO Bausteine
Diese Bausteine stellen die Schnittstelle zur Hardware dar.

- **DigitalInput_CLK_I1**
    - **Typ**: `logiBUS::io::DI::logiBUS_IE`
    - **Funktion**: Erfasst das Eingangsereignis.
    - **Parameter**: 
        - `Input` = `Input_I1`
        - `InputEvent` = `BUTTON_SINGLE_CLICK` (Reagiert auf einen einfachen Klick).

- **DigitalOutput_Q1**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    - **Funktion**: Steuert den physikalischen Ausgang an.
    - **Parameter**: 
        - `Output` = `Output_Q1`

### Adapter-Logik Bausteine
Diese Bausteine verarbeiten die Signale innerhalb der Adapter-Ebene.

- **E_SR**
    - **Typ**: `adapter::events::unidirectional::AX_SR`
    - **Funktion**: Ein Set-Reset Flip-Flop auf Adapter-Basis. Es speichert den aktuellen Zustand (Ein oder Aus).

- **AX_SWITCH**
    - **Typ**: `adapter::events::unidirectional::AX_SWITCH`
    - **Funktion**: Ein Schalter, der Ereignisse basierend auf einem Steuersignal (Gate) auf zwei verschiedene Ausgänge (EO0 oder EO1) umleitet. Hier genutzt, um zwischen Setzen und Rücksetzen zu entscheiden.

- **AX_SPLIT_2**
    - **Typ**: `adapter::events::unidirectional::AX_SPLIT_2`
    - **Funktion**: Ein Splitter, der ein eingehendes Adapter-Signal auf zwei Ausgänge dupliziert. Notwendig für die Rückkopplung (Feedback-Loop).

### Konvertierungs-Bausteine
Dienen der Umwandlung zwischen klassischen IEC 61499 Signalen und Adapter-Signalen.

- **AX_BOOL_TO_X**
    - **Typ**: `adapter::conversion::unidirectional::AX_BOOL_TO_X`
    - **Funktion**: Konvertiert boolesche Logik/Ereignisse in das Adapter-Format, um den `AX_SWITCH` zu steuern.

- **AX_X_TO_BOOL**
    - **Typ**: `adapter::conversion::unidirectional::AX_X_TO_BOOL`
    - **Funktion**: Konvertiert Adapter-Signale zurück, um sie im Feedback-Pfad nutzbar zu machen.

## Programmablauf und Verbindungen

Das Ziel der Schaltung ist es, den Ausgang Q1 bei jedem Klick auf den Taster I1 umzuschalten (An -> Aus -> An).

1.  **Eingangssignal**: Das Signal kommt vom `DigitalInput_CLK_I1` (Button Click).
2.  **Verarbeitung**:
    - Das Ereignis triggert den `AX_BOOL_TO_X` Baustein.
    - Dieser steuert den `AX_SWITCH`.
3.  **Entscheidungslogik (Switch)**:
    - Der `AX_SWITCH` entscheidet basierend auf dem aktuellen Zustand (Rückkopplung), ob er den `E_SR` Baustein auf **Set** (S) oder **Reset** (R) schaltet.
    - `AX_SWITCH.EO0` ist mit `E_SR.S` verbunden.
    - `AX_SWITCH.EO1` ist mit `E_SR.R` verbunden.
4.  **Speicherung und Ausgabe**:
    - Der `E_SR` speichert den neuen Zustand.
    - Sein Ausgang `Q` geht an den Splitter `AX_SPLIT_2`.
    - **Pfad 1**: `AX_SPLIT_2.OUT1` geht direkt an den physikalischen Ausgang `DigitalOutput_Q1`, um die Lampe/Aktor zu schalten.
5.  **Rückkopplung (Feedback Loop)**:
    - **Pfad 2**: `AX_SPLIT_2.OUT2` führt das Signal zurück.
    - Es durchläuft `AX_X_TO_BOOL` und dann `AX_BOOL_TO_X`.
    - Dieses Rückkopplungssignal bestimmt für den nächsten Klick, wie der `AX_SWITCH` stehen muss, damit der Zustand das nächste Mal invertiert wird.

## Zusammenfassung
Die Übung `Uebung_004b_AX` zeigt eine komplexe Realisierung eines Stromstoßschalters (Toggle) mittels Adapter-Bausteinen. Obwohl die Lösung funktionstüchtig ist, wird sie aufgrund der hohen Anzahl an benötigten Bausteinen und der Komplexität ("Over-Engineering") in der Praxis nicht empfohlen. Sie dient jedoch als exzellentes Beispiel für das Routing von Signalen, die Verwendung von Splittern und die Logikbildung mittels Adaptern in 4diac.