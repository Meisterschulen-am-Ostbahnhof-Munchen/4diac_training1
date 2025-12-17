Hier ist die Dokumentationsseite für die Übung `Uebung_002a5b` basierend auf den bereitgestellten XML-Daten.

# Uebung_002a5b

![Uebung_002a5b](Uebung_002a5b.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Verarbeitung digitaler Signale unter Verwendung einer logischen ODER-Verknüpfung. Konkret werden drei digitale Eingänge (Input I1 bis I3) eingelesen, logisch miteinander verknüpft und das Ergebnis auf drei digitale Ausgänge (Output Q1 bis Q3) verteilt. Das Ziel ist es, zu verstehen, wie mehrere Eingänge in einem Logikbaustein verarbeitet werden und wie ein resultierendes Signal mehrere Ausgänge gleichzeitig steuern kann.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden verschiedene Funktionsbausteine instanziiert, um die Eingabe, Verarbeitung und Ausgabe der Signale zu realisieren.

### Sub-Bausteine: Digitale Eingänge
- **Typ**: `logiBUS::io::DI::logiBUS_IX`
- **Verwendete interne FBs**:
    - **DigitalInput_I1**: `logiBUS_IX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Input` = `Input_I1`
    - **DigitalInput_I2**: `logiBUS_IX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Input` = `Input_I2`
    - **DigitalInput_I3**: `logiBUS_IX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Input` = `Input_I3`
- **Funktionsweise**: Diese Bausteine lesen die physikalischen oder simulierten digitalen Eingänge 1, 2 und 3 ein. Bei einer Änderung des Signalzustands wird ein Event (`IND`) ausgelöst und der Datenwert (`IN`) bereitgestellt.

### Sub-Bausteine: Logik-Verarbeitung
- **Typ**: `iec61131::bitwiseOperators::OR_3_BOOL`
- **Verwendete interne FBs**:
    - **OR_3_BOOL**: `OR_3_BOOL`
        - Dateneingänge: `IN1`, `IN2`, `IN3` (verbunden mit den digitalen Eingängen)
        - Datenausgang: `OUT` (verbunden mit den digitalen Ausgängen)
- **Funktionsweise**: Dieser Baustein führt eine logische ODER-Operation mit drei Booleschen Eingängen durch. Der Ausgang `OUT` ist `TRUE`, wenn mindestens einer der Eingänge `IN1`, `IN2` oder `IN3` `TRUE` ist.

### Sub-Bausteine: Digitale Ausgänge
- **Typ**: `logiBUS::io::DQ::logiBUS_QX`
- **Verwendete interne FBs**:
    - **DigitalOutput_Q1**: `logiBUS_QX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q1`
    - **DigitalOutput_Q2**: `logiBUS_QX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q2`
    - **DigitalOutput_Q3**: `logiBUS_QX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q3`
- **Funktionsweise**: Diese Bausteine steuern die digitalen Ausgänge. Sie erhalten den zu schaltenden Wert über den Dateneingang `OUT`.

## Programmablauf und Verbindungen

Der Ablauf innerhalb der Übung wird durch Event- und Datenverbindungen gesteuert:

1.  **Eingabeverarbeitung**:
    *   Die Events `IND` von `DigitalInput_I1`, `DigitalInput_I2` und `DigitalInput_I3` sind alle mit dem Event-Eingang `REQ` des `OR_3_BOOL`-Bausteins verbunden. Das bedeutet, sobald sich einer der Eingänge ändert, wird die Logikberechnung angestoßen.
    *   Die Daten `IN` der Eingangsbausteine werden an die entsprechenden Eingänge `IN1`, `IN2` und `IN3` des ODER-Bausteins geleitet.

2.  **Logische Verknüpfung**:
    *   Der `OR_3_BOOL` Baustein prüft, ob mindestens eines der Eingangssignale aktiv (`TRUE`) ist.

3.  **Ausgabesteuerung**:
    *   Nach Abschluss der Berechnung löst der ODER-Baustein das Event `CNF` aus. Dieses Event ist mit den `REQ`-Eingängen aller drei Ausgangsbausteine (`DigitalOutput_Q1`, `Q2`, `Q3`) verbunden.
    *   Das Ergebnis der ODER-Verknüpfung (`OUT`) wird an die Dateneingänge `OUT` aller drei Ausgangsbausteine übertragen.

**Lernziele:**
*   Verständnis der `OR` (ODER) Logik mit mehr als zwei Eingängen.
*   Verkettung von Events (Eingang -> Verarbeitung -> Ausgang).
*   Verteilung (Broadcasting) eines Signalsignals auf mehrere Aktoren/Ausgänge.

## Zusammenfassung

Die Übung `Uebung_002a5b` realisiert eine parallele Ansteuerung von drei Ausgängen (Q1, Q2, Q3) basierend auf dem Zustand von drei Eingängen (I1, I2, I3). Durch die Verwendung eines 3-fach ODER-Bausteins werden alle Ausgänge aktiviert, sobald auch nur einer der drei Eingänge aktiv ist. Dies verdeutlicht effizientes Signalrouting und logische Grundfunktionen in 4diac.