# Uebung_030: LED_PWM Blinkende LED

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Anwendung von PWM-gesteuerten LEDs mit verschiedenen Blinkfrequenzen. Es werden vier verschiedene Betriebsmodi einer LED über digitale Eingänge gesteuert, wobei jeder Eingang eine spezifische Blinkfrequenz oder Betriebsart aktiviert.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

**DigitalInput_I1, DigitalInput_I2, DigitalInput_I3, DigitalInput_I4**
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 bis Input_I4
- **Funktionsweise**: Digitale Eingangsbausteine zur Erfassung von Schalterzuständen

**LED_Q1_5HZ**
- **Typ**: logiBUS_LED_PWM_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
  - FREQ = LED_FREQ::LED_5HZ
- **Funktionsweise**: Steuert LED Q1 mit 5Hz Blinkfrequenz

**LED_Q1_1HZ**
- **Typ**: logiBUS_LED_PWM_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
  - FREQ = LED_FREQ::LED_1HZ
- **Funktionsweise**: Steuert LED Q1 mit 1Hz Blinkfrequenz

**LED_Q1_breathing_05HZ**
- **Typ**: logiBUS_LED_PWM_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
  - FREQ = LED_FREQ::LED_05HZ
- **Funktionsweise**: Steuert LED Q1 mit 0.5Hz Blinkfrequenz (Atmungseffekt)

**LED_Q1_ON_1**
- **Typ**: logiBUS_LED_PWM_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
  - FREQ = LED_FREQ::LED_ON
- **Funktionsweise**: Schaltet LED Q1 dauerhaft ein

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- DigitalInput_I1.IND → LED_Q1_5HZ.REQ
- DigitalInput_I2.IND → LED_Q1_1HZ.REQ
- DigitalInput_I3.IND → LED_Q1_breathing_05HZ.REQ
- DigitalInput_I4.IND → LED_Q1_ON_1.REQ

### Datenverbindungen:
- DigitalInput_I1.IN → LED_Q1_5HZ.OUT
- DigitalInput_I2.IN → LED_Q1_1HZ.OUT
- DigitalInput_I3.IN → LED_Q1_breathing_05HZ.OUT
- DigitalInput_I4.IN → LED_Q1_ON_1.OUT

### Lernziele:
- Verständnis der PWM-LED-Steuerung
- Umgang mit verschiedenen Blinkfrequenzen
- Steuerung von Ausgängen über digitale Eingänge
- Implementierung von Mehrfachauswahl für LED-Betriebsarten

### Schwierigkeitsgrad:
Einfach - geeignet für Einsteiger in die 4diac-IDE

### Benötigte Vorkenntnisse:
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Basiswissen über digitale Ein- und Ausgänge

### Start der Übung:
Die Übung wird durch Aktivieren der digitalen Eingänge I1-I4 gestartet. Jeder Eingang aktiviert einen spezifischen LED-Betriebsmodus an Ausgang Q1.

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung zur Steuerung einer LED mit verschiedenen PWM-Frequenzen. Vier digitale Eingänge ermöglichen die Auswahl zwischen vier verschiedenen Betriebsarten: 5Hz Blinken, 1Hz Blinken, 0.5Hz Atmungseffekt und Dauerlicht. Die Übung vermittelt grundlegende Konzepte der Signalverarbeitung und Ausgangssteuerung in verteilten Automatisierungssystemen.