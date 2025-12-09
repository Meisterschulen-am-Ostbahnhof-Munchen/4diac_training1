# Uebung_004a3: wie Uebung_004a2 aber ohne E_MERGE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines T-Flipflops (Toggle-Flipflop) in der 4diac-IDE. Im Vergleich zur vorherigen Übung 004a2 wurde der E_MERGE-Baustein entfernt, um eine direktere Verbindung zwischen den Eingängen und dem Flipflop zu zeigen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgang**: IND

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgang**: IND

### E_T_FF
- **Typ**: E_T_FF (T-Flipflop)
- **Ereigniseingang**: CLK
- **Ereignisausgang**: EO
- **Datenausgang**: Q

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingang**: REQ
- **Dateneingang**: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_T_FF.EO → DigitalOutput_Q1.REQ
- DigitalInput_CLK_I1.IND → E_T_FF.CLK
- DigitalInput_CLK_I2.IND → E_T_FF.CLK

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Lernziele:**
- Verständnis der Funktionsweise eines T-Flipflops
- Umgang mit digitalen Ein- und Ausgängen in logiBUS
- Implementierung von Toggle-Funktionalität ohne E_MERGE-Baustein

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis von Flipflop-Schaltungen
- Basiswissen über Ereignis- und Datenverbindungen

**Starten der Übung:**
Die Übung wird durch Betätigen der Taster I1 oder I2 gestartet. Jeder Tastendruck toggelt den Ausgangszustand des Flipflops.

## Zusammenfassung
Diese Übung zeigt eine vereinfachte Implementierung eines T-Flipflops, bei der zwei digitale Eingänge direkt mit dem Clock-Eingang des Flipflops verbunden sind. Der Ausgang Q1 schaltet bei jedem Tastendruck an I1 oder I2 zwischen den Zuständen ein und aus. Die Übung demonstriert effektiv die grundlegende Toggle-Funktionalität ohne zusätzliche Verschmelzungsbausteine.