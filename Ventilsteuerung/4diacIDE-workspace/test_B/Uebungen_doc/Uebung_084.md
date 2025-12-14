# Uebung_084: Beispiel für E_CYCLE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CYCLE-Funktionsbausteins in Kombination mit einem Aufwärtszähler (E_CTU). Das Programm zeigt, wie ein zyklischer Timer gesteuert werden kann und wie ein Zählerbaustein eingesetzt wird, um nach Erreichen eines bestimmten Wertes eine Ausgabe zu aktivieren.

## Verwendete Funktionsbausteine (FBs)

### E_CYCLE
- **Typ**: E_CYCLE
- **Parameter**: 
  - DT = T#1s (Zykluszeit von 1 Sekunde)
- **Funktionsweise**: Generiert in regelmäßigen Abständen Ereignisausgänge basierend auf der konfigurierten Zykluszeit

### E_CTU
- **Typ**: E_CTU (Counter Up)
- **Parameter**: 
  - PV = UINT#5 (Preset Value = 5)
- **Funktionsweise**: Zählt bei jedem Ereigniseingang CU um 1 hoch. Bei Erreichen des Preset-Wertes (5) wird der Ausgang Q aktiviert

### DigitalInput_CLK_I1, I2, I3
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_I1/I2/I3
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erkennt Einzelklicks auf Taster und generiert entsprechende Ereignisse

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Output aktiviert)
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den physischen Ausgang Q1 basierend auf den empfangenen Steuersignalen

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_CYCLE.EO → E_CTU.CU: Der Zyklus-Timer triggert den Zähler
- DigitalInput_CLK_I1.IND → E_CYCLE.START: Startet den Zyklus-Timer
- DigitalInput_CLK_I2.IND → E_CYCLE.STOP: Stoppt den Zyklus-Timer
- DigitalInput_CLK_I3.IND → E_CTU.R: Setzt den Zähler zurück
- E_CTU.CUO → DigitalOutput_Q1.REQ: Aktiviert Ausgang bei Zählerüberlauf
- E_CTU.RO → DigitalOutput_Q1.REQ: Aktiviert Ausgang bei Reset

**Datenverbindungen:**
- E_CTU.Q → DigitalOutput_Q1.OUT: Überträgt den Zählerstatus zum Ausgang

**Programmablauf:**
1. Durch Betätigen von Taster I1 wird der Zyklus-Timer gestartet
2. Der Timer generiert alle 1 Sekunde ein Ereignis
3. Jedes Timer-Ereignis erhöht den Zähler um 1
4. Bei Erreichen des Wertes 5 wird der Ausgang Q1 aktiviert
5. Taster I2 stoppt den Timer
6. Taster I3 setzt den Zähler zurück

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Ereignissteuerung in IEC 61499, insbesondere die Verwendung von zyklischen Timern und Aufwärtszählern. Die Kombination aus E_CYCLE und E_CTU zeigt ein typisches Muster für zeitgesteuerte Zählvorgänge in Automatisierungsanwendungen. Die Übung demonstriert zudem die Integration von physischen Ein- und Ausgängen über die logiBUS-Schnittstelle.