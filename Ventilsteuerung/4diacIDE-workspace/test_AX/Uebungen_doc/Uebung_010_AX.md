Hier ist die Dokumentation für die Übung `Uebung_010_AX` basierend auf den bereitgestellten Daten.

# Uebung_010_AX

![Uebung_010_AX](Uebung_010_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert eine grundlegende Funktion der IEC 61499 Programmierung innerhalb der 4diac IDE: Die direkte Verbindung eines Eingabeelements (SoftKey auf einem Universal Terminal) mit einem physikalischen Ausgabeelement (Digitaler Ausgang). Das Ziel ist es, den digitalen Ausgang `Output_Q1` zu aktivieren, sobald der SoftKey `F1` betätigt wird.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden zwei spezifische Schnittstellen-Bausteine verwendet, um die Kommunikation zwischen der Steuerungslogik und der Hardware bzw. dem ISOBUS-System herzustellen.

### Sub-Bausteine: Uebung_010_AX
Diese Übung besteht aus einem Netzwerk, das folgende interne Bausteine instanziiert:

- **SoftKey_F1**
    - **Typ**: `isobus::UT::io::Softkey::Softkey_IXA`
    - **Beschreibung**: Dieser Baustein repräsentiert einen SoftKey-Eingang von einem ISOBUS Universal Terminal (UT). Er dient als Adapter-Quelle (`IXA` - Input X Adapter).
    - **Parameter**:
        - `QI` = `TRUE` (Baustein ist aktiviert)
        - `u16ObjId` = `SoftKey_F1` (Referenziert die spezifische Objekt-ID des SoftKeys im Objekt-Pool)
    - **Adapter**:
        - `IN`: Ausgangsadapter, der den Zustand des SoftKeys bereitstellt.

- **DigitalOutput_Q1**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    - **Beschreibung**: Dieser Baustein repräsentiert einen digitalen Ausgang auf der Hardware (logiBUS). Er dient als Adapter-Senke (`QXA` - Output X Adapter).
    - **Parameter**:
        - `QI` = `TRUE` (Baustein ist aktiviert)
        - `Output` = `Output_Q1` (Logische Zuordnung zum physikalischen Ausgang Q1)
        - `PARAMS` -> `Visible` = `false`
    - **Adapter**:
        - `OUT`: Eingangsadapter, der das Steuersignal für den Ausgang empfängt.

## Programmablauf und Verbindungen

Der Programmablauf in dieser Übung ist linear und ereignisgesteuert durch die Adapter-Technologie.

1.  **Startbedingungen**: Beide Bausteine (`SoftKey_F1` und `DigitalOutput_Q1`) werden durch den Parameter `QI = TRUE` initialisiert und sind betriebsbereit.
2.  **Verbindung**: Es existiert genau eine Verbindung im Netzwerk:
    -   **Quelle**: `SoftKey_F1.IN`
    -   **Ziel**: `DigitalOutput_Q1.OUT`
    -   **Art der Verbindung**: Dies ist eine **Adapterverbindung**. Adapter bündeln Daten und Ereignisse. In diesem Fall wird der Status des SoftKeys direkt an den digitalen Ausgang weitergeleitet.
3.  **Logik**:
    -   Wenn der Benutzer die Taste **F1** (SoftKey) auf dem Terminal drückt, ändert sich der Status im Adapter `SoftKey_F1`.
    -   Durch die Verbindung wird dieser Status unmittelbar an `DigitalOutput_Q1` übertragen.
    -   Der physikalische Ausgang **Q1** schaltet entsprechend (wird `HIGH`, solange die Taste gedrückt ist, bzw. folgt der Logik des SoftKeys).

**Lernziele:**
-   Verständnis von Adapterverbindungen in IEC 61499.
-   Mapping von ISOBUS-Objekten (SoftKeys) auf Hardware-IOs.

## Zusammenfassung
Die `Uebung_010_AX` ist eine Einstiegsübung, die zeigt, wie ohne komplexe logische Verknüpfungen (wie AND/OR Bausteine) eine direkte Durchleitung von Signalen mittels Adaptertechnologie realisiert werden kann. Der SoftKey F1 steuert dabei direkt den Digitalen Ausgang Q1.