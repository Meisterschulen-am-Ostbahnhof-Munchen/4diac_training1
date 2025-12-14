# Uebung_019: Umschalten einer Maske

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert das Umschalten zwischen verschiedenen Masken auf einem logi.BUS-System. Das Programm ermöglicht es, durch Betätigung von Tastern zwischen zwei vordefinierten Masken zu wechseln.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### F_SEL_E_2
- **Typ**: F_SEL_E_2
- **Parameter**:
  - IN0 = DefaultPool::DataMask_M1
  - IN1 = DefaultPool::DataMask_M2

### Q_ActiveMask
- **Typ**: Q_ActiveMask
- **Parameter**:
  - u16WorkSetId = DefaultPool::WorkingSet_0

## Programmablauf und Verbindungen

Das Programm arbeitet nach folgendem Prinzip:

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → F_SEL_E_2.REQ0
- DigitalInput_CLK_I2.IND → F_SEL_E_2.REQ1
- F_SEL_E_2.CNF → Q_ActiveMask.REQ

**Datenverbindungen:**
- F_SEL_E_2.OUT → Q_ActiveMask.u16NewMaskId

**Funktionsweise:**
- Taster I1 (Single-Click) aktiviert Maske M1
- Taster I2 (Single-Click) aktiviert Maske M2
- Der F_SEL_E_2 Baustein wählt basierend auf dem auslösenden Ereignis die entsprechende Maske aus
- Q_ActiveMask setzt die ausgewählte Maske auf dem WorkingSet_0 aktiv

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundkenntnisse in 4diac FORTE, logi.BUS Systemaufbau
**Start der Übung**: Programm auf logi.BUS System laden und Taster I1/I2 betätigen

## Zusammenfassung
Diese Übung zeigt das grundlegende Prinzip des Maskenumschaltens auf logi.BUS-Systemen. Durch die Verwendung von Digital-Inputs mit Single-Click Events und einem Selektor-Baustein wird ein zuverlässiger Wechsel zwischen verschiedenen Anzeigemasken realisiert.