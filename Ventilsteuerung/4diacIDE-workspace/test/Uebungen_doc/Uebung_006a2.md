# Uebung_006a2: 2x SR und T-Flip-Flop mit IE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert den Einsatz von T-Flip-Flops mit Set/Reset-Funktionalität in Kombination mit digitalen Ein- und Ausgängen. Das System verwendet zwei unabhängige T-Flip-Flop-Schaltungen, die über Eingabebuttons gesteuert werden können.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_CLK_I1**, **DigitalInput_CLK_I2**, **DigitalInput_CLK_I3**: logiBUS_IE
- **E_T_FF_SR_Q1**, **E_T_FF_SR_Q2**: E_T_FF_SR
- **DigitalOutput_Q1**, **DigitalOutput_Q2**: logiBUS_QX

### Sub-Bausteine: E_T_FF_SR
- **Typ**: T-Flip-Flop mit Set/Reset-Funktionalität
- **Verwendete interne FBs**: Nicht in der bereitgestellten Datei spezifiziert
- **Funktionsweise**: Der Baustein arbeitet als Toggle-Flip-Flop, der bei jedem Taktimpuls seinen Zustand wechselt. Zusätzlich verfügt er über eine Reset-Funktion.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF_SR_Q1.CLK (Takt für Flip-Flop 1)
- DigitalInput_CLK_I2.IND → E_T_FF_SR_Q2.CLK (Takt für Flip-Flop 2)
- DigitalInput_CLK_I3.IND → E_T_FF_SR_Q1.R und E_T_FF_SR_Q2.R (gemeinsamer Reset)
- E_T_FF_SR_Q1.EO → DigitalOutput_Q1.REQ
- E_T_FF_SR_Q2.EO → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- E_T_FF_SR_Q1.Q → DigitalOutput_Q1.OUT
- E_T_FF_SR_Q2.Q → DigitalOutput_Q2.OUT

**Parameterkonfiguration:**
- Alle DigitalInput-Bausteine sind mit BUTTON_SINGLE_CLICK konfiguriert
- Die Ausgänge sind auf logiBUS_DO::Output_Q1 und Output_Q2 gemappt
- QI-Parameter sind auf TRUE gesetzt für korrekte Initialisierung

**Lernziele:**
- Verständnis von T-Flip-Flop-Verhalten
- Umgang mit digitalen Ein- und Ausgängen
- Implementierung von Reset-Funktionalität
- Parallelbetrieb mehrerer Flip-Flop-Schaltungen

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen digitaler Schaltungen, IEC 61499, 4diac-IDE

## Zusammenfassung
Die Übung 006a2 zeigt eine praktische Anwendung von T-Flip-Flops in einer industriellen Steuerungsumgebung. Durch die Verwendung von drei unabhängigen Eingabetastern können zwei Flip-Flop-Schaltungen separat getaktet und gemeinsam zurückgesetzt werden. Die Ausgangszustände werden auf digitale Ausgänge geschaltet, was typische Szenarien in der Automatisierungstechnik abbildet.