Hier ist die Dokumentation für die Übung `Uebung_038_AX` im gewünschten Format.

# Uebung_038_AX: Lauflicht 8 reine Zeitsteuerung

![Uebung_038_AX](Uebung_038_AX.png)

* * * * * * * * * *

## Einleitung

Diese Übung implementiert ein 8-stufiges Lauflicht, das rein zeitgesteuert abläuft. Das Ziel ist es, eine Sequenz von 8 Ausgängen nacheinander zu aktivieren, wobei die Umschaltzeiten zwischen den Schritten variieren. Die Steuerung erfolgt über einen spezialisierten Sequenz-Baustein, der in einer Schleife (Loop) läuft. Zusätzlich wird der aktuelle Status (die Schrittnummer) auf einem Display ausgegeben.

## Verwendete Funktionsbausteine (FBs)

In dieser Anwendung werden verschiedene Bausteine aus der `logiBUS`, `iec61131`, `isobus` und `iec61499` Bibliothek verwendet, um die Ein-/Ausgabe und die Logik zu realisieren.

### Haupt-Bausteine:

*   **DigitalInput_CLK_I1** (`logiBUS::io::DI::logiBUS_IE`): Erfasst den Klick auf Taste I1 (Event: `BUTTON_SINGLE_CLICK`), um das Lauflicht zu starten.
*   **DigitalInput_CLK_I4** (`logiBUS::io::DI::logiBUS_IE`): Erfasst den Klick auf Taste I4 (Event: `BUTTON_SINGLE_CLICK`), um das Lauflicht zurückzusetzen.
*   **DigitalOutput_Q1** bis **DigitalOutput_Q8** (`logiBUS::io::DQ::logiBUS_QXA`): Steuern die physikalischen Ausgänge Q1 bis Q8 an. Diese nutzen Adapter-Verbindungen.
*   **Q_NumericValue** (`isobus::UT::Q::Q_NumericValue`): Zeigt den aktuellen Zustand der Sequenz (Schrittnummer) auf dem Universal Terminal (UT) unter der Objekt-ID `OutputNumber_N1` an.
*   **F_SINT_TO_UINT** (`iec61131::conversion::F_SINT_TO_UINT`): Konvertiert den Statuswert der Sequenz (SINT) in einen vorzeichenlosen Integer (UINT) für die Anzeige.
*   **E_TimeOut** (`iec61499::events::E_TimeOut`): Dient als Zeitgeber-Ressource für den Sequenzbaustein.

### Sub-Bausteine: sequence_T_08_loop_AX

Dieser Baustein ist das Herzstück der Steuerung. Er kapselt die Logik für eine zeitgesteuerte Sequenz mit 8 Schritten, die sich wiederholt (Loop).

- **Typ**: `logiBUS::utils::sequence::timed::sequence_T_08_loop_AX`
- **Verwendete interne FBs**: 
    - *Hinweis: Da der interne Aufbau dieses Sub-Bausteins nicht im XML enthalten ist, wird hier die Schnittstellen-Konfiguration beschrieben.*
    - **Parameter (Zeiten)**:
        - `DT_S1_S2` = `T#200ms` (Zeit zwischen Schritt 1 und 2)
        - `DT_S2_S3` = `T#100ms`
        - `DT_S3_S4` = `T#200ms`
        - `DT_S4_S5` = `T#100ms`
        - `DT_S5_S6` = `T#200ms`
        - `DT_S6_S7` = `T#100ms`
        - `DT_S7_S8` = `T#200ms`
        - `DT_S8_S1` = `T#100ms` (Zeit zwischen Schritt 8 und Wiederanfang bei 1)
    - **Adapter-Ausgänge**:
        - `DO_S1` bis `DO_S8`: Adapter-Schnittstellen, die direkt mit den `DigitalOutput`-Bausteinen verbunden sind.
- **Funktionsweise**:
    Der Baustein schaltet nacheinander durch 8 Zustände (S1 bis S8). Jeder Zustand aktiviert den zugehörigen Adapter-Ausgang. Nach Ablauf der definierten Zeit (`DT_xx_xx`) wechselt der Baustein automatisch in den nächsten Zustand. Nach S8 springt die Sequenz zurück zu S1.

## Programmablauf und Verbindungen

1.  **Starten der Sequenz**:
    Wird der Taster **I1** gedrückt (`BUTTON_SINGLE_CLICK`), sendet der Baustein `DigitalInput_CLK_I1` ein Event an den Eingang `START_S1` des `loop`-Bausteins. Dies initiiert das Lauflicht beginnend bei Schritt 1.

2.  **Sequenzablauf**:
    Der Baustein `loop` durchläuft zyklisch die Schritte 1 bis 8.
    *   Die Verweildauer in den ungeraden Schritten (1, 3, 5, 7) beträgt **200ms**.
    *   Die Verweildauer in den geraden Schritten (2, 4, 6, 8) beträgt **100ms**.
    *   Die Zeitsteuerung wird technisch durch die Verbindung zum `E_TimeOut`-Baustein realisiert.

3.  **Ansteuerung der Ausgänge**:
    Die Ausgänge **Q1 bis Q8** werden über Adapter-Verbindungen (`Connection`) direkt vom `loop`-Baustein angesteuert. Wenn der Loop-Baustein in Zustand 1 ist, ist `DO_S1` aktiv und schaltet `DigitalOutput_Q1`. Dies setzt sich bis Q8 fort.

4.  **Visualisierung**:
    Der `loop`-Baustein gibt über `STATE_NR` die aktuelle Schrittnummer aus.
    *   Dieser Wert wird an `F_SINT_TO_UINT` gesendet, um das Datenformat anzupassen.
    *   Das Ergebnis wird an `Q_NumericValue` übergeben, welches die Nummer auf dem Display anzeigt (`OutputNumber_N1`).

5.  **Reset**:
    Wird der Taster **I4** gedrückt, wird das Event an den `RESET`-Eingang des `loop`-Bausteins gesendet, wodurch die Sequenz gestoppt oder zurückgesetzt wird.

## Zusammenfassung

Die Übung `Uebung_038_AX` demonstriert die Erstellung eines komplexen 8-Kanal-Lauflichts unter Verwendung eines vorgefertigten Sequenz-Bausteins (`sequence_T_08_loop_AX`). Der Fokus liegt auf der Parametrierung von Zeitintervallen für Zustandsübergänge und der Nutzung von Adapter-Technologie zur vereinfachten Verbindung von Logik und Peripherie (Ausgänge). Zusätzlich wird der interne Zustand der Logik zur Laufzeit visualisiert.