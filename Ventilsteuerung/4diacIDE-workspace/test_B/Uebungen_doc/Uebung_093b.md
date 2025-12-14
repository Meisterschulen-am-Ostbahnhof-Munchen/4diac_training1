# Uebung_093b: Beispiel für E_N_TABLE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_N_TABLE-Funktionsbausteins zur zeitgesteuerten Ereignisausgabe. Ein Taster-Eingang löst eine Sequenz von vier zeitverzögerten Ereignissen aus, die jeweils einen Flip-Flop-Baustein ansteuern und damit digitale Ausgänge schalten.

## Verwendete Funktionsbausteine (FBs)

### E_N_TABLE (E_TABLE)
- **Typ**: E_N_TABLE
- **Parameter**:
  - DT = [T#0s, T#2s, T#3s, T#4s]
  - N = 4
- **Funktionsweise**: Gibt nach einem START-Ereignis vier Ausgangsereignisse zu den definierten Zeitpunkten aus (0s, 2s, 3s und 4s nach Start)

### logiBUS_IE (DigitalInput_CLK_I1)
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfasst Taster-Ereignisse von einem digitalen Eingang

### E_T_FF (E_T_FF_Q1, E_T_FF_Q2, E_T_FF_Q3, E_T_FF_Q4)
- **Typ**: E_T_FF (Toggle-Flip-Flop)
- **Funktionsweise**: Schaltet den Ausgang Q bei jedem CLK-Ereignis um

### logiBUS_QX (DigitalOutput_Q1, Q2, Q3, Q4)
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1/Q2/Q3/Q4
- **Funktionsweise**: Steuert digitale Ausgänge an

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_TABLE.START (Taster löst Ereignistabelle aus)
- E_TABLE.EO0 → E_T_FF_Q1.CLK (sofort nach Tastendruck)
- E_TABLE.EO1 → E_T_FF_Q2.CLK (2s nach Tastendruck)
- E_TABLE.EO2 → E_T_FF_Q3.CLK (3s nach Tastendruck)
- E_TABLE.EO3 → E_T_FF_Q4.CLK (4s nach Tastendruck)
- E_T_FF_Q1.EO → DigitalOutput_Q1.REQ
- E_T_FF_Q2.EO → DigitalOutput_Q2.REQ
- E_T_FF_Q3.EO → DigitalOutput_Q3.REQ
- E_T_FF_Q4.EO → DigitalOutput_Q4.REQ

**Datenverbindungen:**
- E_T_FF_Qx.Q → DigitalOutput_Qx.OUT (Flip-Flop-Ausgänge zu digitalen Ausgängen)

**Lernziele:**
- Verständnis der E_N_TABLE-Funktionalität
- Umgang mit zeitgesteuerten Ereignissequenzen
- Anwendung von Toggle-Flip-Flops
- Verknüpfung von Ereignis- und Datenverbindungen

**Schwierigkeitsgrad**: Mittel

**Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignisverarbeitung

**Starten der Übung**: Die Übung wird durch Betätigen des Tasters I1 gestartet, was die Ereignissequenz auslöst.

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung des E_N_TABLE-Bausteins zur Erzeugung zeitlich versetzter Ereignisse. Die definierte Zeitsequenz [0s, 2s, 3s, 4s] sorgt für eine gestaffelte Aktivierung von vier digitalen Ausgängen über Toggle-Flip-Flops. Die Gesamtlaufzeit der Sequenz beträgt 9 Sekunden ab Tastendruck.