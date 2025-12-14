# Uebung_020e2: DigitalInput_I1 auf DigitalOutput_Q1; FB_TOF; Ausschaltverzögert

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Anwendung eines ausschaltverzögerten Timers (FB_TOF) in der Automatisierungstechnik. Ein digitaler Eingangssignal wird über einen Zeitgeber verzögert und an einen digitalen Ausgang weitergeleitet. Die Verzögerungszeit beträgt 5 Sekunden.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Liest den Zustand des digitalen Eingangs I1 ein

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt den Ausgangswert auf den digitalen Ausgang Q1

### FB_TOF
- **Typ**: FB_TOF
- **Parameter**:
  - PT = T#5s (Verzögerungszeit: 5 Sekunden)
- **Funktion**: Ausschaltverzögerter Timer (OFF-Delay)

### E_CYCLE
- **Typ**: E_CYCLE
- **Parameter**:
  - DT = T#500ms (Zykluszeit: 500ms)
- **Funktion**: Zyklische Ereignisgenerierung

### E_SWITCH_I1
- **Typ**: E_SWITCH
- **Funktion**: Ereignisweiche für den Eingang I1

### E_SWITCH_Q1
- **Typ**: E_SWITCH
- **Funktion**: Ereignisweiche für den Ausgang Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_SWITCH_I1.EI
- E_SWITCH_I1.EO1 → E_CYCLE.START
- E_CYCLE.EO → FB_TOF.REQ
- FB_TOF.CNF → DigitalOutput_Q1.REQ
- FB_TOF.CNF → E_SWITCH_Q1.EI
- E_SWITCH_Q1.EO0 → E_CYCLE.STOP

**Datenverbindungen:**
- DigitalInput_I1.IN → FB_TOF.IN
- DigitalInput_I1.IN → E_SWITCH_I1.G
- FB_TOF.Q → DigitalOutput_Q1.OUT
- FB_TOF.Q → E_SWITCH_Q1.G

**Programmablauf:**
1. Bei Änderung des Eingangssignals I1 wird der Zyklusgeber E_CYCLE gestartet
2. E_CYCLE sendet alle 500ms ein Ereignis an FB_TOF
3. FB_TOF aktualisiert seinen ET-Wert und gibt nach Ablauf der 5-Sekunden-Verzögerung das Signal aus
4. Das Ausgangssignal Q1 wird entsprechend dem verzögerten Eingangssignal geschaltet
5. Bei Signalwechsel wird der Zyklusgeber gestoppt

## Zusammenfassung
Diese Übung verdeutlicht die Funktionsweise eines ausschaltverzögerten Timers in Verbindung mit zyklischer Abfrage. Der E_CYCLE-Baustein sorgt für die regelmäßige Aktualisierung des Timer-Zustands, während die E_SWITCH-Bausteine die Steuerung des Zyklus basierend auf den Eingangs- und Ausgangssignalen übernehmen. Die Übung zeigt praxisnah die Anwendung von Zeitverzögerungen in der industriellen Automatisierungstechnik.