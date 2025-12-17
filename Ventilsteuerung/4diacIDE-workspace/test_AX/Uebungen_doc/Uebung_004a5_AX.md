Hier ist die Dokumentation für die Übung `Uebung_004a5_AX`, basierend auf den bereitgestellten XML-Daten.

# Uebung_004a5_AX

![Uebung_004a5_AX](Uebung_004a5_AX.png)

* * * * * * * * * *

## Einleitung

Diese Übung ist eine Variation der Übung `Uebung_004a4`. Das Hauptziel besteht darin, die Verwendung von T-Flip-Flops (T_FF) in einer Adapter-basierten Umgebung (`AX`) zu demonstrieren, jedoch ohne die Verwendung eines `E_SPLIT`-Bausteins für das Ereignissignal.

In dieser Sub-Applikation wird gezeigt, wie ein einzelnes Eingangsereignis direkt an mehrere Ziele verteilt werden kann (Event-Fan-Out). Obwohl die Verwendung von zwei identischen T-Flip-Flops logisch betrachtet redundant sein mag, dient dieser Aufbau dazu, die parallele Ansteuerung ohne expliziten Splitter-Baustein zu veranschaulichen.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden spezifische Funktionsbausteine aus der `logiBUS` und `adapter` Bibliothek verwendet, um die Ein- und Ausgabe sowie die Logik zu realisieren.

### Sub-Bausteine:

#### DigitalInput_CLK_I1
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Beschreibung**: Dieser Baustein stellt die Schnittstelle zum physischen Taster dar.
- **Konfiguration**:
    - **Parameter**: `Input` = `Input_I1`
    - **Parameter**: `InputEvent` = `BUTTON_SINGLE_CLICK`
- **Funktion**: Erzeugt ein Ereignis (`IND`), wenn der Taster I1 einfach geklickt wird.

#### E_T_FF_Q1 & E_T_FF_Q2
- **Typ**: `adapter::events::unidirectional::AX_T_FF`
- **Beschreibung**: Diese Bausteine fungieren als Toggle-Flip-Flops (T-Flip-Flop) mit Adapter-Schnittstellen.
- **Funktionsweise**: Bei jedem Eingangssignal am `CLK` Eingang ändert sich der Zustand des Ausgangs (`Q`).
- **Verwendung**: Es werden zwei Instanzen dieses Bausteins verwendet, um zwei separate Ausgänge zu steuern.

#### DigitalOutput_Q1 & DigitalOutput_Q2
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Beschreibung**: Diese Bausteine stellen die Schnittstelle zu den physischen Ausgängen (z.B. LEDs) dar und nutzen Adapter-Verbindungen.
- **Konfiguration**:
    - **Instanz Q1**: Parameter `Output` = `Output_Q1`
    - **Instanz Q2**: Parameter `Output` = `Output_Q2`
- **Funktion**: Setzt den physischen Ausgang basierend auf dem Status der angeschlossenen Adapter-Logik.

## Programmablauf und Verbindungen

Der Ablauf der Übung gestaltet sich wie folgt:

1.  **Eingabe**: Das Signal beginnt beim Baustein `DigitalInput_CLK_I1`. Wenn am Eingang `Input_I1` ein einfacher Klick (`BUTTON_SINGLE_CLICK`) registriert wird, wird das `IND`-Event ausgelöst.
2.  **Verarbeitung (Signalverteilung)**:
    - Das `IND`-Event des Eingangsbausteins ist **direkt** mit zwei Zielen verbunden:
        - `E_T_FF_Q1.CLK`
        - `E_T_FF_Q2.CLK`
    - Dies demonstriert, dass in 4diac ein Event-Ausgang mehrere Event-Eingänge treiben kann, ohne dass ein `E_SPLIT`-Baustein notwendig ist. Beide Flip-Flops erhalten das Taktsignal.
3.  **Logik**: Beide T-Flip-Flops (`E_T_FF_Q1` und `E_T_FF_Q2`) wechseln ihren Zustand (Toggle) bei Erhalt des Events.
4.  **Ausgabe**:
    - Der Adapter-Ausgang `Q` von `E_T_FF_Q1` ist mit `DigitalOutput_Q1.OUT` verbunden.
    - Der Adapter-Ausgang `Q` von `E_T_FF_Q2` ist mit `DigitalOutput_Q2.OUT` verbunden.
    - Dies führt dazu, dass die Ausgänge Q1 und Q2 synchron geschaltet werden.

## Zusammenfassung

Die `Uebung_004a5_AX` verdeutlicht die direkte Verdrahtung eines Ereignis-Quellsignals auf mehrere Ziele. Sie zeigt, dass für einfache Signalverzweigungen kein separater Splitter-Baustein erforderlich ist. Das Ergebnis ist eine synchrone Steuerung der Ausgänge Q1 und Q2 durch einen einzelnen Tasterdruck auf I1, realisiert durch Adapter-basierte T-Flip-Flops.