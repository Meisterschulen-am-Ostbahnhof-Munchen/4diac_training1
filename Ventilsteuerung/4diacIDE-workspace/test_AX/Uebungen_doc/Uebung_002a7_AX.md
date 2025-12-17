# Uebung_002a7_AX: DigitalInput_I1-3 mit XOR auf DigitalOutput_Q1, mit Plug and Socket

(Bild der Übung ist nicht vorhanden)

* * * * * * * * * *
## Einleitung
Diese Übung demonstriert die Verwendung digitaler Eingänge (I1, I2, I3) in Kombination mit einer dreifachen Exklusiv-Oder (XOR)-Verknüpfung, um einen digitalen Ausgang (Q1) zu steuern. Die Logik wird unter Verwendung von 4diac-IDE Funktionsbausteinen realisiert, wobei ein spezifischer Adapter-Baustein für die XOR-Funktion zum Einsatz kommt und die Verbindungen über "Plug and Socket"-Mechanismen erfolgen. Das Ziel ist es, den Ausgang Q1 zu aktivieren, wenn eine ungerade Anzahl der Eingänge I1, I2 oder I3 aktiv (TRUE) ist.

## Verwendete Funktionsbausteine (FBs)

*   **`DigitalInput_I1`** (Typ: `logiBUS::io::DI::logiBUS_IXA`)
    *   **Parameter**: `QI = TRUE`, `Input = Input_I1`
    *   **Funktion**: Dieser Baustein liest den aktuellen logischen Zustand (TRUE/FALSE) des digitalen Eingangs I1 und stellt ihn am Datenausgang `IN` zur Verfügung.
*   **`DigitalInput_I2`** (Typ: `logiBUS::io::DI::logiBUS_IXA`)
    *   **Parameter**: `QI = TRUE`, `Input = Input_I2`
    *   **Funktion**: Dieser Baustein liest den aktuellen logischen Zustand (TRUE/FALSE) des digitalen Eingangs I2 und stellt ihn am Datenausgang `IN` zur Verfügung.
*   **`DigitalInput_I3`** (Typ: `logiBUS::io::DI::logiBUS_IXA`)
    *   **Parameter**: `QI = TRUE`, `Input = Input_I3`
    *   **Funktion**: Dieser Baustein liest den aktuellen logischen Zustand (TRUE/FALSE) des digitalen Eingangs I3 und stellt ihn am Datenausgang `IN` zur Verfügung.
*   **`DigitalOutput_Q1`** (Typ: `logiBUS::io::DQ::logiBUS_QXA`)
    *   **Parameter**: `QI = TRUE`, `Output = Output_Q1`
    *   **Funktion**: Dieser Baustein setzt den digitalen Ausgang Q1 auf den logischen Zustand, der an seinem Dateneingang `OUT` anliegt.

### Sub-Bausteine: AX_XOR_3
    - **Typ**: `adapter::booleanOperators::AX_XOR_3`
    - **Verwendete interne FBs**: (Informationen sind aus den bereitgestellten Dateiinhalten nicht direkt ableitbar)
    - **Funktionsweise**: Dieser Funktionsbaustein implementiert eine Exklusiv-Oder (XOR)-Logik mit drei Eingängen. Das Ergebnis (Datenausgang `OUT`) ist `TRUE`, wenn eine ungerade Anzahl der Dateneingänge (`IN1`, `IN2`, `IN3`) den Wert `TRUE` aufweist. Ist eine gerade Anzahl der Eingänge `TRUE` oder sind alle `FALSE`, so ist das Ergebnis `FALSE`.
        - **Dateneingänge**:
            - `IN1`: Boolean
            - `IN2`: Boolean
            - `IN3`: Boolean
        - **Datenausgang**:
            - `OUT`: Boolean

## Programmablauf und Verbindungen

Der Programmablauf dieser Übung ist wie folgt strukturiert:

1.  **Eingangswerte erfassen**: Die Funktionsbausteine `DigitalInput_I1`, `DigitalInput_I2` und `DigitalInput_I3` erfassen kontinuierlich die Zustände der physikalischen digitalen Eingänge I1, I2 und I3. Die gelesenen Boolean-Werte werden an ihren jeweiligen Datenausgängen `IN` bereitgestellt.
2.  **XOR-Verknüpfung**: Die Ausgänge der drei Eingangs-Bausteine werden mit den Eingängen des `AX_XOR_3`-Bausteins verbunden:
    *   Der Datenausgang `IN` von `DigitalInput_I1` wird mit dem Dateneingang `IN1` von `AX_XOR_3` verbunden.
    *   Der Datenausgang `IN` von `DigitalInput_I2` wird mit dem Dateneingang `IN2` von `AX_XOR_3` verbunden.
    *   Der Datenausgang `IN` von `DigitalInput_I3` wird mit dem Dateneingang `IN3` von `AX_XOR_3` verbunden.
    Der `AX_XOR_3`-Baustein führt die logische XOR-Operation mit diesen drei Eingangswerten durch.
3.  **Ausgang steuern**: Der Datenausgang `OUT` des `AX_XOR_3`-Bausteins wird mit dem Dateneingang `OUT` des `DigitalOutput_Q1`-Bausteins verbunden. Das Ergebnis der XOR-Operation wird somit direkt an den digitalen Ausgang Q1 weitergeleitet, der dann entsprechend seinen Zustand ändert.

Zusammenfassend bedeutet dies, dass der digitale Ausgang Q1 aktiv (TRUE) wird, wenn entweder nur ein Eingang (I1, I2 oder I3) aktiv ist, oder wenn alle drei Eingänge (I1, I2 und I3) aktiv sind. Wenn keiner der Eingänge aktiv ist oder genau zwei Eingänge aktiv sind, bleibt der Ausgang Q1 inaktiv (FALSE).

## Zusammenfassung
Diese Übung demonstriert eine grundlegende Steuerungsschaltung unter Verwendung von drei digitalen Eingängen und einer dreifachen XOR-Logik zur Ansteuerung eines digitalen Ausgangs. Sie zeigt die Verknüpfung von I/O-Bausteinen mit einem Adapter-Baustein für komplexe Logikfunktionen und verdeutlicht den Datenfluss innerhalb einer 4diac-Anwendung. Die Übung ist ideal, um das Verständnis für logische Operationen und die Verbindung von Funktionsbausteinen in der 4diac-IDE zu vertiefen.