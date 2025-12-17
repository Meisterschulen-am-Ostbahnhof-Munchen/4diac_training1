Hier ist die Dokumentation für die Übung `Uebung_160` basierend auf den bereitgestellten Daten.

# Uebung_160 - Motor Links/Rechtslauf

![Uebung_160 Bild](Uebung_160.png)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine grundlegende Steuerung für einen Motor mit Links- und Rechtslauf. Das Ziel ist es, Eingangssignale direkt auf entsprechende Ausgänge zu mappen und zusätzlich einen Sammelausgang zu schalten, sobald eine der beiden Richtungen aktiv ist. Diese Logik wird typischerweise verwendet, um Schütze für die Drehrichtung anzusteuern und gleichzeitig eine Anzeige (z. B. "Motor läuft") zu betreiben.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden Standard-Ein-/Ausgabebausteine des `logiBUS` sowie logische Verknüpfungsbausteine verwendet.

### Enthaltene Bausteine im Netzwerk

Hier sind die Instanzen der Funktionsbausteine aufgeführt, die in dieser SubApplikation verschaltet sind:

- **DigitalInput_I1**
    - **Typ**: `logiBUS::io::DI::logiBUS_IX`
    - **Parameter**: 
        - `QI` = `TRUE`
        - `Input` = `Input_I1`
    - **Funktion**: Liest das erste digitale Eingangssignal (z. B. Taster "Links").

- **DigitalInput_I2**
    - **Typ**: `logiBUS::io::DI::logiBUS_IX`
    - **Parameter**: 
        - `QI` = `TRUE`
        - `Input` = `Input_I2`
    - **Funktion**: Liest das zweite digitale Eingangssignal (z. B. Taster "Rechts").

- **DigitalOutput_Q5**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QX`
    - **Parameter**: 
        - `QI` = `TRUE`
        - `Output` = `Output_Q5`
    - **Funktion**: Steuert den ersten Ausgang an (z. B. Schütz für Linkslauf).

- **DigitalOutput_Q6**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QX`
    - **Parameter**: 
        - `QI` = `TRUE`
        - `Output` = `Output_Q6`
    - **Funktion**: Steuert den zweiten Ausgang an (z. B. Schütz für Rechtslauf).

- **DigitalOutput_Q56**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QX`
    - **Parameter**: 
        - `QI` = `TRUE`
        - `Output` = `Output_Q56`
    - **Funktion**: Steuert einen Sammelausgang an (z. B. Signallampe "Betrieb").

- **OR_2_BOOL**
    - **Typ**: `iec61131::bitwiseOperators::OR_2_BOOL`
    - **Funktion**: Logische ODER-Verknüpfung von zwei booleschen Signalen.

## Programmablauf und Verbindungen

Der Ablauf der Steuerung ist wie folgt aufgebaut:

1.  **Direkte Ansteuerung der Ausgänge:**
    *   Das Signal von **DigitalInput_I1** (`Input_I1`) wird direkt an **DigitalOutput_Q5** (`Output_Q5`) weitergeleitet. Wenn Eingang I1 aktiv ist, wird Ausgang Q5 gesetzt.
    *   Das Signal von **DigitalInput_I2** (`Input_I2`) wird direkt an **DigitalOutput_Q6** (`Output_Q6`) weitergeleitet. Wenn Eingang I2 aktiv ist, wird Ausgang Q6 gesetzt.

2.  **Sammelmeldung (ODER-Verknüpfung):**
    *   Die Datenausgänge (`IN`) von sowohl **DigitalInput_I1** als auch **DigitalInput_I2** sind mit den Eingängen des Bausteins **OR_2_BOOL** verbunden.
    *   Der Baustein **OR_2_BOOL** prüft, ob *mindestens einer* der beiden Eingänge `TRUE` ist.
    *   Das Ergebnis dieser Prüfung (`OUT`) wird an den Dateneingang von **DigitalOutput_Q56** (`Output_Q56`) gesendet. Dies bedeutet, dass Ausgang Q56 aktiv wird, sobald entweder Links- oder Rechtslauf (oder beide) angefordert werden.

3.  **Event-Kette (Ereignissteuerung):**
    *   Sobald sich ein Wert am Eingang ändert (`IND` Event von I1 oder I2), wird dieses Ereignis genutzt, um die entsprechenden Ausgänge (`REQ` Event an Q5, Q6) und die Logik-Berechnung (`REQ` am OR-Baustein) zu triggern.

**Lernziele:**
*   Verständnis der direkten Signalweiterleitung (Mapping).
*   Einsatz von logischen Grundfunktionen (ODER).
*   Verwendung von Hardware-Abstraktions-FBs (logiBUS Inputs/Outputs).

## Zusammenfassung

Die Übung `Uebung_160` realisiert eine einfache Motorsteuerung, bei der zwei Eingänge direkt zwei separate Ausgänge schalten (für Links- bzw. Rechtslauf). Zusätzlich wird über eine ODER-Logik ein dritter Ausgang aktiviert, der als allgemeine Betriebsanzeige dient, solange eines der beiden Eingangssignale anliegt. Dies demonstriert die Kombination von direkter E/A-Zuordnung und logischer Signalverarbeitung innerhalb der 4diac IDE.