Hier ist die Dokumentation basierend auf der bereitgestellten XML-Datei `Uebung_003b_sub`.

# Uebung_003b_sub

![Uebung_003b_sub](pfad/zum/bild_falls_vorhanden.png)

* * * * * * * * * *

## Einleitung

Die Komponente **Uebung_003b_sub** ist ein Sub-Application-Typ (SubApp), der eine direkte Verbindung zwischen einem digitalen Eingang und einem digitalen Ausgang herstellt. Der Zweck dieses Bausteins ist es, ein Eingangssignal (IX) generisch auf ein Ausgangssignal (QX) durchzuschalten (Mapping). Dies dient der Kapselung von Hardware-IO-Zugriffen in einem wiederverwendbaren Modul.

## Verwendete Funktionsbausteine (FBs)

Diese Übung ist als SubApp definiert, die intern spezifische IO-Bausteine des `logiBUS`-Systems verwendet.

### Sub-Bausteine: Uebung_003b_sub

*   **Typ**: SubAppType
*   **Verwendete interne FBs**:

    *   **IX**: `logiBUS::io::DI::logiBUS_IX`
        *   **Parameter**: `QI` = TRUE
        *   **Dateneingang**: `Input` (kommt von der SubApp-Schnittstelle zur Identifikation des Eingangs)
        *   **Datenausgang**: `IN` (Der gelesene Wert)
        *   **Ereignisausgang**: `IND` (Indication - Signalisiert neuen Wert)

    *   **QX**: `logiBUS::io::DQ::logiBUS_QX`
        *   **Parameter**: `QI` = TRUE
        *   **Dateneingang**: `Output` (kommt von der SubApp-Schnittstelle zur Identifikation des Ausgangs)
        *   **Dateneingang**: `OUT` (Der zu schreibende Wert, verbunden mit `IX.IN`)
        *   **Ereigniseingang**: `REQ` (Request - Löst den Schreibvorgang aus)

*   **Funktionsweise**:
    Der Sub-Baustein kapselt die Logik für das direkte Durchreichen eines Signals. Über die Schnittstellenvariablen `Input` und `Output` wird definiert, welche physischen Hardware-Adressen (z.B. I1 bis I8 bzw. Q1 bis Q8) angesprochen werden sollen.

## Programmablauf und Verbindungen

Der interne Ablauf der SubApp gestaltet sich wie folgt:

1.  **Initialisierung**: Die Bausteine `IX` und `QX` sind standardmäßig aktiviert (`QI` = TRUE).
2.  **Signalverarbeitung**:
    *   Der Baustein **IX** liest den Zustand des physikalischen Eingangs, der durch die Variable `Input` definiert ist.
    *   Sobald ein Wert gelesen wurde, sendet **IX** ein Event über den Ausgang `IND`.
    *   Dieses Event ist mit dem Eingang `REQ` des Bausteins **QX** verbunden.
3.  **Datenfluss**:
    *   Der gelesene Zustand (`IX.IN`) wird direkt an den Ausgangswert (`QX.OUT`) übertragen.
    *   Dies bewirkt, dass der physikalische Ausgang (definiert durch die Variable `Output`) den gleichen Zustand annimmt wie der Eingang.

**Zusammenfassung der Verbindungen:**
*   **Event**: `IX.IND` $\rightarrow$ `QX.REQ`
*   **Daten**: `IX.IN` $\rightarrow$ `QX.OUT`
*   **Konfiguration**: Die externen Parameter `Input` und `Output` der SubApp werden an die internen Konfigurationseingänge von `IX` und `QX` weitergeleitet.

## Zusammenfassung

Die `Uebung_003b_sub` ist ein kompakter, wiederverwendbarer Baustein für IO-Operationen. Sie implementiert eine "Hard-Wire"-Logik in Software, bei der ein Eingangssignal ohne zusätzliche logische Verknüpfung 1:1 an einen Ausgang weitergegeben wird. Dies eignet sich hervorragend für Tests der Hardwareverdrahtung oder als Basismodul für komplexere Steuerungsaufgaben, bei denen IO-Zuordnungen flexibel bleiben sollen.