Hier ist die Dokumentation für die Übung `Uebung_095_AX` basierend auf den bereitgestellten XML-Daten.

# Uebung_095_AX

![Uebung_095_AX](Uebung_095_AX.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Verwendung des `AX_SELECT` Bausteins in Kombination mit Adaptern innerhalb einer IEC 61499 Anwendung. Das Ziel ist es, zu zeigen, wie Ereignisströme basierend auf einem Zustand (Adapter-Datenwert) umgeschaltet werden können. Die Schaltung realisiert eine Auswahlsteuerung, bei der entschieden wird, welcher Taster ein Toggle-Flip-Flop (T-FF) ansteuert, um einen Ausgang zu schalten.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden verschiedene Bausteine aus der `logiBUS` und `adapter` Bibliothek verschaltet. Im Folgenden werden die instanzierten Bausteine im Detail beschrieben.

### Sub-Bausteine: DigitalInput_I1
- **Typ**: `logiBUS::io::DI::logiBUS_IXA`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalInput_I1
        - **Parameter**: 
            - `QI` = `TRUE`
            - `Input` = `Input_I1`
        - **Datenausgang/-eingang**: Der Adapter-Anschluss `IN` liefert den Zustand des physikalischen Eingangs I1.
- **Funktionsweise**: Dieser Baustein stellt den Zustand des digitalen Eingangs 1 (z.B. ein Schalter) als Adapter-Signal zur Verfügung. Er dient als Wahlschalter für den Selektor.

### Sub-Bausteine: DigitalInput_CLK_I2
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalInput_CLK_I2
        - **Parameter**: 
            - `QI` = `TRUE`
            - `Input` = `Input_I2`
            - `InputEvent` = `BUTTON_SINGLE_CLICK`
        - **Ereignisausgang/-eingang**: Der Ausgang `IND` feuert ein Event bei einem einfachen Klick auf Eingang I2.
- **Funktionsweise**: Erfasst Klicks auf dem Taster an Eingang 2 und sendet ein Ereignis. Dient als erste mögliche Ereignisquelle.

### Sub-Bausteine: DigitalInput_CLK_I3
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalInput_CLK_I3
        - **Parameter**: 
            - `QI` = `TRUE`
            - `Input` = `Input_I3`
            - `InputEvent` = `BUTTON_SINGLE_CLICK`
        - **Ereignisausgang/-eingang**: Der Ausgang `IND` feuert ein Event bei einem einfachen Klick auf Eingang I3.
- **Funktionsweise**: Erfasst Klicks auf dem Taster an Eingang 3 und sendet ein Ereignis. Dient als zweite mögliche Ereignisquelle.

### Sub-Bausteine: E_SELECT
- **Typ**: `adapter::events::unidirectional::AX_SELECT`
- **Verwendete interne FBs**:
    - **Bausteinname**: E_SELECT
        - **Ereignisausgang/-eingang**: Eingänge `EI0` und `EI1`, Ausgang `EO`.
        - **Datenausgang/-eingang**: Adapter-Eingang `G` (Gate/Select).
- **Funktionsweise**: Dieser Baustein leitet Ereignisse von einem der beiden Eingänge (`EI0` oder `EI1`) an den Ausgang (`EO`) weiter. Welcher Eingang aktiv ist, wird durch den Zustand am Adapter-Anschluss `G` bestimmt.

### Sub-Bausteine: E_T_FF
- **Typ**: `adapter::events::unidirectional::AX_T_FF`
- **Verwendete interne FBs**:
    - **Bausteinname**: E_T_FF
        - **Ereignisausgang/-eingang**: Eingang `CLK`.
        - **Datenausgang/-eingang**: Adapter-Ausgang `Q`.
- **Funktionsweise**: Ein Toggle-Flip-Flop auf Adapter-Basis. Bei jedem eingehenden Ereignis am `CLK`-Eingang wechselt der logische Zustand des Adapter-Ausgangs `Q` (von TRUE auf FALSE oder umgekehrt).

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalOutput_Q1
        - **Parameter**: 
            - `QI` = `TRUE`
            - `Output` = `Output_Q1`
        - **Datenausgang/-eingang**: Adapter-Eingang `OUT` empfängt den zu setzenden Zustand.
- **Funktionsweise**: Dieser Baustein steuert den physischen Ausgang Q1 an. Der Zustand wird über die Adapter-Verbindung empfangen.

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich wie folgt beschreiben:

1.  **Auswahl der Quelle (I1):**
    Der Schalter an Eingang I1 (`DigitalInput_I1`) ist über eine Adapter-Verbindung mit dem Eingang `G` des Bausteins `E_SELECT` verbunden.
    *   Ist I1 `FALSE` (0), wird der Pfad `EI0` ausgewählt.
    *   Ist I1 `TRUE` (1), wird der Pfad `EI1` ausgewählt.

2.  **Ereigniserzeugung (I2 und I3):**
    *   Der Taster I2 (`DigitalInput_CLK_I2`) sendet bei Betätigung ein Event an `EI0` des Selektors.
    *   Der Taster I3 (`DigitalInput_CLK_I3`) sendet bei Betätigung ein Event an `EI1` des Selektors.

3.  **Selektion und Weiterleitung:**
    Abhängig von der Stellung des Schalters I1 wird entweder das Klick-Event von I2 oder das von I3 durch den `E_SELECT` Baustein an den Ausgang `EO` durchgelassen.

4.  **Verarbeitung (Toggle):**
    Das durchgelassene Event am Ausgang `EO` triggert den Eingang `CLK` des `E_T_FF`. Dies führt dazu, dass das Flip-Flop seinen internen Zustand umschaltet (Toggelt).

5.  **Ausgabe (Q1):**
    Der Zustand des Flip-Flops (`Q`) wird über eine Adapter-Verbindung direkt an den Ausgangsbaustein `DigitalOutput_Q1` übertragen, welcher die Lampe an Q1 entsprechend ein- oder ausschaltet.

**Zusammenfassend:** Mit dem Schalter I1 wählt man aus, ob Taster I2 oder Taster I3 das Licht Q1 ein- und ausschalten darf.

## Zusammenfassung

Die Übung `Uebung_095_AX` ist ein praktisches Beispiel für die Ereignissteuerung mittels Adaptern (`AX`-Bausteine). Sie vermittelt das Verständnis für bedingte Ereignisweiterleitung (`AX_SELECT`) und zustandsbasierte Logik (`AX_T_FF`) unter Verwendung der logiBUS-Schnittstellen für Hardware-IOs.