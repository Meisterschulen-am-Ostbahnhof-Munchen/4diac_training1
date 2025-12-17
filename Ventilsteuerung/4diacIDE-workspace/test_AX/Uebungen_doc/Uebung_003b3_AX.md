Hier ist die Dokumentation für die Übung `Uebung_003b3_AX` basierend auf den bereitgestellten Daten.

# Uebung_003b3_AX

![Uebung_003b3_AX](Uebung_003b3_AX.png)

* * * * * * * * * *

## Einleitung

Die Übung **Uebung_003b3_AX** realisiert eine direkte Zuordnung von Tasten einer Funk-Fernbedienung ("Funk") auf digitale Ausgänge eines Anzeigepanels ("DataPanel"). Ziel der Übung ist es, Eingabesignale (Tasten) modular auf Ausgabesignale (LEDs oder Relais) zu routen. Dabei wird ein Sub-Baustein mehrfach instanziiert, um den Code übersichtlich und wiederverwendbar zu gestalten.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung wird hauptsächlich ein spezifischer Sub-App-Typ mehrfach verwendet, um die Verbindung zwischen Eingang und Ausgang herzustellen.

### Sub-Bausteine: Uebung_003b3_sub_AX

Dieser Baustein wird insgesamt 15 Mal im Netzwerk instanziiert (F1 bis F15). Er dient als gekapselte Logikeinheit, um einen spezifischen digitalen Eingang auf einen digitalen Ausgang zu mappen.

- **Typ**: SubApp (`Uebungen::Uebung_003b3_sub_AX`)
- **Schnittstelle (Parameter)**:
    - **Input**: Der Name des physikalischen Eingangs (hier: Tasten der Funk-Einheit).
    - **Output**: Der Name des physikalischen Ausgangs (hier: Ausgänge des DataPanels).
    - **u8SAMember**: Ein Index-Parameter (hier konstant `MI_00`), der wahrscheinlich die Modulzugehörigkeit definiert.
- **Funktionsweise**:
    Der Baustein nimmt ein digitales Signal am `Input` entgegen und leitet dieses, konfiguriert durch `u8SAMember`, an den definierten `Output` weiter. Da der interne Aufbau dieses Sub-Bausteins nicht im Detail vorliegt, wird von einer direkten Durchleitung (Mapping) ausgegangen.

## Programmablauf und Verbindungen

Das Hauptnetzwerk besteht aus einer parallelen Anordnung von 15 Instanzen des oben beschriebenen Sub-Bausteins. Es findet keine komplexe logische Verknüpfung zwischen den Tasten statt; stattdessen handelt es sich um eine reine 1-zu-1-Verdrahtung in Software.

**Die Zuordnungen im Detail:**

1.  **Steuertasten:**
    -   **F1**: Die Taste `DigitalInput_Key_STOP` schaltet `DigitalOutput_1A`.
    -   **F2**: Die Taste `DigitalInput_Key_START` schaltet `DigitalOutput_1B`.

2.  **Nummerierte Tasten (01 - 13):**
    -   **F3**: Taste `Key_01` -> `DigitalOutput_2A`
    -   **F4**: Taste `Key_02` -> `DigitalOutput_2B`
    -   **F5**: Taste `Key_03` -> `DigitalOutput_3A`
    -   **F6**: Taste `Key_04` -> `DigitalOutput_3B`
    -   **F7**: Taste `Key_05` -> `DigitalOutput_4A`
    -   **F8**: Taste `Key_06` -> `DigitalOutput_4B`
    -   **F9**: Taste `Key_07` -> `DigitalOutput_5A`
    -   **F10**: Taste `Key_08` -> `DigitalOutput_5B`
    -   **F11**: Taste `Key_09` -> `DigitalOutput_6A`
    -   **F12**: Taste `Key_10` -> `DigitalOutput_6B`
    -   **F13**: Taste `Key_11` -> `DigitalOutput_7A`
    -   **F14**: Taste `Key_12` -> `DigitalOutput_7B`
    -   **F15**: Taste `Key_13` -> `DigitalOutput_8A`

Alle Instanzen verwenden `MI_00` als `u8SAMember` Parameter.

## Zusammenfassung

Die Übung `Uebung_003b3_AX` zeigt exemplarisch, wie mittels Sub-Applications eine strukturierte Hardware-Abstraktion in 4diac erfolgen kann. Anstatt Eingänge und Ausgänge "wild" zu verdrahten, werden standardisierte Blöcke (`Uebung_003b3_sub_AX`) genutzt, um 15 verschiedene Tastenfunktionen auf korrespondierende Ausgänge zu legen. Dies erleichtert die Wartung und Lesbarkeit des Programms erheblich.