# Uebung_004a6: Toggle Flip-Flop mit IE und E_REND (Rendezvous)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle Flip-Flops in Kombination mit einem Rendezvous-Mechanismus. Die Schaltung verwendet digitale Eingänge und Ausgänge sowie spezielle Ereignisbausteine zur Synchronisation.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1, DigitalInput_CLK_I2, DigitalInput_CLK_I3
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 / Input_I2 / Input_I3
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### E_REND
- **Typ**: E_REND (Rendezvous-Baustein)
- **Funktionsweise**: Synchronisiert eingehende Ereignisse und gibt erst ein Ausgangsereignis aus, wenn bestimmte Bedingungen erfüllt sind

### E_T_FF
- **Typ**: E_T_FF (Toggle Flip-Flop)
- **Funktionsweise**: Ändert seinen Ausgangszustand bei jedem eingehenden Takt-Ereignis

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
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Die drei digitalen Eingänge (I1, I2, I3) erfassen Tastendruck-Ereignisse
2. E_REND synchronisiert die Ereignisse von I1 und I2
3. I3 dient als Reset-Signal für den Rendezvous-Baustein
4. Bei erfolgreicher Synchronisation gibt E_REND ein Takt-Signal an den Toggle Flip-Flop
5. Der Toggle Flip-Flop ändert seinen Ausgangszustand bei jedem Taktimpuls
6. Der Ausgangszustand wird an die digitale Ausgangsleitung Q1 weitergeleitet

**Lernziele:**
- Verständnis von Toggle Flip-Flop Funktionalität
- Implementierung von Rendezvous-Synchronisation
- Umgang mit digitalen Ein- und Ausgängen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundkenntnisse in IEC 61499, digitale Schaltungen, Ereignisverarbeitung

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung eines Toggle Flip-Flops in Verbindung mit einem Rendezvous-Mechanismus. Die Schaltung demonstriert, wie mehrere Eingangssignale synchronisiert werden können, um einen zuverlässigen Takt für einen Flip-Flop zu generieren. Die Übung vermittelt wichtige Konzepte der ereignisgesteuerten Automatisierungstechnik und Synchronisationsmechanismen.