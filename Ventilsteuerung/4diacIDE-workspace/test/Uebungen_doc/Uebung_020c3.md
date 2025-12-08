# Uebung_020c3: DigitalInput_I1 auf DigitalOutput_Q1; FB_TON; Einschaltverzögert

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines einschaltverzögerten Timers (FB_TON) zur Steuerung eines digitalen Ausgangs basierend auf einem digitalen Eingang. Der Funktionsbaustein FB_TON sorgt dafür, dass der Ausgang erst nach Ablauf einer definierten Verzögerungszeit aktiviert wird.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Funktion**: Liest den digitalen Eingang I1 des logiBUS Systems aus
- **Parameter**: 
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (verknüpft mit physischem Eingang I1)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Funktion**: Steuert den digitalen Ausgang Q1 des logiBUS Systems
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (verknüpft mit physischem Ausgang Q1)

### FB_TON
- **Typ**: FB_TON (Timer On-Delay)
- **Funktion**: Einschaltverzögerungstimer
- **Parameter**:
  - PT = T#5s (Verzögerungszeit von 5 Sekunden)

### E_SWITCH_I1
- **Typ**: E_SWITCH
- **Funktion**: Ereignis-Switch, der basierend auf dem Eingangssignal zwischen verschiedenen Ereignisausgängen umschaltet

### E_CYCLE
- **Typ**: E_CYCLE
- **Funktion**: Zyklischer Ereignisgenerator
- **Parameter**:
  - DT = T#500ms (Zykluszeit von 500 Millisekunden)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_SWITCH_I1.EI (Eingangsänderung löst Switch aus)
- E_SWITCH_I1.EO0 → E_CYCLE.STOP (Eingang = 0 stoppt Zyklus)
- E_SWITCH_I1.EO1 → E_CYCLE.START (Eingang = 1 startet Zyklus)
- E_CYCLE.EO → FB_TON.REQ (Zyklus aktualisiert Timer)
- FB_TON.CNF → DigitalOutput_Q1.REQ (Timer-Ergebnis steuert Ausgang)

**Datenverbindungen:**
- DigitalInput_I1.IN → FB_TON.IN (Eingangssignal an Timer)
- DigitalInput_I1.IN → E_SWITCH_I1.G (Eingangssignal steuert Switch)
- FB_TON.Q → DigitalOutput_Q1.OUT (Timer-Ausgang steuert physischen Ausgang)

**Besonderheiten:**
- Der E_CYCLE Baustein mit 500ms Zykluszeit sorgt für die regelmäßige Aktualisierung des FB_TON Timers
- Der E_SWITCH steuert basierend auf dem Eingangssignal den Start/Stop des Zyklus
- Die Verzögerungszeit des FB_TON ist auf 5 Sekunden eingestellt

## Zusammenfassung
Diese Übung zeigt die Implementierung einer einschaltverzögerten Steuerung mit einem TON-Timer. Der digitale Ausgang Q1 wird erst 5 Sekunden nach Aktivierung des digitalen Eingangs I1 eingeschaltet. Die Übung demonstriert die Zusammenarbeit von Ereignis- und Datenverbindungen sowie die Verwendung zyklischer Abfragen für Timer-Operationen in 4diac.