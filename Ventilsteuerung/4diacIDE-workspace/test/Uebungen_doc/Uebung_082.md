# Uebung_082: Beispiel für E_CTUD

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CTUD-Funktionsbausteins (Counter Up/Down) in der 4diac-IDE. Die Übung zeigt das Aufwärts- und Abwärtszählen sowie Reset- und Lade-Funktionalitäten eines Zählers und ist Teil des UAO Curriculum Module 3 - The IEC 61499 Standard.

## Verwendete Funktionsbausteine (FBs)

### E_CTUD (Counter Up/Down)
- **Typ**: E_CTUD
- **Parameter**: 
  - PV = UINT#5 (Preset Value = 5)
- **Ereigniseingänge**: CU (Count Up), CD (Count Down), R (Reset), LD (Load)
- **Ereignisausgänge**: CO (Count Overflow), RO (Reset Overflow), LDO (Load Overflow)
- **Datenausgänge**: QU (Q Up), QD (Q Down)

### DigitalInput_CLK_I1 bis I4
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 bis I4
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfassen von Tastendrücken an den digitalen Eingängen I1 bis I4

### DigitalOutput_Q1 und Q2
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1 bzw. Output_Q2
- **Funktionsweise**: Steuerung der digitalen Ausgänge Q1 und Q2

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- I1 (Taster) → E_CTUD.CU (Aufwärts zählen)
- I2 (Taster) → E_CTUD.CD (Abwärts zählen) 
- I3 (Taster) → E_CTUD.R (Reset)
- I4 (Taster) → E_CTUD.LD (Laden)
- E_CTUD.CO, RO, LDO → Q1.REQ und Q2.REQ

**Datenverbindungen:**
- E_CTUD.QU → DigitalOutput_Q1.OUT (Zählstand Aufwärts)
- E_CTUD.QD → DigitalOutput_Q2.OUT (Zählstand Abwärts)

**Lernziele:**
- Verständnis des E_CTUD-Funktionsbausteins
- Implementierung von Zählfunktionen
- Verwendung von digitalen Ein- und Ausgängen
- Ereignis- und Datenverbindungen in 4diac

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, 4diac-IDE Bedienung

**Starten der Übung**: Nach dem Laden der Applikation können die Taster I1-I4 betätigt werden, um die verschiedenen Zählfunktionen zu testen. Der Zähler hat einen Preset-Wert von 5.

## Zusammenfassung
Diese Übung vermittelt praktische Kenntnisse im Umgang mit dem E_CTUD-Zählerbaustein und demonstriert die Interaktion zwischen digitalen Ein- und Ausgängen. Die Implementierung zeigt alle wesentlichen Funktionen eines Up/Down-Zählers mit Reset- und Lade-Funktionalität.