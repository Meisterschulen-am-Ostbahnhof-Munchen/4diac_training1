# Uebung_001_AX_b: DigitalInput_I1 auf DigitalOutput_Q1, mit Plug and Socket

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung eines digitalen Eingangs mit einem digitalen Ausgang unter Verwendung von Plug-and-Socket-Adaptern. Das System liest den Zustand eines digitalen Eingangs (I1) und gibt diesen direkt auf einem digitalen Ausgang (Q1) aus.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: AX_X_TO_BOOL
- **Typ**: AX_X_TO_BOOL
- **Verwendete interne FBs**: Keine
- **Funktionsweise**: Wandelt ein AX-Signal in einen BOOL-Wert um

### Sub-Bausteine: AX_BOOL_TO_X
- **Typ**: AX_BOOL_TO_X
- **Verwendete interne FBs**: Keine
- **Funktionsweise**: Wandelt einen BOOL-Wert zurück in ein AX-Signal um

## Programmablauf und Verbindungen

**Verwendete Haupt-Funktionsbausteine:**
- DigitalInput_I1 (logiBUS_IXA)
- DigitalOutput_Q1 (logiBUS_QXA)

**Parameterkonfiguration:**
- DigitalInput_I1: QI=TRUE, Input=logiBUS_DI::Input_I1
- DigitalOutput_Q1: QI=TRUE, Output=logiBUS_DO::Output_Q1

**Verbindungen:**
- Eventverbindung: AX_X_TO_BOOL.CNF → AX_BOOL_TO_X.REQ
- Datenverbindung: AX_X_TO_BOOL.IN → AX_BOOL_TO_X.OUT
- Adapterverbindungen:
  - DigitalInput_I1.IN → AX_X_TO_BOOL.AX_IN
  - AX_BOOL_TO_X.AX_OUT → DigitalOutput_Q1.OUT

**Lernziele:**
- Grundlegende Verwendung von Plug-and-Socket-Adaptern
- Signalwandlung zwischen verschiedenen Datentypen
- Aufbau einfacher E/A-Verknüpfungen

**Schwierigkeitsgrad:** Einfach
**Benötigte Vorkenntnisse:** Grundverständnis von 4diac-IDE und Funktionsbausteinen

**Starten der Übung:** Das Programm wird automatisch aktiviert, da beide Hauptbausteine den Parameter QI=TRUE haben.

## Zusammenfassung
Diese Übung vermittelt die grundlegende Funktionsweise von Signalwandlern und Adapterverbindungen in 4diac. Sie zeigt, wie digitale Eingangssignale verarbeitet und auf Ausgänge weitergeleitet werden können, wobei die Signalwandlung zwischen verschiedenen Datentypen im Fokus steht.