Hier ist die Dokumentation für die Übung `Uebung_094a_AX`, basierend auf den bereitgestellten XML-Daten.

# Uebung_094a_AX

![Bild der Übung, falls vorhanden](Pfad_zum_Bild_placeholder.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Verwendung des `QI` (Qualifier Input) Eingangs anstelle eines expliziten `PERMIT`-Bausteins, um die Verarbeitung von Signalen zu steuern. Das Ziel ist es, einen Signalpfad (von I1 nach Q1) basierend auf einem Zustand, der durch einen Taster (I2) getoggled wird, zu aktivieren oder zu deaktivieren.

Zusätzlich zeigt die Übung den Umgang mit Adapter-Bausteinen (`AX_...`) für Flip-Flops und Signalwandlung.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden verschiedene logiBUS-IO-Bausteine sowie Adapter-Logikbausteine verwendet.

### Bausteinliste

-   **DigitalInput_I1**
    -   **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    -   **Beschreibung**: Adapter-basierter digitaler Eingang.
    -   **Parameter**: `Input` = `Input_I1`
    -   **Funktion**: Liest den Status des physischen Eingangs I1. Der Eingang `QI` steuert hierbei, ob der Baustein aktiv ist.

-   **DigitalInput_CLK_I2**
    -   **Typ**: `logiBUS::io::DI::logiBUS_IE`
    -   **Beschreibung**: Digitaler Eingang für Events.
    -   **Parameter**:
        -   `QI` = `TRUE`
        -   `Input` = `Input_I2`
        -   `InputEvent` = `BUTTON_SINGLE_CLICK`
    -   **Funktion**: Erzeugt ein Event (IND), wenn der Taster I2 einfach geklickt wird.

-   **E_T_FF**
    -   **Typ**: `adapter::events::unidirectional::AX_T_FF`
    -   **Beschreibung**: Adapter-basiertes Toggle-Flip-Flop (T-Flip-Flop).
    -   **Funktion**: Wechselt seinen internen Zustand bei jedem eingehenden Event am `CLK`-Eingang.

-   **DigitalOutput_Q1**
    -   **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    -   **Beschreibung**: Adapter-basierter digitaler Ausgang.
    -   **Parameter**:
        -   `QI` = `TRUE`
        -   `Output` = `Output_Q1`
    -   **Funktion**: Gibt das Signal von I1 aus, sofern dieser aktiv ist.

-   **DigitalOutput_Q2**
    -   **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    -   **Beschreibung**: Adapter-basierter digitaler Ausgang.
    -   **Parameter**:
        -   `QI` = `TRUE`
        -   `Output` = `Output_Q2`
    -   **Funktion**: Zeigt den aktuellen Status des Toggle-Flip-Flops an.

-   **AX_X_TO_BOOL**
    -   **Typ**: `adapter::conversion::unidirectional::AX_X_TO_BOOL`
    -   **Beschreibung**: Konvertierungsbaustein.
    -   **Funktion**: Wandelt ein Adapter-Signal in ein einfaches Boolesches Datensignal um.

-   **AX_SPLIT_2**
    -   **Typ**: `adapter::events::unidirectional::AX_SPLIT_2`
    -   **Beschreibung**: Signalverteiler (Splitter).
    -   **Funktion**: Teilt eine Adapter-Verbindung auf zwei Ausgänge auf.

## Programmablauf und Verbindungen

Das Netzwerk realisiert eine schaltbare Durchleitung eines Signals. Der Ablauf ist wie folgt:

1.  **Status-Wechsel (Toggling):**
    -   Der Eingang `DigitalInput_CLK_I2` überwacht den Taster `Input_I2`.
    -   Bei einem einfachen Klick (`BUTTON_SINGLE_CLICK`) wird ein Event (`IND`) an den Takteingang (`CLK`) des Toggle-Flip-Flops `E_T_FF` gesendet.
    -   Der Adapter-Ausgang `Q` des Flip-Flops wechselt daraufhin seinen Zustand (Ein/Aus).

2.  **Signalverteilung:**
    -   Das Ausgangssignal des Flip-Flops geht an den Splitter `AX_SPLIT_2`.
    -   **Pfad 1 (Anzeige):** `OUT2` des Splitters ist direkt mit `DigitalOutput_Q2` verbunden. Somit zeigt Q2 immer den aktuellen Zustand des Flip-Flops an (Statusanzeige).
    -   **Pfad 2 (Steuerung):** `OUT1` des Splitters geht an den Konverter `AX_X_TO_BOOL`.

3.  **Steuerung über QI:**
    -   Der Konverter `AX_X_TO_BOOL` wandelt den Adapter-Status in ein Boolesches Signal (`IN`) und ein Bestätigungs-Event (`CNF`) um.
    -   Dieses Boolesche Signal ist mit dem `QI` (Qualifier Input) des Bausteins `DigitalInput_I1` verbunden.
    -   Das Event `CNF` triggert die Initialisierung (`INIT`) von `DigitalInput_I1`.

4.  **Signalpfad I1 -> Q1:**
    -   Ist das Flip-Flop **TRUE**, wird `QI` von `DigitalInput_I1` auf TRUE gesetzt. Der Baustein ist aktiv, liest `Input_I1` und leitet das Signal über die Adapter-Verbindung an `DigitalOutput_Q1` weiter.
    -   Ist das Flip-Flop **FALSE**, wird `QI` von `DigitalInput_I1` auf FALSE gesetzt. Der Baustein `DigitalInput_I1` wird deaktiviert. Das Signal von I1 wird nicht mehr an Q1 weitergeleitet (bzw. Q1 wird nicht mehr aktualisiert/angesteuert).

**Lernziele:**
-   Verständnis des `QI`-Eingangs zur Aktivierung/Deaktivierung von Funktionsbausteinen.
-   Nutzung von Adapter-Bausteinen für Logik (T-FF) und Signalfluss.
-   Konvertierung von Adapter-Signalen zu Standard-Datentypen.

## Zusammenfassung

Die Übung `Uebung_094a_AX` zeigt eine elegante Methode, um einen Signalfluss bedingt zu aktivieren. Anstatt das Datensignal selbst durch ein UND-Gatter oder einen PERMIT-Baustein zu führen, wird der Quell-Baustein (`DigitalInput_I1`) direkt über seinen `QI`-Eingang ein- oder ausgeschaltet. Der Schaltzustand wird dabei über einen Taster (I2) und ein Toggle-Flip-Flop gesteuert und parallel auf Ausgang Q2 visualisiert.