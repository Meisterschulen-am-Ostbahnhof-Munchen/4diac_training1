Hier ist die Dokumentation für die Übung `Uebung_003a0`, basierend auf den bereitgestellten XML-Daten.

# Uebung_003a0

*(Hier Bild der Übung einfügen, falls vorhanden)*

* * * * * * * * * *

## Einleitung

Die Übung **Uebung_003a0** demonstriert die logische Verknüpfung von digitalen Eingängen und Ausgängen unter Verwendung von sogenannten "Untyped SubApps" (typisierten Unteranwendungen). Das Ziel dieser Übung ist es, die Signale der digitalen Eingänge `Input_I1` und `Input_I2` direkt an die digitalen Ausgänge `Output_Q1` und `Output_Q2` weiterzuleiten. Dabei wird der Code strukturiert, indem die Logik für verschiedene I/O-Paare in separate Sub-Applikationen gekapselt wird.

## Verwendete Funktionsbausteine (FBs)

Diese Anwendung besteht aus zwei internen Sub-Bausteinen (SubApps), die jeweils einen Eingang auf einen Ausgang abbilden.

### Sub-Bausteine: SubApp
Dieser Sub-Baustein ist für die Verarbeitung des zweiten Eingangs-Ausgangs-Paares zuständig.

- **Typ**: SubApp (Untyped / Intern)
- **Verwendete interne FBs**:
    - **DigitalInput_I2**: `logiBUS::io::DI::logiBUS_IX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Input` = `Input_I2`
        - Ereignisausgang: `IND`
        - Datenausgang: `IN`
    - **DigitalOutput_Q2**: `logiBUS::io::DQ::logiBUS_QX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q2`
        - Ereigniseingang: `REQ`
        - Dateneingang: `OUT`
- **Funktionsweise**: 
    Der Baustein liest den Hardware-Eingang `Input_I2`. Sobald ein Signalwechsel erkannt wird (Event `IND`), wird dieses Ereignis an den Ausgangsbaustein weitergeleitet (`REQ`), um den Hardware-Ausgang `Output_Q2` entsprechend dem Datenwert (`IN` auf `OUT`) zu schalten.

### Sub-Bausteine: SubApp_1
Dieser Sub-Baustein ist für die Verarbeitung des ersten Eingangs-Ausgangs-Paares zuständig.

- **Typ**: SubApp (Untyped / Intern)
- **Verwendete interne FBs**:
    - **DigitalOutput_Q1**: `logiBUS::io::DQ::logiBUS_QX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q1`
        - Ereigniseingang: `REQ`
        - Dateneingang: `OUT`
    - **DigitalInput_I1**: `logiBUS::io::DI::logiBUS_IX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `Input` = `Input_I1`
        - Ereignisausgang: `IND`
        - Datenausgang: `IN`
- **Funktionsweise**:
    Analog zur ersten SubApp wird hier der Hardware-Eingang `Input_I1` eingelesen. Das Signal und der Datenwert werden direkt an den Hardware-Ausgang `Output_Q1` durchgereicht.

## Programmablauf und Verbindungen

Die Logik der Anwendung ist rein ereignisbasiert und in zwei unabhängige Bereiche aufgeteilt:

1.  **Verarbeitungskette 1 (in SubApp_1):**
    *   Der Baustein `DigitalInput_I1` überwacht den Eingang `Input_I1`.
    *   Bei einer Änderung wird das Ereignis `IND` ausgelöst.
    *   Dieses Ereignis ist mit dem Eingang `REQ` des Bausteins `DigitalOutput_Q1` verbunden.
    *   Gleichzeitig wird der logische Zustand (`TRUE` oder `FALSE`) vom Ausgang `IN` auf den Eingang `OUT` des Ausgangsbausteins übertragen.

2.  **Verarbeitungskette 2 (in SubApp):**
    *   Der Baustein `DigitalInput_I2` überwacht den Eingang `Input_I2`.
    *   Das Ereignis `IND` triggert den Eingang `REQ` von `DigitalOutput_Q2`.
    *   Der Datenwert `IN` wird auf `OUT` von `DigitalOutput_Q2` geschrieben.

**Lernziele:**
*   Verständnis für die Kapselung von Logik in SubApps zur besseren Strukturierung.
*   Umgang mit logiBUS I/O-Bausteinen (IX und QX).
*   Realisierung einfacher Durchgangsschaltungen (Pass-Through).

## Zusammenfassung

Die Übung `Uebung_003a0` zeigt eine grundlegende Hardware-Abstraktion und Signalweiterleitung. Durch die Aufteilung in zwei `SubApp`-Container wird der Code übersichtlich gehalten. Es handelt sich um eine direkte Umsetzung der Hardware-Eingänge I1 und I2 auf die Hardware-Ausgänge Q1 und Q2 ohne zusätzliche logische Verknüpfungen (wie UND/ODER), rein basierend auf der Ereignis- und Datenweitergabe.