Hier ist die Dokumentation für die Übung `Uebung_002b3_AX` basierend auf den bereitgestellten Daten.

# Uebung_002b3_AX

![Bild der Übung Uebung_002b3_AX](Uebung_002b3_AX.png)

* * * * * * * * * *

## Einleitung
Die Übung **Uebung_002b3_AX** realisiert eine kombinatorische Logiksteuerung unter Verwendung von Adapter-Verbindungen (`AX`-Typen) im LogiBUS-System. Ziel der Übung ist es, drei digitale Eingänge (`Input_I1`, `Input_I2`, `Input_I3`) so zu verknüpfen, dass sie einen digitalen Ausgang (`Output_Q1`) steuern. Die Logik entspricht dabei der Booleschen Formel: `Q1 = (I1 AND I2) OR I3`.

Besonderes Merkmal dieser Übung ist die Verwendung von Adapter-Bausteinen für die booleschen Operationen und die I/O-Anbindung, wodurch explizite Konvertierungsbausteine (wie `F_MOVE`) entfallen.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden spezialisierte Bausteine für das LogiBUS-System sowie Adapter-basierte Logikbausteine verwendet.

### Sub-Bausteine: Netzwerk-Komponenten
Da es sich um eine SubApp handelt, werden hier die im Netzwerk instanziierten Bausteine beschrieben:

- **DigitalInput_I1**
    - **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    - **Funktion**: Stellt den ersten digitalen Eingang als Adapter zur Verfügung.
    - **Parameter**:
        - `QI` = `TRUE`
        - `Input` = `Input_I1`

- **DigitalInput_I2**
    - **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    - **Funktion**: Stellt den zweiten digitalen Eingang als Adapter zur Verfügung.
    - **Parameter**:
        - `QI` = `TRUE`
        - `Input` = `Input_I2`

- **DigitalInput_I3**
    - **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    - **Funktion**: Stellt den dritten digitalen Eingang als Adapter zur Verfügung.
    - **Parameter**:
        - `QI` = `TRUE`
        - `Input` = `Input_I3`

- **DigitalOutput_Q1**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    - **Funktion**: Steuert den digitalen Ausgang über eine Adapter-Verbindung.
    - **Parameter**:
        - `QI` = `TRUE`
        - `Output` = `Output_Q1`

- **AND_2_BOOL**
    - **Typ**: `adapter::booleanOperators::AX_AND_2`
    - **Funktion**: Führt eine logische UND-Verknüpfung von zwei Adapter-Eingängen durch.

- **OR_2_BOOL**
    - **Typ**: `adapter::booleanOperators::AX_OR_2`
    - **Funktion**: Führt eine logische ODER-Verknüpfung von zwei Adapter-Eingängen durch.

## Programmablauf und Verbindungen

Der Programmablauf wird durch Adapter-Verbindungen (Adapter Connections) realisiert, welche Daten und Events kapseln. Die Logik ist wie folgt aufgebaut:

1.  **UND-Verknüpfung**:
    - Der Adapter-Anschluss von `DigitalInput_I1` ist mit dem ersten Eingang (`IN1`) des Bausteins `AND_2_BOOL` verbunden.
    - Der Adapter-Anschluss von `DigitalInput_I2` ist mit dem zweiten Eingang (`IN2`) des Bausteins `AND_2_BOOL` verbunden.
    - Dies bildet den Term `(I1 AND I2)`.

2.  **ODER-Verknüpfung**:
    - Das Ergebnis der UND-Verknüpfung (`AND_2_BOOL.OUT`) wird auf den ersten Eingang (`IN1`) des Bausteins `OR_2_BOOL` geführt.
    - Der Adapter-Anschluss von `DigitalInput_I3` ist direkt mit dem zweiten Eingang (`IN2`) des Bausteins `OR_2_BOOL` verbunden.
    - Dies vervollständigt die Logik zu `(Term1 OR I3)`.

3.  **Ausgabe**:
    - Das Endergebnis der ODER-Verknüpfung (`OR_2_BOOL.OUT`) ist mit dem Ausgangsbaustein `DigitalOutput_Q1.OUT` verbunden, um das Signal physikalisch auszugeben.

**Hinweis:** Ein expliziter `F_MOVE`-Baustein ist in diesem Aufbau nicht mehr nötig, da die Datenübertragung und Triggerung durch die Adapter-Logikbausteine (`AX_...`) und die `IXA`/`QXA` I/O-Bausteine implizit gehandhabt wird.

## Zusammenfassung
Die Übung `Uebung_002b3_AX` zeigt effizient, wie komplexe boolesche Logik mittels Adapter-Technologie in 4diac implementiert werden kann. Sie veranschaulicht die Einsparung von "Glue Logic" (wie Event- und Datenkonvertern), indem sie spezialisierte Adapter-Operatoren für AND und OR Verknüpfungen nutzt, um drei Eingänge auf einen Ausgang zu mappen.