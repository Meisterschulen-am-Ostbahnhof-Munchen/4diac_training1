Hier ist die Dokumentation für die Übung basierend auf den bereitgestellten XML-Daten.

# Uebung_090a2_AX

![Uebung_090a2_AX](Uebung_090a2_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des Funktionsbausteins `AX_MUX_3`. Ziel ist es, Adapter-Verbindungen basierend auf einem Steuersignal umzuschalten. Dabei wird gezeigt, wie ein digitaler Eingang genutzt wird, um zu steuern, welcher Adapter-Eingang an einen Adapter-Ausgang weitergeleitet wird.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application kommen folgende Bausteine zum Einsatz:

*   **F_MUX_3** (`adapter::selection::unidirectional::AX_MUX_3`)
    *   Dieser Baustein ist ein Multiplexer für Adapter-Verbindungen. Er schaltet basierend auf dem Integer-Eingang `K` einen der Eingänge (`IN1`, `IN2`, etc.) auf den Ausgang `OUT`.
*   **DigitalInput_I4** (`logiBUS::io::DI::logiBUS_IX`)
    *   Ein digitaler Standard-Eingang (Bit), der als Steuersignal fungiert.
    *   Parameter: `Input` = `Input_I4`
*   **F_BOOL_TO_UINT_I4** (`iec61131::conversion::F_BOOL_TO_UINT`)
    *   Ein Konvertierungsbaustein, der das boolesche Signal von I4 in einen Unsigned Integer umwandelt, damit es vom Multiplexer verarbeitet werden kann.
*   **DigitalOutput_Q1** (`logiBUS::io::DQ::logiBUS_QXA`)
    *   Ein Adapter-Ausgang, an den das gewählte Signal weitergeleitet wird.
    *   Parameter: `Output` = `Output_Q1`
*   **DigitalInput_I1** (`logiBUS::io::DI::logiBUS_IXA`)
    *   Ein Adapter-Eingang (Kanal 1).
    *   Parameter: `Input` = `Input_I1`
*   **DigitalInput_I2** (`logiBUS::io::DI::logiBUS_IXA`)
    *   Ein Adapter-Eingang (Kanal 2).
    *   Parameter: `Input` = `Input_I2`

## Programmablauf und Verbindungen

Der Ablauf der Schaltung lässt sich wie folgt beschreiben:

1.  **Signalerfassung und Umwandlung:**
    *   Der digitale Eingang `DigitalInput_I4` liefert ein boolesches Signal (TRUE/FALSE).
    *   Dieses Signal löst über das Event `IND` den Baustein `F_BOOL_TO_UINT_I4` aus.
    *   Der Konverter wandelt den booleschen Wert in eine Ganzzahl (UINT) um: `FALSE` wird zu `0`, `TRUE` wird zu `1`.

2.  **Multiplexer-Steuerung:**
    *   Das konvertierte Integer-Signal wird an den Selektor-Eingang `K` des Multiplexers `F_MUX_3` übergeben.
    *   Das `CNF`-Event des Konverters triggert das `REQ`-Event des Multiplexers, um die Umschaltung zu aktualisieren.

3.  **Adapter-Routing:**
    *   Der Multiplexer `F_MUX_3` verfügt über zwei angeschlossene Adapter-Quellen:
        *   `DigitalInput_I1` ist an `IN1` angeschlossen.
        *   `DigitalInput_I2` ist an `IN2` angeschlossen.
    *   Der Ausgang des Multiplexers `OUT` ist mit dem Adapter-Ausgang `DigitalOutput_Q1` verbunden.

**Funktionsweise der Auswahl:**
*   Wenn **I4 = TRUE** ist, liegt am Eingang `K` der Wert **1** an. Der Multiplexer verbindet `IN1` (I1) mit `OUT` (Q1).
*   Wenn **I4 = FALSE** ist, liegt am Eingang `K` der Wert **0** an.

*Hinweis zur Logik:* Da der Steuereingang nur ein Bit breit ist (I4), kann in dieser spezifischen Konfiguration nur zwischen dem Zustand 0 und 1 gewechselt werden. Der Eingang `IN2` (I2), der logisch dem Wert `K=2` entsprechen würde, ist zwar verdrahtet, kann aber durch den einfachen Schalter I4 in diesem Aufbau nicht direkt angewählt werden (dafür wäre ein Integer-Eingang oder eine Logik notwendig, die Werte > 1 erzeugt). Die Übung zeigt somit primär das Prinzip der Adapter-Durchschaltung am Beispiel von Kanal 1.

## Zusammenfassung
Diese Übung veranschaulicht die Handhabung von Adaptern in 4diac. Sie zeigt, wie man Adapter-Ströme (hier repräsentiert durch `IXA` und `QXA` Bausteine) mithilfe logischer Standard-Bausteine (`AX_MUX`) dynamisch umschalten kann. Zudem wird die Notwendigkeit der Datentypkonvertierung (`BOOL` zu `UINT`) deutlich, um binäre Schaltersignale für Selektions-Eingänge nutzbar zu machen.