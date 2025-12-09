# Uebung_080b: Beispiel für E_CTU mit E_SPLIT für Event-Verdoppelung

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CTU-Funktionsbausteins in Kombination mit einem E_SPLIT-Baustein zur Event-Verdoppelung. Es handelt sich um ein Aufwärtszählsystem, das als Beispiel für die Anwendung von IEC 61499 Standard-Komponenten dient.

## Verwendete Funktionsbausteine (FBs)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_CTU
- **Typ**: E_CTU (Up-Counter)
- **Parameter**:
  - PV = UINT#5 (Preset Value = 5)

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_SPLIT
- **Typ**: E_SPLIT (Event Splitter)
- **Funktionsweise**: Teilt ein eingehendes Event in zwei identische Ausgangs-Events auf

## Programmablauf und Verbindungen

**Event-Verbindungen:**
- DigitalInput_CLK_I1.IND → E_SPLIT.EI
- E_SPLIT.EO1 → E_CTU.CU
- E_SPLIT.EO2 → E_CTU.CU
- DigitalInput_CLK_I2.IND → E_CTU.R
- E_CTU.CUO → DigitalOutput_Q1.REQ
- E_CTU.RO → DigitalOutput_Q1.REQ

**Daten-Verbindungen:**
- E_CTU.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Ein Tastendruck auf Input_I1 löst über E_SPLIT zwei identische Count-Events für E_CTU aus
2. E_CTU zählt bei jedem CU-Event hoch (bis zum Preset-Wert 5)
3. Ein Tastendruck auf Input_I2 resetet den Zähler (E_CTU.R)
4. Bei Erreichen des Preset-Werts (CUO) oder Reset (RO) wird die Ausgabe Q1 aktiviert

**Besonderheit:** Durch den E_SPLIT wird jedes Eingangs-Event von I1 verdoppelt, was zu einer speziellen Zählcharakteristik führt.

## Zusammenfassung
Diese Übung zeigt die praktische Anwendung des E_CTU-Zählbausteins in Kombination mit Event-Manipulation durch E_SPLIT. Sie demonstriert das Konzept der Event-Verdoppelung und deren Auswirkung auf den Zählvorgang. Die Übung eignet sich zum Verständnis von Event-basierter Steuerung und Zählerfunktionalitäten in IEC 61499 Systemen.