Hier ist die Dokumentation für die Übung **Uebung_160_AX**, basierend auf den bereitgestellten XML-Daten.

# Uebung_160_AX

*(Hier Platzhalter für Bild der Übung einfügen)*

* * * * * * * * * *

## Einleitung
Die Übung **Uebung_160_AX** implementiert eine Steuerung für einen **Motor Links/Rechtslauf**. Das Ziel dieser Übung ist es, zwei Eingangssignale (Taster für Links/Rechts) auf entsprechende Ausgänge zu leiten und zusätzlich einen gemeinsamen Ausgang zu schalten, sobald einer der beiden Motoren läuft (Betriebsanzeige).

Eine Besonderheit dieser Übung ist die Verwendung von **Adapter-Verbindungen** (erkennbar am Präfix `AX` und den Typen `..._IXA`/`..._QXA`), welche die Verdrahtung vereinfachen, indem sie Ereignisse und Daten in einer Verbindung bündeln.

## Verwendete Funktionsbausteine (FBs)

In diesem Netzwerk werden spezifische Adapter-Bausteine verwendet, um die Logik zu realisieren.

### Sub-Bausteine: Logik- und IO-Komponenten

Hier werden die im Netzwerk instanziierten Bausteine beschrieben:

*   **Digitale Eingänge (Adapter)**
    *   **Instanznamen**: `DigitalInput_I1`, `DigitalInput_I2`
    *   **Typ**: `logiBUS::io::DI::logiBUS_IXA`
    *   **Parameter**:
        *   `QI` = `TRUE`
        *   `Input` = `Input_I1` bzw. `Input_I2`
    *   **Funktionsweise**: Stellen die Schnittstelle zu den physischen Tastern dar.

*   **Digitale Ausgänge (Adapter)**
    *   **Instanznamen**: `DigitalOutput_Q5`, `DigitalOutput_Q6`, `DigitalOutput_Q56`
    *   **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    *   **Parameter**:
        *   `QI` = `TRUE`
        *   `Output` = `Output_Q5`, `Output_Q6` bzw. `Output_Q56`
    *   **Funktionsweise**: Stellen die Schnittstelle zu den physischen Aktoren (Schütze/Lampen) dar.

*   **Signal-Splitter**
    *   **Instanznamen**: `AX_SPLIT_2_A`, `AX_SPLIT_2_B`
    *   **Typ**: `adapter::events::unidirectional::AX_SPLIT_2`
    *   **Funktionsweise**: Dieser Baustein nimmt eine eingehende Adapter-Verbindung entgegen und teilt sie auf zwei Ausgänge (`OUT1`, `OUT2`) auf. Dies wird benötigt, um ein Signal gleichzeitig an einen Ausgang und an ein Logikgatter zu senden.

*   **Logisches ODER (Adapter)**
    *   **Instanzname**: `AX_OR_2`
    *   **Typ**: `adapter::booleanOperators::AX_OR_2`
    *   **Funktionsweise**: Realisiert eine logische ODER-Verknüpfung für Adapter-Signale. Wenn an `IN1` ODER `IN2` ein aktives Signal anliegt, wird der Ausgang `OUT` aktiviert.

## Programmablauf und Verbindungen

Das Netzwerk steuert die Ausgänge basierend auf den Eingängen wie folgt:

1.  **Motor Links (Pfad A)**:
    *   Der Eingang **DigitalInput_I1** ist mit dem Splitter **AX_SPLIT_2_A** verbunden.
    *   Der erste Ausgang des Splitters (`OUT1`) aktiviert direkt den Ausgang **DigitalOutput_Q5** (z.B. Motorschütz Links).
    *   Der zweite Ausgang des Splitters (`OUT2`) führt zum ersten Eingang des ODER-Gatters **AX_OR_2**.

2.  **Motor Rechts (Pfad B)**:
    *   Der Eingang **DigitalInput_I2** ist mit dem Splitter **AX_SPLIT_2_B** verbunden.
    *   Der zweite Ausgang des Splitters (`OUT2`) aktiviert direkt den Ausgang **DigitalOutput_Q6** (z.B. Motorschütz Rechts).
    *   Der erste Ausgang des Splitters (`OUT1`) führt zum zweiten Eingang des ODER-Gatters **AX_OR_2**.

3.  **Gemeinsame Anzeige (Pfad OR)**:
    *   Das ODER-Gatter **AX_OR_2** empfängt Signale von beiden Splittern.
    *   Der Ausgang des ODER-Gatters ist mit **DigitalOutput_Q56** verbunden.
    *   Dadurch leuchtet Q56, wenn entweder I1 oder I2 betätigt wird.

## Zusammenfassung

Die Übung **Uebung_160_AX** demonstriert effektiv den Umgang mit Adapter-Bausteinen in 4diac. Durch den Einsatz von `AX_SPLIT_2` wird gezeigt, wie ein Signalverlauf verzweigt werden kann, um parallele Aktionen auszulösen (direktes Schalten und Logikverarbeitung). Der Baustein `AX_OR_2` fasst die Zustände zusammen, um eine allgemeine Betriebsmeldung zu generieren. Die Übung eignet sich hervorragend zum Verständnis von Signalfluss und logischen Grundverknüpfungen innerhalb der Adapter-Architektur.