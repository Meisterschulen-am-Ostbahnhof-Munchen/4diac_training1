# Uebung_003_AX: DigitalInput_I1/_I2 auf DigitalOutput_Q1/_I2 - flach mit Adapter

********************
## Einleitung
Diese Übung demonstriert eine einfache Weiterleitung von digitalen Eingangssignalen auf digitale Ausgangssignale. Die Implementierung erfolgt "flach" mithilfe von Adapter-Funktionsbausteinen, um digitale Eingänge direkt auf digitale Ausgänge abzubilden. Konkret werden die Signale der digitalen Eingänge I1 und I2 direkt an die digitalen Ausgänge Q1 und Q2 weitergeleitet.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden die folgenden externen Funktionsbausteine verwendet, um die Ein- und Ausgänge zu verwalten:

*   **Bausteinname**: `DigitalOutput_Q1`
    - **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    - Parameter:
        - `QI` = `TRUE`
        - `Output` = `Output_Q1`
    - Funktionsweise: Dieser Baustein repräsentiert den digitalen Ausgang Q1. Er ist dafür verantwortlich, den empfangenen Wert auf den physikalischen Ausgang Q1 auszugeben.
*   **Bausteinname**: `DigitalInput_I1`
    - **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    - Parameter:
        - `QI` = `TRUE`
        - `Input` = `Input_I1`
    - Funktionsweise: Dieser Baustein liest den Zustand des physikalischen digitalen Eingangs I1 und stellt ihn zur Weiterverarbeitung bereit.
*   **Bausteinname**: `DigitalOutput_Q2`
    - **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    - Parameter:
        - `QI` = `TRUE`
        - `Output` = `Output_Q2`
    - Funktionsweise: Dieser Baustein repräsentiert den digitalen Ausgang Q2 und gibt den empfangenen Wert auf den physikalischen Ausgang Q2 aus.
*   **Bausteinname**: `DigitalInput_I2`
    - **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    - Parameter:
        - `QI` = `TRUE`
        - `Input` = `Input_I2`
    - Funktionsweise: Dieser Baustein liest den Zustand des physikalischen digitalen Eingangs I2 und stellt ihn zur Weiterverarbeitung bereit.

## Programmablauf und Verbindungen
Der Programmablauf dieser Übung ist sehr einfach und direkt:

1.  Der digitale Eingang `DigitalInput_I1` liest seinen Zustand ein. Das Ausgangssignal (`IN`) dieses Bausteins wird direkt mit dem Eingang (`OUT`) des `DigitalOutput_Q1` Bausteins verbunden.
2.  In gleicher Weise liest der digitale Eingang `DigitalInput_I2` seinen Zustand ein. Das Ausgangssignal (`IN`) dieses Bausteins wird direkt mit dem Eingang (`OUT`) des `DigitalOutput_Q2` Bausteins verbunden.

Somit wird jeder digitale Eingang direkt auf den entsprechenden digitalen Ausgang umgeleitet. Es gibt keine zusätzliche Logik oder Verarbeitung zwischen den Eingangs- und Ausgangsbausteinen.

Diese Übung ist ideal für Anfänger, um die grundlegende Verwendung und Verbindung von I/O-Funktionsbausteinen in 4diac-IDE zu verstehen und die direkte Signalweiterleitung zu erlernen.

## Zusammenfassung
Die Übung "Uebung_003_AX" bietet eine klare und einfache Demonstration der direkten Signalweiterleitung von digitalen Eingängen auf digitale Ausgänge mithilfe von speziellen Adapter-Funktionsbausteinen. Sie ist ein grundlegendes Beispiel dafür, wie externe I/O-Schnittstellen in einer 4diac-Applikation integriert und miteinander verbunden werden können, ohne dass komplexe Steuerungslogik dazwischengeschaltet ist.