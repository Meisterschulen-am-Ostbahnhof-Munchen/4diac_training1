# Uebung_004a9: mit E_SPLIT_3

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert den Einsatz von Toggle-Flipflops (T-FF) in Verbindung mit einem Ereignisverteiler. Die Schaltung steuert drei digitale Ausgänge über Toggle-Flipflops, die durch einen gemeinsamen Tasterimpuls getriggert werden.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_CLK_I1** (logiBUS_IE): Digitaler Eingang für Taster I1 mit Einzelklick-Erkennung
- **E_SPLIT_3**: Ereignisverteiler mit drei Ausgängen
- **E_T_FF_Q1**, **E_T_FF_Q2**, **E_T_FF_Q3** (E_T_FF): Toggle-Flipflops für drei Ausgänge
- **DigitalOutput_Q1**, **DigitalOutput_Q2**, **DigitalOutput_Q3** (logiBUS_QX): Digitale Ausgänge Q1-Q3

### Sub-Bausteine: E_T_FF (Toggle-Flipflop)
- **Typ**: Basic Function Block
- **Verwendete interne FBs**: Keine internen FBs
- **Funktionsweise**: Bei jedem eingehenden CLK-Ereignis toggelt der Q-Ausgang zwischen TRUE und FALSE. Der EO-Ausgang bestätigt die Verarbeitung.

## Programmablauf und Verbindungen

### Ereignisverbindungen:
1. DigitalInput_CLK_I1.IND → E_SPLIT_3.EI (Tasterimpuls wird an Verteiler gesendet)
2. E_SPLIT_3.EO1 → E_T_FF_Q1.CLK (Verteilerausgang 1 triggert Flipflop 1)
3. E_SPLIT_3.EO2 → E_T_FF_Q2.CLK (Verteilerausgang 2 triggert Flipflop 2)
4. E_SPLIT_3.EO3 → E_T_FF_Q3.CLK (Verteilerausgang 3 triggert Flipflop 3)
5. E_T_FF_Q1.EO → DigitalOutput_Q1.REQ (Flipflop 1 aktiviert Ausgang Q1)
6. E_T_FF_Q2.EO → DigitalOutput_Q2.REQ (Flipflop 2 aktiviert Ausgang Q2)
7. E_T_FF_Q3.EO → DigitalOutput_Q3.REQ (Flipflop 3 aktiviert Ausgang Q3)

### Datenverbindungen:
- E_T_FF_Q1.Q → DigitalOutput_Q1.OUT (Flipflop-Zustand an Ausgang Q1)
- E_T_FF_Q2.Q → DigitalOutput_Q2.OUT (Flipflop-Zustand an Ausgang Q2)
- E_T_FF_Q3.Q → DigitalOutput_Q3.OUT (Flipflop-Zustand an Ausgang Q3)

### Konfiguration:
- **DigitalInput_CLK_I1**: Input_I1 mit BUTTON_SINGLE_CLICK Event
- **DigitalOutputs**: Q1-Q3 mit aktiviertem QI-Parameter (TRUE)

**Schwierigkeitsgrad**: Einfach bis Mittel  
**Benötigte Vorkenntnisse**: Grundverständnis von Funktionsbausteinen und Ereignisverarbeitung  
**Start der Übung**: Taster I1 betätigen - bei jedem Klick werden alle drei Flipflops getoggelt

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung von Toggle-Flipflops in Verbindung mit einem Ereignisverteiler. Durch die Verwendung von E_SPLIT_3 wird ein einzelner Tasterimpuls auf drei parallele Flipflops verteilt, die unabhängig voneinander ihre Zustände ändern. Die Schaltung demonstriert effektiv die Prinzipien der Ereignisverteilung und parallelen Signalverarbeitung in IEC 61499-Systemen.