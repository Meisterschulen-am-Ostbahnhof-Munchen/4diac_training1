# Uebung_080c: Beispiel für E_CTU

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CTU-Funktionsbausteins für Aufwärtszählvorgänge. Die Übung zeigt, wie ein Zähler implementiert wird, der bei Erreichen eines bestimmten Wertes ein Signal ausgibt und wie die Eingangsereignisse durch zusätzliche Bausteine verarbeitet werden können.

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

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_CTU
- **Typ**: E_CTU
- **Parameter**:
  - PV = UINT#5

### E_PERMIT
- **Typ**: E_PERMIT

### E_T_FF
- **Typ**: E_T_FF

## Programmablauf und Verbindungen

Die Übung verwendet einen Aufwärtszähler (E_CTU) mit einem Preset-Wert von 5. Der Zähler wird durch Ereignisse von DigitalInput_CLK_I1 angesteuert, wobei die Ereignishäufigkeit durch die Kombination von E_T_FF und E_PERMIT halbiert wird.

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF.CLK
- E_T_FF.EO → E_PERMIT.EI
- E_PERMIT.EO → E_CTU.CU
- DigitalInput_CLK_I2.IND → E_CTU.R
- E_CTU.CUO → DigitalOutput_Q1.REQ
- E_CTU.RO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_CTU.Q → DigitalOutput_Q1.OUT
- E_T_FF.Q → E_PERMIT.PERMIT

**Lernziele:**
- Verständnis des E_CTU-Zählbausteins
- Implementierung von Ereignis-Halbierung
- Umgang mit digitalen Ein- und Ausgängen
- Kombination verschiedener Funktionsbausteine

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundkenntnisse in IEC 61499 und 4diac IDE

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Aufwärtszählers mit Ereignissteuerung. Durch die Kombination von T-Flipflop und PERMIT-Baustein wird demonstriert, wie Eingangsereignisse verarbeitet und in ihrer Frequenz angepasst werden können. Der Zähler gibt bei Erreichen des Preset-Wertes 5 ein Signal aus und kann über einen separaten Eingang zurückgesetzt werden.