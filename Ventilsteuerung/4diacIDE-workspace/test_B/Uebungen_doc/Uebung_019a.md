# Uebung_019a: Umschalten einer Maske

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert das Umschalten zwischen verschiedenen Anzeigemasken auf einem Display. Durch Betätigung verschiedener Eingänge können unterschiedliche Masken aktiviert werden, was typische Szenarien in der Bedienoberfläche von industriellen Anlagen abbildet.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1, DigitalInput_CLK_I2, DigitalInput_CLK_I3
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 / Input_I2 / Input_I3
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfassen von Tastendruck-Ereignissen an den digitalen Eingängen I1, I2 und I3

### Q_ActiveMask
- **Typ**: Q_ActiveMask
- **Parameter**:
  - u16WorkSetId = DefaultPool::WorkingSet_0
- **Funktionsweise**: Verwaltung und Aktivierung der aktuellen Anzeigemaske

### F_SEL_E_2
- **Typ**: F_SEL_E_4
- **Parameter**:
  - IN0 = DefaultPool::DataMask_M1
  - IN1 = DefaultPool::DataMask_M2
  - IN2 = DefaultPool::AlarmMask_A2_medium
  - IN3 = DefaultPool::DataMask_M1
- **Funktionsweise**: Selektiert basierend auf dem auslösenden Ereignis eine der vier vordefinierten Masken

### ACK
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = isobus::ID_NULL
  - InputEvent = SoftKeyActivationCode::SK_PRESSED
- **Funktionsweise**: Erfassung von Softkey-Betätigungen

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → F_SEL_E_2.REQ0 (aktiviert Maske M1)
- DigitalInput_CLK_I2.IND → F_SEL_E_2.REQ1 (aktiviert Maske M2)
- DigitalInput_CLK_I3.IND → F_SEL_E_2.REQ2 (aktiviert Alarmmaske A2)
- ACK.IND → F_SEL_E_2.REQ3 (aktiviert Maske M1)
- F_SEL_E_2.CNF → Q_ActiveMask.REQ

**Datenverbindungen:**
- F_SEL_E_2.OUT → Q_ActiveMask.u16NewMaskId

**Lernziele:**
- Verständnis des Maskenmanagements in industriellen Steuerungen
- Implementierung von Maskenumschaltungen über verschiedene Eingänge
- Verwendung von Selektionsfunktionsbausteinen
- Integration von Softkey-Funktionalität

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignisverarbeitung

**Starten der Übung**: Die Übung wird durch Betätigung der digitalen Eingänge I1, I2, I3 oder des ACK-Softkeys gestartet.

## Zusammenfassung
Diese Übung zeigt ein praktisches Beispiel für das dynamische Umschalten zwischen verschiedenen Anzeigemasken in einer industriellen Steuerung. Durch die Verwendung von digitalen Eingängen und Softkeys können unterschiedliche Masken (Datenmasken M1/M2 und eine Alarmmaske) aktiviert werden. Die Implementierung demonstriert effektiv die Ereignisverarbeitung und Datenweitergabe zwischen Funktionsbausteinen in einem typischen HMI-Szenario.