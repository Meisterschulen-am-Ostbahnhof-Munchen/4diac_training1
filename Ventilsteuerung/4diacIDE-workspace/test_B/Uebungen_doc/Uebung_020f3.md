Hier ist die Dokumentation für die Übung `Uebung_020f3` basierend auf den bereitgestellten Daten.

# Uebung_020f3

![Uebung_020f3](Uebung_020f3.png)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung eines digitalen Eingangsereignisses, um einen Blink-Generator zu starten, der wiederum einen digitalen Ausgang ansteuert. Konkret wird ein einfacher Klick auf den Eingang `I1` verwendet, um den Blinker zu aktivieren, dessen Signal auf den Ausgang `Q1` ausgegeben wird.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden logiBUS-Bausteine für die Ein- und Ausgabe sowie ein Standard-Utility-Baustein für die Signalerzeugung verwendet.

### Sub-Bausteine: DigitalInput_I1
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalInput_I1
        - **Parameter**: 
            - `QI` = TRUE
            - `Input` = Input_I1
            - `InputEvent` = BUTTON_SINGLE_CLICK
        - **Ereignisausgang**: `IND` (Indication - wird ausgelöst, wenn das definierte Ereignis eintritt)
- **Funktionsweise**: Dieser Baustein überwacht den digitalen Eingang `I1`. Er ist so konfiguriert, dass er speziell auf einen "Single Click" (einfachen Tastendruck) reagiert und daraufhin ein Ereignis auslöst.

### Sub-Bausteine: E_BLINK
- **Typ**: `eclipse4diac::utils::signals::E_BLINK`
- **Verwendete interne FBs**:
    - **Bausteinname**: E_BLINK
        - **Parameter**: 
            - `TIMELOW` = T#1s (Zeitdauer für den FALSE-Zustand)
            - `TIMEHIGH` = T#1s200ms (Zeitdauer für den TRUE-Zustand)
        - **Ereigniseingang**: `START`
        - **Ereignisausgang**: `CNF`
        - **Datenausgang**: `OUT`
- **Funktionsweise**: Ein asymmetrischer Taktgeber (Blinker). Er erzeugt ein boolesches Signal, das zwischen FALSE (1 Sekunde) und TRUE (1,2 Sekunden) wechselt.

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QX`
- **Verwendete interne FBs**:
    - **Bausteinname**: DigitalOutput_Q1
        - **Parameter**: 
            - `QI` = TRUE
            - `Output` = Output_Q1
        - **Ereigniseingang**: `REQ`
        - **Dateneingang**: `OUT` (verbunden mit dem Parameter `Output` intern)
- **Funktionsweise**: Dieser Baustein steuert den physischen digitalen Ausgang `Q1`. Bei jedem `REQ`-Ereignis wird der Wert am Dateneingang auf den Hardware-Ausgang geschrieben.

## Programmablauf und Verbindungen

Der Ablauf der Schaltung wird durch Ereignis- und Datenverbindungen gesteuert:

1.  **Start des Blinkers**:
    - Das Ereignis `IND` vom Baustein `DigitalInput_I1` ist mit dem Ereigniseingang `START` des Bausteins `E_BLINK` verbunden.
    - Sobald am Eingang `I1` ein einfacher Klick (`BUTTON_SINGLE_CLICK`) registriert wird, startet der Blink-Zyklus.

2.  **Signalverarbeitung und Ausgabe**:
    - Der `E_BLINK`-Baustein wechselt seinen Zustand basierend auf den Zeiten `TIMELOW` (1 Sekunde) und `TIMEHIGH` (1,2 Sekunden).
    - Bei jedem Zustandswechsel feuert `E_BLINK` das `CNF`-Ereignis, welches mit dem `REQ`-Eingang von `DigitalOutput_Q1` verbunden ist. Dies triggert die Aktualisierung des Ausgangs.
    - Der Datenwert `OUT` (TRUE oder FALSE) des Blinkers wird an den Eingang `OUT` des `DigitalOutput_Q1` übertragen, wodurch die LED oder der Aktor an `Q1` im Takt des Blinkers ein- und ausgeschaltet wird.

**Lernziele:**
- Umgang mit logiBUS Event-Eingängen (Single Click).
- Verwendung von Zeit-Parametern in Funktionsbausteinen (T#1s, T#1s200ms).
- Verknüpfung von Logikbausteinen (Blinker) mit Hardware-Ausgängen.

## Zusammenfassung
Die Übung `Uebung_020f3` realisiert eine blinkende Signalausgabe an Ausgang `Q1`, die durch eine Benutzerinteraktion (Klick) an Eingang `I1` ausgelöst wird. Dabei kommt ein asymmetrisches Blinkmuster (1s Aus, 1.2s An) zum Einsatz.