# Uebung_095: Beispiel für E_SELECT

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_SELECT-Funktionsbausteins in Kombination mit einem Toggle-Flipflop (E_T_FF). Die Schaltung ermöglicht die Steuerung eines Ausgangssignals über verschiedene Eingangsereignisse.

## Verwendete Funktionsbausteine (FBs)

### E_SELECT
- **Typ**: E_SELECT
- **Funktionsweise**: Wählt zwischen zwei Eingangsereignissen (EI0 und EI1) basierend auf dem G-Dateneingang. Bei G=0 wird EI0 durchgeschaltet, bei G=1 wird EI1 durchgeschaltet.

### E_T_FF
- **Typ**: E_T_FF
- **Funktionsweise**: Ein Toggle-Flipflop, das seinen Ausgangszustand bei jedem ankommenden Takt-Event (CLK) umschaltet.

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### DigitalInput_CLK_I3
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I3
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I2.IND → E_SELECT.EI0
- DigitalInput_CLK_I3.IND → E_SELECT.EI1
- E_SELECT.EO → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_SELECT.G
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Funktionsweise:**
Der E_SELECT-Baustein wählt zwischen zwei Tastereingängen (I2 und I3) basierend auf dem Zustand von Eingang I1. Bei I1=0 werden Ereignisse von I2 durchgeschaltet, bei I1=1 werden Ereignisse von I3 durchgeschaltet. Die ausgewählten Ereignisse steuern den Toggle-Flipflop (E_T_FF), der bei jedem Ereignis seinen Ausgangszustand umschaltet und damit die Ausgangslampe Q1 ein- bzw. ausschaltet.

**Lernziele:**
- Verständnis des E_SELECT-Funktionsbausteins
- Anwendung von Toggle-Flipflops
- Kombination von Ereignis- und Datenflusssteuerung
- Praktische Umsetzung mit logiBUS-Komponenten

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung des E_SELECT-Bausteins zur Ereignisauswahl in Kombination mit einem Toggle-Flipflop. Die Schaltung ermöglicht die Steuerung eines Ausgangssignals über zwei verschiedene Taster, wobei ein zusätzlicher Eingang die Auswahl zwischen den beiden Tastern bestimmt.