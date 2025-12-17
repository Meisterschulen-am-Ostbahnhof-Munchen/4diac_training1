Hier ist die Dokumentation für die Übung `Uebung_033_sub` basierend auf den bereitgestellten Daten.

# Uebung_033_sub

![Uebung_033_sub Bild](Uebung_033_sub.png)

* * * * * * * * * *

## Einleitung

Die Übung **Uebung_033_sub** implementiert eine Sub-Applikation zur Steuerung einer LED auf einem LED-Streifen. Das Ziel ist es, eine LED basierend auf einem digitalen Eingangssignal (Taster/Schalter) zum Blinken zu bringen. Die Applikation kapselt die Logik zwischen einem LogiBUS-Eingangsbaustein und einem LED-Ausgangsbaustein und ermöglicht die Parametrierung von Farbe, Eingangsquelle und Ausgangsnummer von außen.

## Verwendete Funktionsbausteine (FBs)

Diese Übung ist selbst als Sub-Applikation (`SubAppType`) definiert und enthält intern verschaltete Funktionsbausteine.

### Sub-Bausteine: Uebung_033_sub

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **BUTTON**: `logiBUS::io::DI::logiBUS_IX`
        - Parameter: `QI` = `TRUE`
        - Dateneingang: `Input` (Verbunden mit externem Input-Parameter)
        - Ereignisausgang: `IND` (Indication - Signalisiert Statusänderung)
        - Datenausgang: `IN` (Aktueller Status des Eingangs)
    - **LED**: `logiBUS::io::DO_LED::logiBUS_LED_strip_QX`
        - Parameter: `QI` = `TRUE`
        - Parameter: `FREQ` = `LED_FREQ::LED_1HZ` (Setzt Blinkfrequenz auf 1 Hz)
        - Ereigniseingang: `REQ` (Request - Aktualisierungsanfrage)
        - Dateneingang: `OUT` (Ein/Aus Status der LED, kommt vom BUTTON)
        - Dateneingang: `Output` (Nummer der LED auf dem Streifen, externer Parameter)
        - Dateneingang: `Colour` (Farbe der LED, externer Parameter)

- **Funktionsweise**:
    Dieser Sub-Baustein verbindet einen physikalischen Eingang (`BUTTON`) direkt mit einer LogiBUS-LED (`LED`). Wenn das Eingangssignal empfangen wird, wird der Status an die LED weitergeleitet. Durch den Parameter `FREQ` ist die LED so konfiguriert, dass sie blinkt (1 Hz), sofern der Baustein dies basierend auf dem Eingangssignal aktiviert.

## Programmablauf und Verbindungen

Der Programmablauf innerhalb der Sub-Applikation gestaltet sich wie folgt:

1.  **Schnittstelle (Inputs):**
    *   `Input`: Definiert, welcher physische Eingang (z.B. I1..I8) überwacht wird. Standardwert ist `Invalid`.
    *   `Colour`: Bestimmt die Farbe der LED (UINT). Standardwert ist Grün (`LED_COLOURS::LED_GREEN`).
    *   `Output`: Bestimmt den Index der LED auf dem LED-Streifen (USINT).

2.  **Verarbeitung:**
    *   Der Baustein **BUTTON** liest den Zustand des über `Input` definierten Eingangs.
    *   Sobald sich der Status des Tasters ändert oder aktualisiert wird, sendet der **BUTTON**-Baustein ein Event über `IND` an den `REQ`-Eingang des **LED**-Bausteins.
    *   Gleichzeitig wird der logische Zustand des Tasters (`IN`) an den Eingang `OUT` des **LED**-Bausteins übertragen. Dies aktiviert oder deaktiviert die LED-Logik.

3.  **Ausgabe:**
    *   Der **LED**-Baustein steuert die entsprechende LED (definiert durch `Output`) in der gewünschten Farbe (`Colour`) an.
    *   Aufgrund des festen Parameters `FREQ = LED_FREQ::LED_1HZ` blinkt die LED mit einer Frequenz von 1 Hertz, solange sie durch den Taster aktiviert ist.

**Daten- und Eventfluss:**
*   `BUTTON.IND` -> `LED.REQ` (Event-Triggerung)
*   `BUTTON.IN` -> `LED.OUT` (Statusweitergabe)
*   Externe Parameter (`Input`, `Output`, `Colour`) versorgen die entsprechenden Eingänge der internen FBs.

## Zusammenfassung

Die `Uebung_033_sub` stellt einen wiederverwendbaren Baustein dar, um eine blinkende LED-Funktionalität auf einem LogiBUS-System einfach zu implementieren. Sie abstrahiert die direkte Verschaltung von Eingangs- und Ausgangstreibern und ermöglicht die Konfiguration der Hardware-Zuordnung (Welcher Taster? Welche LED?) sowie der Farbe über die Baustein-Schnittstelle.