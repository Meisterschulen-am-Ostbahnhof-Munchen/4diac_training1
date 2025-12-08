# Uebung_019c: Umschalten einer Maske

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert das Umschalten zwischen verschiedenen Masken auf einem Anzeigegerät. Das System ermöglicht die Auswahl unterschiedlicher Anzeigemasken über Tastereingänge und behandelt gleichzeitig Alarmzustände mit entsprechender Visualisierung.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1 / DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 / logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### Q_ActiveMask
- **Typ**: Q_ActiveMask
- **Parameter**:
  - u16WorkSetId = DefaultPool::WorkingSet_0

### F_SEL_E_2
- **Typ**: F_SEL_E_4
- **Parameter**:
  - IN0 = DefaultPool::DataMask_M1
  - IN1 = DefaultPool::DataMask_M2
  - IN2 = DefaultPool::AlarmMask_A2_medium
  - IN3 = DefaultPool::DataMask_M1

### ACK
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I4
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_SR
- **Typ**: E_SR

### Alarmausgang
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q8

### Alarmeingang
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I3

### E_SWITCH / E_PERMIT_INVERT / E_PERMIT_INVERT_1 / E_PERMIT_INVERT_2
- **Typ**: E_SWITCH

## Programmablauf und Verbindungen

Das System arbeitet mit folgenden Hauptfunktionen:

**Maskenauswahl:**
- Taster I1 und I2 dienen zur Auswahl zwischen verschiedenen Datenmasken (M1, M2)
- Jeder Tastendruck löst über E_PERMIT_INVERT_1 und E_PERMIT_INVERT_2 die entsprechende Maskenanforderung aus
- Die Auswahl erfolgt über den F_SEL_E_2 Baustein, der zwischen vier verschiedenen Masken wählen kann

**Alarmbehandlung:**
- Ein Alarmeingang (I3) überwacht den Alarmzustand
- Bei Alarmaktivierung wird automatisch auf die Alarmmaske A2_medium umgeschaltet
- Der Alarmzustand wird über ein E_SR Flip-Flop gespeichert
- Ein Bestätigungstaster (I4) dient zur Alarmquittierung

**Ereignisverbindungen:**
- Tasterereignisse werden zu den E_SWITCH und E_PERMIT Bausteinen geleitet
- Maskenauswahl-Ereignisse werden an Q_ActiveMask weitergegeben
- Alarmereignisse steuern das E_SR Flip-Flop und die Alarmausgabe

**Datenverbindungen:**
- Die ausgewählte Masken-ID wird an Q_ActiveMask übergeben
- Alarmzustände werden an den physischen Ausgang Q8 weitergeleitet
- Alarmeingangssignale werden an mehrere Schalterbausteine verteilt

## Zusammenfassung
Diese Übung vermittelt praktische Kenntnisse in der Maskensteuerung und Alarmbehandlung in Automatisierungssystemen. Sie zeigt die Integration von Tastereingängen, die Auswahl zwischen verschiedenen Anzeigemasken und die Behandlung von Alarmzuständen mit Quittierungsmöglichkeit. Das System demonstriert eine typische Anwendung in der Prozessvisualisierung mit strukturierter Ereignis- und Datenverarbeitung.