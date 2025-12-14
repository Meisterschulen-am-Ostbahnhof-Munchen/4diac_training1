# Uebung_032: LED Strip Blinkende LED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung eines LED-Streifens mit verschiedenen Farben und Tastern. Vier unabhängige Taster steuern jeweils eine LED in einer bestimmten Farbe mit einer Blinkfrequenz von 5 Hz.

## Verwendete Funktionsbausteine (FBs)

### logiBUS_IX (Taster-Bausteine)
- **Typ**: Eingangsbaustein für Taster
- **Verwendete interne FBs**: 4 Instanzen
    - **BUTTON_GREEN**: logiBUS_IX
        - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I1
    - **BUTTON_YELLOW**: logiBUS_IX
        - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I2
    - **BUTTON_RED**: logiBUS_IX
        - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I3
    - **BUTTON_BLUE**: logiBUS_IX
        - Parameter: QI = TRUE, Input = logiBUS_DI::Input_I4
- **Funktionsweise**: Liest den Zustand der physikalischen Taster-Eingänge und gibt diese über Daten- und Ereignisausgänge weiter

### logiBUS_LED_strip_QX (LED-Bausteine)
- **Typ**: Ausgangsbaustein für LED-Streifen
- **Verwendete interne FBs**: 4 Instanzen
    - **LED_GREEN_5HZ**: logiBUS_LED_strip_QX
        - Parameter: QI = TRUE, Output = LED_strip::Output_strip, Colour = LED_COLOURS::LED_GREEN, FREQ = LED_FREQ::LED_5HZ
    - **LED_YELLOW_5HZ**: logiBUS_LED_strip_QX
        - Parameter: QI = TRUE, Output = LED_strip::Output_strip, Colour = LED_COLOURS::LED_YELLOW, FREQ = LED_FREQ::LED_5HZ
    - **LED_RED_5HZ**: logiBUS_LED_strip_QX
        - Parameter: QI = TRUE, Output = LED_strip::Output_strip, Colour = LED_COLOURS::LED_RED, FREQ = LED_FREQ::LED_5HZ
    - **LED_BLUE_5HZ**: logiBUS_LED_strip_QX
        - Parameter: QI = TRUE, Output = LED_strip::Output_strip, Colour = LED_COLOURS::LED_BLUE, FREQ = LED_FREQ::LED_5HZ
- **Funktionsweise**: Steuert den LED-Streifen mit konfigurierter Farbe und Blinkfrequenz (5 Hz)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- BUTTON_GREEN.IND → LED_GREEN_5HZ.REQ
- BUTTON_YELLOW.IND → LED_YELLOW_5HZ.REQ
- BUTTON_RED.IND → LED_RED_5HZ.REQ
- BUTTON_BLUE.IND → LED_BLUE_5HZ.REQ

**Datenverbindungen:**
- BUTTON_GREEN.IN → LED_GREEN_5HZ.OUT
- BUTTON_YELLOW.IN → LED_YELLOW_5HZ.OUT
- BUTTON_RED.IN → LED_RED_5HZ.OUT
- BUTTON_BLUE.IN → LED_BLUE_5HZ.OUT

**Lernziele:**
- Verständnis der Taster-LED-Steuerung
- Umgang mit verschiedenen LED-Farben und Blinkfrequenzen
- Implementierung paralleler Steuerungsfunktionen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Basiswissen über Ereignis- und Datenverbindungen

**Starten der Übung:**
Die Übung wird automatisch gestartet, sobald das System initialisiert ist. Jeder Taster steuert unabhängig die entsprechende farbige LED mit 5 Hz Blinkfrequenz.

## Zusammenfassung
Diese Übung zeigt eine einfache aber effektive Steuerung eines LED-Streifens mit vier unabhängigen Tastern. Jeder Taster aktiviert eine spezifische LED-Farbe (Grün, Gelb, Rot, Blau) mit einer konstanten Blinkfrequenz von 5 Hz. Die parallele Architektur ermöglicht die gleichzeitige Steuerung mehrerer LEDs ohne gegenseitige Beeinflussung.