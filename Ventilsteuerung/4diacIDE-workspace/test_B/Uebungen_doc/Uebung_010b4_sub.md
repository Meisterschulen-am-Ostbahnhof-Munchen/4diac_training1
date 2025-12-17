Hier ist die Dokumentation für die Sub-Applikation `Uebung_010b4_sub` basierend auf den bereitgestellten Daten.

# Uebung_010b4_sub

![Uebung_010b4_sub Übersicht](img/Uebung_010b4_sub.png)

* * * * * * * * * *

## Einleitung
Die Sub-Applikation `Uebung_010b4_sub` realisiert eine generische Verknüpfung zwischen einem ISOBUS-Softkey-Eingang (IX) und einem digitalen Ausgang (QX). Der Zweck dieses Bausteins ist es, den Status eines Softkeys auf dem Universal Terminal (UT) direkt auf einen physikalischen Ausgang des Steuergeräts zu mappen. Durch die Parametrierbarkeit der Objekt-ID und des Ausgangs-Pins ist dieser Baustein wiederverwendbar.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung wird ein Sub-Applikationstyp definiert, der intern spezifische Treiber-Bausteine für ISOBUS und logiBUS verwendet.

### Sub-Bausteine: Uebung_010b4_sub
Dieser Baustein kapselt die Logik für die Signalweiterleitung.

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: `isobus::UT::io::Softkey::Softkey_IX`
        - **Parameter**: `QI` = `TRUE`
        - **Dateneingang**: `u16ObjId` (Verbunden mit dem SubApp-Eingang `u16ObjId`)
        - **Ereignisausgang**: `IND` (Indication - Statusänderung des Softkeys)
        - **Datenausgang**: `IN` (Aktueller Wert des Softkeys)
    - **QX**: `logiBUS::io::DQ::logiBUS_QX`
        - **Parameter**: `QI` = `TRUE`
        - **Parameter**: `PARAMS` = "" (Unsichtbar/Leer)
        - **Dateneingang**: `Output` (Verbunden mit dem SubApp-Eingang `Output`)
        - **Ereigniseingang**: `REQ` (Request - Schreibanforderung)
        - **Dateneingang**: `OUT` (Wert, der auf den Ausgang geschrieben werden soll)

- **Funktionsweise**:
    Der Sub-Baustein nimmt eine Objekt-ID (`u16ObjId`) und eine Ausgangs-Identifikation (`Output`) entgegen. Der interne Baustein `IX` überwacht den Softkey mit der entsprechenden ID. Sobald sich der Status des Softkeys ändert (Event `IND`), wird dieser Status (Data `IN`) an den Baustein `QX` weitergeleitet. Der `QX`-Baustein schreibt diesen Wert (Data `OUT`) auf den physikalischen Ausgang, der über den Eingang `Output` definiert wurde.

## Programmablauf und Verbindungen

Der Ablauf innerhalb der Sub-Applikation ist ereignisgesteuert:

1.  **Initialisierung**: Die Bausteine `IX` und `QX` sind dauerhaft aktiviert (`QI` = TRUE).
2.  **Eingangssignal**: Wenn das ISOBUS-System eine Änderung am Softkey (definiert durch `u16ObjId`) feststellt, feuert der Baustein `IX` das Ereignis `IND`.
3.  **Verarbeitung & Weiterleitung**:
    - Das Ereignis `IND` von `IX` ist direkt mit dem Ereignis `REQ` von `QX` verbunden. Dies löst den Schreibvorgang auf den Ausgang aus.
    - Der Datenwert `IN` (Zustand des Softkeys) von `IX` wird an den Eingang `OUT` von `QX` übergeben.
4.  **Ausgangssignal**: Der Baustein `QX` setzt den physikalischen Ausgang (definiert durch `Output`) auf den empfangenen Wert.

**Zusätzliche Informationen zur Übung:**
*   **Lernziele**: Verständnis von Sub-Applikationen, Kapselung von Hardware- und Kommunikationslogik, Parametrierung von generischen Bausteinen.
*   **Vorkenntnisse**: Grundlegendes Verständnis von IEC 61499, ISOBUS-Konzepten (Softkeys) und logiBUS IO-Handling.
*   **Schwierigkeitsgrad**: Mittel (durch die Verwendung spezifischer Hardware-Bibliotheken).

## Zusammenfassung
Die `Uebung_010b4_sub` stellt einen kompakten, wiederverwendbaren Baustein dar, um ohne komplexe externe Logik eine direkte Verbindung („Durchschleifen“) von einem ISOBUS-Bedienelement auf einen Hardware-Ausgang zu realisieren. Durch die Exponierung der Konfigurationsvariablen (`u16ObjId`, `Output`) an der Schnittstelle der Sub-Applikation kann dieser Baustein mehrfach instanziiert werden, um verschiedene Tasten auf verschiedene Ausgänge zu legen.