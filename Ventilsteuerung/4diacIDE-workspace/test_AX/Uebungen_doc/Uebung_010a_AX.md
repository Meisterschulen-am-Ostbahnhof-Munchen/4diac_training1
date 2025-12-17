Hier ist die Dokumentation für die Übung `Uebung_010a_AX` basierend auf dem bereitgestellten XML-Inhalt.

# Uebung_010a_AX

![Uebung_010a_AX](Uebung_010a_AX.png)

* * * * * * * * * *

## Einleitung
Die Übung **Uebung_010a_AX** demonstriert eine direkte Verknüpfung von Softkeys (Bildschirmtasten eines ISOBUS-Terminals) mit digitalen Ausgängen. Das Ziel dieser Sub-Applikation ist es, den Zustand der Softkeys F1 und F2 direkt auf die Ausgänge Q1 und Q2 zu übertragen.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden spezifische Bausteine für die Interaktion mit dem ISOBUS Universal Terminal (UT) und dem lokalen IO-System (logiBUS) verwendet.

### Sub-Bausteine: SoftKey_F1
- **Typ**: `isobus::UT::io::Softkey::Softkey_IXA`
- **Verwendete interne FBs**:
    - **Bausteinname**: SoftKey_F1
        - Parameter: `QI` = `TRUE`
        - Parameter: `u16ObjId` = `SoftKey_F1` (Referenz auf das Softkey-Objekt im UT-Pool)
        - Ereignisausgang/-eingang: N/A (Adapter-basiert)
        - Datenausgang/-eingang: `IN` (Adapter-Verbindung)
- **Funktionsweise**: Dieser Baustein stellt die Schnittstelle zum Softkey F1 auf dem Terminal dar. Er fungiert als Eingangsadapter.

### Sub-Bausteine: SoftKey_F2
- **Typ**: `isobus::UT::io::Softkey::Softkey_IXA`
- **Verwendete interne FBs**:
    - **Bausteinname**: SoftKey_F2
        - Parameter: `QI` = `TRUE`
        - Parameter: `u16ObjId` = `SoftKey_F2` (Referenz auf das Softkey-Objekt im UT-Pool)
        - Ereignisausgang/-eingang: N/A (Adapter-basiert)
        - Datenausgang/-eingang: `IN` (Adapter-Verbindung)
- **Funktionsweise**: Dieser Baustein stellt die Schnittstelle zum Softkey F2 auf dem Terminal dar.

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalOutput_Q1
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q1` (Referenz auf den physikalischen Ausgang Q1)
        - Ereignisausgang/-eingang: N/A (Adapter-basiert)
        - Datenausgang/-eingang: `OUT` (Adapter-Verbindung)
- **Funktionsweise**: Dieser Baustein steuert den physikalischen digitalen Ausgang Q1. Er fungiert als Ausgangsadapter.

### Sub-Bausteine: DigitalOutput_Q2
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalOutput_Q2
        - Parameter: `QI` = `TRUE`
        - Parameter: `Output` = `Output_Q2` (Referenz auf den physikalischen Ausgang Q2)
        - Ereignisausgang/-eingang: N/A (Adapter-basiert)
        - Datenausgang/-eingang: `OUT` (Adapter-Verbindung)
- **Funktionsweise**: Dieser Baustein steuert den physikalischen digitalen Ausgang Q2.

## Programmablauf und Verbindungen

Der Programmablauf in dieser Übung ist rein ereignisgesteuert durch Adapter-Verbindungen realisiert. Es findet keine logische Verarbeitung (wie AND/OR Verknüpfungen) zwischen den Eingängen und Ausgängen statt.

*   **Verbindung 1**: Der Adapter-Anschluss `IN` von **SoftKey_F1** ist direkt mit dem Adapter-Anschluss `OUT` von **DigitalOutput_Q1** verbunden.
*   **Verbindung 2**: Der Adapter-Anschluss `IN` von **SoftKey_F2** ist direkt mit dem Adapter-Anschluss `OUT` von **DigitalOutput_Q2** verbunden.

Dies bedeutet, dass eine Betätigung der Taste F1 auf dem Terminal unmittelbar den Ausgang Q1 aktiviert. Analog dazu steuert Taste F2 den Ausgang Q2. Die Verwendung von Adaptern (erkennbar an den Endungen `_IXA` und `_QXA`) vereinfacht das Netzwerk, da Daten- und Ereignisflüsse gebündelt übertragen werden.

## Zusammenfassung
Die `Uebung_010a_AX` ist eine grundlegende Einführung in die Verwendung von Adapter-Verbindungen innerhalb der 4diac-IDE. Sie zeigt, wie Eingabeelemente (Softkeys) ohne komplexe Logik direkt auf Hardware-Ausgänge gemappt werden können. Dies dient oft als Test, um die Kommunikation zwischen Steuerung und Terminal sowie die Funktion der Ausgänge sicherzustellen.