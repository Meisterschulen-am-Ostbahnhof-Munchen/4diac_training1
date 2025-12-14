# Uebung_019b: Umschalten einer Maske

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert das Umschalten zwischen verschiedenen Masken auf einem Display und die Steuerung eines Alarmausgangs. Das System ermöglicht die Auswahl unterschiedlicher Anzeigemasken über Tastereingänge und behandelt gleichzeitig Alarmzustände.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1, DigitalInput_CLK_I2, DigitalInput_CLK_I3
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 (bzw. I2, I3)
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfassen von Tasterereignissen mit Einfachklick-Erkennung

### Q_ActiveMask
- **Typ**: Q_ActiveMask
- **Parameter**:
  - u16WorkSetId = DefaultPool::WorkingSet_0
- **Funktionsweise**: Verwaltung und Anzeige der aktiven Maske auf dem Display

### F_SEL_E_2
- **Typ**: F_SEL_E_4
- **Parameter**:
  - IN0 = DefaultPool::DataMask_M1
  - IN1 = DefaultPool::DataMask_M2
  - IN2 = DefaultPool::AlarmMask_A2_medium
  - IN3 = DefaultPool::DataMask_M1
- **Funktionsweise**: Multiplexer für die Auswahl zwischen vier verschiedenen Masken

### ACK
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = isobus::ID_NULL
  - InputEvent = SoftKeyActivationCode::SK_PRESSED
- **Funktionsweise**: Erfassung von Softkey-Ereignissen

### E_SR
- **Typ**: E_SR
- **Funktionsweise**: Set-Reset-Flipflop zur Alarmzustandssteuerung

### Alarmausgang
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuerung des physischen Alarmausgangs

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- DigitalInput_CLK_I1.IND → F_SEL_E_2.REQ0 (Maske M1)
- DigitalInput_CLK_I2.IND → F_SEL_E_2.REQ1 (Maske M2) 
- DigitalInput_CLK_I3.IND → F_SEL_E_2.REQ2 (Alarmmaske A2)
- ACK.IND → F_SEL_E_2.REQ3 (Maske M1)
- F_SEL_E_2.CNF → Q_ActiveMask.REQ
- DigitalInput_CLK_I3.IND → E_SR.S (Alarm setzen)
- DigitalInput_CLK_I2.IND → E_SR.R (Alarm zurücksetzen)
- DigitalInput_CLK_I1.IND → E_SR.R (Alarm zurücksetzen)
- ACK.IND → E_SR.R (Alarm zurücksetzen)
- E_SR.EO → Alarmausgang.REQ

### Datenverbindungen:
- F_SEL_E_2.OUT → Q_ActiveMask.u16NewMaskId
- E_SR.Q → Alarmausgang.OUT

### Lernziele:
- Verständnis von Maskenumschaltung auf Displays
- Implementierung von Multiplexer-Funktionalität
- Steuerung von Alarmzuständen mit Set-Reset-Logik
- Integration von Taster- und Softkey-Eingaben

### Bedienung:
- Taster I1: Schaltet auf Maske M1 und setzt Alarm zurück
- Taster I2: Schaltet auf Maske M2 und setzt Alarm zurück  
- Taster I3: Schaltet auf Alarmmaske A2 und setzt Alarm
- ACK-Key: Schaltet auf Maske M1 und setzt Alarm zurück

## Zusammenfassung
Diese Übung zeigt ein komplettes System zur Maskensteuerung mit integrierter Alarmbehandlung. Durch die Verwendung eines 4-fach Multiplexers können verschiedene Anzeigemasken ausgewählt werden, während ein Set-Reset-Flipflop die Alarmzustände verwaltet. Die Kombination aus Display-Steuerung und Alarmlogik macht diese Übung zu einem praktischen Beispiel für industrielle HMI-Anwendungen.