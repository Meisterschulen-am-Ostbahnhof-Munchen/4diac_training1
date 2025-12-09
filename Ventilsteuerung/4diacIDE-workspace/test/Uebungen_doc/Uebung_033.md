# Uebung_033: LED Strip Blinkende LED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung eines LED-Streifens mit blinkenden LEDs in verschiedenen Farben. Es werden vier unabhängige LED-Kanäle (GRÜN, GELB, ROT, BLAU) implementiert, die jeweils über separate Eingänge angesteuert werden können.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_033_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **BUTTON**: logiBUS_IX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: IND → LED.REQ
        - Datenausgang/-eingang: IN → LED.OUT
    - **LED**: logiBUS_LED_strip_QX
        - Parameter: QI = TRUE, FREQ = LED_FREQ::LED_1HZ
        - Ereignisausgang/-eingang: REQ (von BUTTON.IND)
        - Datenausgang/-eingang: OUT (von BUTTON.IN)
- **Funktionsweise**: Der Sub-Baustein verbindet einen Eingangstaster (BUTTON) mit einer LED-Streifen-Steuerung. Bei Betätigung des Tasters wird die LED mit der konfigurierten Farbe und Blinkfrequenz aktiviert.

## Programmablauf und Verbindungen
Die Hauptanwendung besteht aus vier identischen Sub-Bausteinen (GREEN, YELLOW, RED, BLUE), die parallel arbeiten. Jeder Sub-Baustein verfügt über:
- Einen Eingang für die Tastererkennung (Input)
- Eine Farbkonfiguration (Colour) 
- Einen Ausgang für den LED-Streifen (Output)

Die Datenverbindungen übertragen:
- Input-Signal an den BUTTON-Baustein
- Ausgangsnummer an die LED-Steuerung
- Farbinformation an die LED-Steuerung

Die Ereignisverbindung sorgt dafür, dass bei Tasterbetätigung (BUTTON.IND) ein Anforderungssignal an die LED-Steuerung (LED.REQ) gesendet wird.

**Lernziele**: 
- Verständnis der parallelen Verarbeitung mit Sub-Bausteinen
- Umgang mit LED-Streifen-Steuerung
- Implementierung von Taster-LED-Interaktionen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Datenverbindungen

**Starten der Übung**: Nach dem Laden der Anwendung können die vier farbigen Kanäle unabhängig voneinander über ihre jeweiligen Eingänge aktiviert werden.

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung zur Steuerung eines mehrfarbigen LED-Streifens mit unabhängigen Kanälen. Die modulare Struktur mit wiederverwendbaren Sub-Bausteinen ermöglicht eine klare und übersichtliche Programmarchitektur, die einfach erweitert werden kann.