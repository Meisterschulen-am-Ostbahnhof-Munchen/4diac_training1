# Uebung_007a2: Blinker mit E_CYCLE und E_T_FF

* * * * * * * * * *

## Einleitung
Diese Übung implementiert einen Blinker mit E_CYCLE und E_T_FF Funktionsbausteinen. Die Anwendung demonstriert die Verwendung von zyklischen Ereignissen und eines Toggle-Flipflops zur Erzeugung eines Blinksignals. Ein besonderer Hinweis in der Übung weist auf einen Nachteil dieser Implementierung hin: Der Blinker kann zufällig im AN- oder AUS-Zustand stehen bleiben.

## Verwendete Funktionsbausteine (FBs)

### E_CYCLE
- **Typ**: E_CYCLE (Zyklusgeber)
- **Parameter**: DT = T#1s (Zykluszeit von 1 Sekunde)
- **Ereigniseingänge**: START, STOP
- **Ereignisausgang**: EO

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flipflop)
- **Ereigniseingang**: CLK
- **Ereignisausgang**: EO
- **Datenausgang**: Q (Boolescher Ausgang)

### logiBUS_IE (START und STOP)
- **Typ**: logiBUS_IE (Eingabeereignis-Baustein)
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 (START) / logiBUS_DI::Input_I2 (STOP)
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgang**: IND

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: logiBUS_QX (Ausgabebaustein)
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingang**: REQ
- **Dateneingang**: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_CYCLE.EO → E_T_FF.CLK (Zyklusereignis triggert Flipflop)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flipflop-Ausgang triggert Ausgabe)
- START.IND → E_CYCLE.START (Start-Button startet Zyklus)
- STOP.IND → E_CYCLE.STOP (Stop-Button stoppt Zyklus)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flipflop-Zustand an Ausgabe)

**Funktionsweise:**
1. Beim Betätigen des START-Buttons (I1) wird der E_CYCLE-Baustein gestartet
2. E_CYCLE generiert alle 1 Sekunde ein Ereignis an EO
3. Dieses Ereignis triggert den E_T_FF-Baustein über CLK
4. E_T_FF toggelt seinen Ausgang Q bei jedem Ereignis
5. Der Q-Ausgang wird an die digitale Ausgabe Q1 weitergeleitet
6. Das Ergebnis ist ein blinkendes Signal mit 0,5 Hz Frequenz
7. Der STOP-Button (I2) beendet den Zyklus

**Lernziele:**
- Verständnis von zyklischen Ereignisgebern
- Anwendung von Toggle-Flipflops
- Umsetzung von Start/Stop-Funktionalität
- Handling von Ereignis- und Datenverbindungen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen

## Zusammenfassung
Diese Übung zeigt eine einfache Blinker-Implementierung mit E_CYCLE und E_T_FF. Die Anwendung demonstriert grundlegende Konzepte der Ereignisverarbeitung und Zustandssteuerung in IEC 61499. Der implementierte Blinker bietet Start/Stop-Funktionalität über externe Taster, wobei ein bekannter Nachteil in der zufälligen Endposition des Blinkzustands liegt.