Hier ist die Dokumentation für die Übung `Uebung_004a4_AX` basierend auf den bereitgestellten Daten.

# Uebung_004a4_AX

*(Hier Platzhalter für ein Bild der Übung einfügen)*

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Schaltung, bei der ein Toggle Flip-Flop (T-FF) durch ein Eingangs-Event gesteuert wird. Konkret wird hier auf einen einfachen Tastendruck (`BUTTON_SINGLE_CLICK`) reagiert. Ein wesentliches Lernziel dieser Übung ist die Demonstration des `E_SPLIT` Bausteins, welcher ein einzelnes Event-Signal aufteilt, um zwei separate Funktionsbausteine parallel anzusteuern.

## Verwendete Funktionsbausteine (FBs)

In dieser SubApplikation werden verschiedene Bausteine verschaltet, um die Eingabeverarbeitung, Signalaufteilung und Ausgabe zu realisieren.

### Sub-Bausteine: Uebung_004a4_AX
- **Typ**: SubAppType
- **Verwendete interne FBs**:

    - **DigitalInput_CLK_I1**: `logiBUS::io::DI::logiBUS_IE`
        - **Parameter**: 
            - `Input` = `Input_I1`
            - `InputEvent` = `BUTTON_SINGLE_CLICK`
            - `QI` = `TRUE` (nicht sichtbar)
        - **Ereignisausgang**: `IND` (Indication - Signalisiert das Eintreten des Events)
        - **Funktionsweise**: Dieser Baustein überwacht den Eingang I1 auf das Ereignis "Einfacher Klick" und sendet daraufhin ein Event.

    - **E_SPLIT**: `iec61499::events::E_SPLIT`
        - **Ereigniseingang**: `EI`
        - **Ereignisausgänge**: `EO1`, `EO2`
        - **Funktionsweise**: Dient dazu, einen eingehenden Event-Strom (EI) auf zwei Ausgänge (EO1 und EO2) aufzuteilen, um parallele Ausführungspfade zu ermöglichen.

    - **E_T_FF_Q1**: `adapter::events::unidirectional::AX_T_FF`
        - **Ereigniseingang**: `CLK`
        - **Datenausgang (Adapter)**: `Q`
        - **Funktionsweise**: Ein Toggle Flip-Flop, das bei jedem `CLK` Event seinen Zustand wechselt (Adapter-basiert).

    - **E_T_FF_Q2**: `adapter::events::unidirectional::AX_T_FF`
        - **Ereigniseingang**: `CLK`
        - **Datenausgang (Adapter)**: `Q`
        - **Funktionsweise**: Zweites Toggle Flip-Flop, identisch zu Q1.

    - **DigitalOutput_Q1**: `logiBUS::io::DQ::logiBUS_QXA`
        - **Parameter**: 
            - `Output` = `Output_Q1`
            - `QI` = `TRUE` (nicht sichtbar)
        - **Dateneingang (Adapter)**: `OUT`
        - **Funktionsweise**: Steuert den physischen Ausgang Q1 an.

    - **DigitalOutput_Q2**: `logiBUS::io::DQ::logiBUS_QXA`
        - **Parameter**: 
            - `Output` = `Output_Q2`
            - `QI` = `TRUE` (nicht sichtbar)
        - **Dateneingang (Adapter)**: `OUT`
        - **Funktionsweise**: Steuert den physischen Ausgang Q2 an.

## Programmablauf und Verbindungen

Der Ablauf der Übung gestaltet sich wie folgt:

1.  **Eingabeerkennung**: Der Baustein `DigitalInput_CLK_I1` wartet auf das Ereignis `BUTTON_SINGLE_CLICK` am Eingang `Input_I1`.
2.  **Event-Verarbeitung**: Sobald der Klick erkannt wird, wird das Event `IND` ausgelöst.
3.  **Signal-Split**: Das Event gelangt in den `E_SPLIT` Baustein (Eingang `EI`). Dieser dupliziert das Event und gibt es an `EO1` und `EO2` aus.
4.  **Logik-Schaltung**:
    *   Der Ausgang `EO1` ist mit dem `CLK`-Eingang von `E_T_FF_Q1` verbunden.
    *   Der Ausgang `EO2` ist mit dem `CLK`-Eingang von `E_T_FF_Q2` verbunden.
5.  **Zustandswechsel**: Beide Flip-Flops wechseln bei Empfang des Events ihren internen Zustand (Toggle).
6.  **Ausgabe**: Die Adapter-Ausgänge (`Q`) der Flip-Flops sind direkt mit den Adapter-Eingängen (`OUT`) der Ausgangsbausteine `DigitalOutput_Q1` und `DigitalOutput_Q2` verbunden, wodurch die physischen Ausgänge geschaltet werden.

**Hinweis zur Übung:**
In der Übung ist ein Kommentar hinterlegt, der darauf hinweist, dass die Verwendung von zwei separaten Toggle-Flip-Flops (T_FF) für denselben Zweck in einer realen Anwendung redundant wäre. Der Aufbau dient hier explizit dazu, die Funktionsweise und den Nutzen des `E_SPLIT` Bausteins didaktisch zu veranschaulichen.

## Zusammenfassung
Die `Uebung_004a4_AX` demonstriert die Verarbeitung von Eingabe-Events (Single Click) und deren Verteilung mittels `E_SPLIT` auf mehrere Signalpfade. Sie zeigt zudem die Anbindung von Hardware-Ausgängen über Adapter-Technologie (`AX_T_FF` zu `logiBUS_QXA`).