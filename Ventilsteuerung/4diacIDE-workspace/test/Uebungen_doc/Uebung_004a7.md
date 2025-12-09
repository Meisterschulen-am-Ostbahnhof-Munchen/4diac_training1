# Uebung_004a7: SR und T-Flip-Flop mit IE und E_REND (Rendezvous)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines T-Flip-Flops in Kombination mit einem Rendezvous-Mechanismus. Die Schaltung verwendet drei digitale Eingänge und einen digitalen Ausgang, um das Verhalten eines T-Flip-Flops mit Set/Reset-Funktionalität zu zeigen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1, DigitalInput_CLK_I2, DigitalInput_CLK_I3
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 / Input_I2 / Input_I3
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_REND
- **Typ**: E_REND (Rendezvous-Baustein)

### E_T_FF
- **Typ**: E_T_FF_SR (T-Flip-Flop mit Set/Reset)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_REND.EI1
- DigitalInput_CLK_I2.IND → E_REND.EI2
- DigitalInput_CLK_I3.IND → E_REND.R
- E_REND.EO → E_T_FF.CLK
- DigitalInput_CLK_I3.IND → E_T_FF.R
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Funktionsweise:**
Das Rendezvous-Element (E_REND) wartet auf gleichzeitige Ereignisse von beiden Eingängen I1 und I2. Erst wenn beide Taster gleichzeitig betätigt werden, gibt E_REND ein Ereignis an den Takt-Eingang (CLK) des T-Flip-Flops weiter. Eingang I3 dient als Reset für beide Bausteine (E_REND und E_T_FF). Der T-Flip-Flop ändert seinen Zustand bei jedem Taktimpuls und steuert den digitalen Ausgang Q1.

**Lernziele:**
- Verständnis von T-Flip-Flop Verhalten
- Anwendung von Rendezvous-Mechanismen
- Umgang mit digitalen Ein- und Ausgängen
- Synchronisation von Ereignissen

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der digitalen Schaltungstechnik, Funktionsbausteine in 4diac

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines T-Flip-Flops mit Rendezvous-Synchronisation. Die Schaltung demonstriert, wie mehrere Eingangsereignisse synchronisiert werden müssen, um einen Zustandswechsel im Flip-Flop auszulösen, während ein separater Reset-Eingang beide Bausteine zurücksetzen kann.