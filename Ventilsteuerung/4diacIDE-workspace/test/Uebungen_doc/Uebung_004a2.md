# Uebung_004a2: mit E_MERGE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines T-Flipflops in Kombination mit einem Ereignis-Merge-Baustein zur Steuerung einer digitalen Ausgabe. Die Besonderheit liegt in der Verwendung von zwei unabhängigen Eingängen, deren Ereignisse zusammengeführt werden, um den Toggle-Vorgang auszulösen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfasst Einzelklick-Ereignisse von digitalem Eingang I1

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfasst Einzelklick-Ereignisse von digitalem Eingang I2

### E_MERGE
- **Typ**: E_MERGE
- **Funktionsweise**: Führt Ereignisse von zwei Eingängen (EI1 und EI2) zusammen und gibt sie über einen gemeinsamen Ausgang (EO) aus

### E_T_FF
- **Typ**: E_T_FF (T-Flipflop)
- **Funktionsweise**: Toggelt den Ausgangszustand bei jedem ankommenden Takt-Ereignis (CLK)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert den digitalen Ausgang Q1 basierend auf dem empfangenen Wert

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_MERGE.EI1
- DigitalInput_CLK_I2.IND → E_MERGE.EI2
- E_MERGE.EO → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Lernziele:**
- Verständnis des T-Flipflop-Verhaltens
- Umgang mit Ereignis-Merge-Bausteinen
- Kombination mehrerer Eingangsereignisse zu einer gemeinsamen Aktion
- Praktische Anwendung digitaler Ein- und Ausgänge

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen

**Starten der Übung**: Die Übung wird durch Betätigen der Taster I1 oder I2 gestartet. Jeder Tastendruck toggelt den Zustand von Ausgang Q1.

## Zusammenfassung
Diese Übung zeigt eine elegante Lösung zur Steuerung eines Toggle-Flipflops mit zwei unabhängigen Eingangsquellen. Durch den Einsatz des E_MERGE-Bausteins können beide Eingänge gleichberechtigt den Toggle-Vorgang auslösen, was typische Anwendungsfälle wie Zweipunkt-Bedienung einer Funktion demonstriert.