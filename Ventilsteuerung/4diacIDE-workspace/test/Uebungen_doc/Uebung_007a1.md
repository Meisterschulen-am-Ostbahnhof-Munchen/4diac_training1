# Uebung_007a1: Blinker mit E_CYCLE und E_T_FF

* * * * * * * * * *

## Einleitung
Diese Übung implementiert einen Blinker mit E_CYCLE und E_T_FF Funktionsbausteinen. Die Anwendung demonstriert die Verwendung von zyklischen Ereignissen und eines Toggle-Flipflops zur Erzeugung eines Blinksignals. Ein besonderer Hinweis in der Übung weist auf einen Nachteil dieser Implementierung hin: Der Blinker bleibt zufällig auf AN oder AUS stehen, wenn er gestoppt wird.

## Verwendete Funktionsbausteine (FBs)

### E_CYCLE
- **Typ**: Zyklischer Ereignisgenerator
- **Parameter**: 
  - DT = T#1s (Zykluszeit von 1 Sekunde)
- **Ereigniseingänge**: START, STOP
- **Ereignisausgang**: EO

### E_T_FF
- **Typ**: Toggle-Flipflop
- **Ereigniseingänge**: CLK
- **Ereignisausgang**: EO
- **Datenausgang**: Q (BOOL)

### logiBUS_IE (START und STOP)
- **Typ**: Eingabeereignis-Baustein für logiBUS
- **Parameter**:
  - QI = TRUE (aktiviert)
  - Input = logiBUS_DI::Input_I1 (START) / Input_I2 (STOP)
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgang**: IND

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: Ausgabebaustein für logiBUS
- **Parameter**:
  - QI = TRUE (aktiviert)
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingang**: REQ
- **Dateneingang**: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_CYCLE.EO → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ
- START.IND → E_CYCLE.START
- STOP.IND → E_CYCLE.STOP

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Beim Betätigen des START-Buttons (I1) wird der zyklische Timer E_CYCLE gestartet
2. E_CYCLE generiert alle 1 Sekunde ein Ereignis an E_T_FF.CLK
3. E_T_FF toggelt seinen Ausgang Q bei jedem Clock-Ereignis
4. Der Q-Ausgang wird an die digitale Ausgabe Q1 weitergeleitet
5. Beim Betätigen des STOP-Buttons (I2) wird der Zyklus gestoppt

**Lernziele:**
- Verständnis von zyklischen Ereignisgeneratoren
- Anwendung von Toggle-Flipflops
- Umsetzung von Start/Stop-Funktionalität
- Praxis mit logiBUS-Ein-/Ausgabebausteinen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen

## Zusammenfassung
Diese Übung zeigt eine einfache Blinker-Implementierung mit E_CYCLE und E_T_FF. Die Anwendung demonstriert grundlegende Konzepte der ereignisgesteuerten Programmierung in 4diac. Der dokumentierte Nachteil (zufälliger Endzustand beim Stoppen) bietet eine gute Diskussionsgrundlage für erweiterte Implementierungen mit definierten Endzuständen.