Hier ist die Dokumentation für die Übung `Uebung_004a2_AX` basierend auf den bereitgestellten Daten.

# Uebung_004a2_AX

![](Uebung_004a2_AX.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Implementierung eines Toggle-Flip-Flops (T-Flip-Flop), das von zwei unabhängigen Tastern gesteuert wird. Dabei wird das spezifische Eingabeereignis "BUTTON_SINGLE_CLICK" (einfacher Tastendruck) verwendet. Um die Signale beider Taster auf einen einzigen logischen Baustein zu leiten, kommt ein Event-Merge-Baustein zum Einsatz. Die Ansteuerung des Ausgangs erfolgt über eine Adapterverbindung.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden verschiedene Bausteine aus der `logiBUS`-Bibliothek sowie Standard-IEC61499-Bausteine und Adapter verwendet.

### Hauptnetzwerk-Komponenten

Im Hauptnetzwerk der Sub-Application `Uebung_004a2_AX` werden folgende Instanzen definiert:

- **DigitalInput_CLK_I1**
    - **Typ**: `logiBUS::io::DI::logiBUS_IE`
    - **Beschreibung**: Dieser Baustein repräsentiert den ersten digitalen Eingang. Er ist so konfiguriert, dass er auf einen einfachen Klick reagiert.
    - **Parameter**:
        - `Input` = `Input_I1` (Hardware-Mapping auf Eingang I1)
        - `InputEvent` = `BUTTON_SINGLE_CLICK` (Löst ein Event bei einfachem Tastendruck aus)

- **DigitalInput_CLK_I2**
    - **Typ**: `logiBUS::io::DI::logiBUS_IE`
    - **Beschreibung**: Repräsentiert den zweiten digitalen Eingang mit identischer Konfiguration wie I1.
    - **Parameter**:
        - `Input` = `Input_I2` (Hardware-Mapping auf Eingang I2)
        - `InputEvent` = `BUTTON_SINGLE_CLICK`

- **E_MERGE**
    - **Typ**: `iec61499::events::E_MERGE`
    - **Beschreibung**: Ein Standard-Baustein zum Zusammenführen von Ereignissen. Er leitet ein eingehendes Event von einem der Eingänge (EI1 oder EI2) an den Ausgang (EO) weiter.

- **E_T_FF**
    - **Typ**: `adapter::events::unidirectional::AX_T_FF`
    - **Beschreibung**: Ein Baustein, der die Logik eines T-Flip-Flops kapselt und über Adapter-Schnittstellen kommuniziert. Er wechselt seinen Zustand bei jedem Eingangsimpuls am `CLK`-Eingang.

- **DigitalOutput_Q1**
    - **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
    - **Beschreibung**: Dieser Baustein steuert den physischen Ausgang an. Er empfängt seinen Zustand über eine Adapterverbindung.
    - **Parameter**:
        - `Output` = `Output_Q1` (Hardware-Mapping auf Ausgang Q1)

## Programmablauf und Verbindungen

Der Ablauf der Schaltung lässt sich wie folgt beschreiben:

1.  **Eingabeerfassung**:
    Die Bausteine `DigitalInput_CLK_I1` und `DigitalInput_CLK_I2` überwachen die Taster I1 und I2. Sobald einer der Taster einfach gedrückt wird (`BUTTON_SINGLE_CLICK`), wird am jeweiligen `IND`-Ausgang (Indication) ein Ereignis ausgelöst.

2.  **Ereignis-Zusammenführung (Merge)**:
    Die `IND`-Ausgänge beider Eingangsbausteine sind mit dem `E_MERGE`-Baustein verbunden:
    - `DigitalInput_CLK_I1.IND` -> `E_MERGE.EI1`
    - `DigitalInput_CLK_I2.IND` -> `E_MERGE.EI2`
    
    Egal welcher Taster gedrückt wird, der `E_MERGE`-Baustein gibt das Signal an seinem Ausgang `EO` aus. Dies realisiert eine ODER-Verknüpfung der Ereignisse (Event-OR).

3.  **Logik-Verarbeitung (Toggle)**:
    Das zusammengeführte Ereignissignal (`E_MERGE.EO`) ist mit dem Takteingang (`CLK`) des `E_T_FF` Bausteins verbunden. Bei jedem Impuls wechselt das Flip-Flop seinen internen Zustand von TRUE auf FALSE oder umgekehrt (Toggle-Funktion).

4.  **Ausgabe**:
    Der Zustand des `E_T_FF` wird nicht über eine klassische boolesche Datenleitung, sondern über eine Adapterverbindung übertragen.
    - `E_T_FF.Q` (Adapter Source) -> `DigitalOutput_Q1.OUT` (Adapter Destination)
    
    Der Baustein `DigitalOutput_Q1` übernimmt diesen Zustand und schaltet den physischen Ausgang Q1 entsprechend ein oder aus.

**Lernziele:**
- Umgang mit Input-Events (Single Click) auf dem logiBUS.
- Zusammenführen von asynchronen Ereignissen mittels `E_MERGE`.
- Verwendung von Adapter-basierten Funktionsbausteinen (`AX_T_FF` und `logiBUS_QXA`).

## Zusammenfassung

Die Übung `Uebung_004a2_AX` zeigt eine effiziente Methode, um eine Leuchte oder einen Aktor (Q1) von zwei verschiedenen Stellen (I1, I2) aus durch einfaches Drücken an- und auszuschalten (Wechselschaltung/Stromstoßschaltung). Durch die Verwendung von Event-Bausteinen und Adaptern wird die Verdrahtung im Funktionsplan übersichtlich gehalten und die spezifische Funktionalität des logiBUS (`BUTTON_SINGLE_CLICK`) demonstriert.