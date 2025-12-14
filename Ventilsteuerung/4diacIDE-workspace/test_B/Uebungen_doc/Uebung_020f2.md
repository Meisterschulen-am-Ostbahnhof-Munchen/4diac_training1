# Uebung_020f2: DigitalInput_I1 auf DigitalOutput_Q1; FB_TP; Impulsformend

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines Taktgebers (E_CYCLE) zur Steuerung eines Impulsformers (FB_TP). Ein digitaler Eingang (I1) wird über einen Impulsformer auf einen digitalen Ausgang (Q1) geschaltet, wobei der Taktgeber die Aktualisierungsrate des Impulsformers bestimmt.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Liest den digitalen Eingang I1 vom logiBUS-System

### E_SWITCH_I1
- **Typ**: E_SWITCH
- **Funktion**: Schalter für den Eingangsimpuls

### E_CYCLE
- **Typ**: E_CYCLE
- **Parameter**: DT = T#500ms
- **Funktion**: Taktgeber mit 500ms Zykluszeit

### FB_TP
- **Typ**: FB_TP
- **Parameter**: PT = T#5s
- **Funktion**: Impulsformer mit 5 Sekunden Pulszeit

### E_SWITCH_Q1
- **Typ**: E_SWITCH
- **Funktion**: Schalter für den Ausgangsimpuls

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt auf den digitalen Ausgang Q1 des logiBUS-Systems

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_CYCLE.EO → FB_TP.REQ (startet Impulsformer bei jedem Takt)
- DigitalInput_I1.IND → E_SWITCH_I1.EI (Eingangsänderung an Schalter)
- FB_TP.CNF → E_SWITCH_Q1.EI (Impulsformer-Bestätigung an Ausgangsschalter)
- E_SWITCH_I1.EO1 → E_CYCLE.START (startet Taktgeber bei Eingangsaktivierung)
- E_SWITCH_Q1.EO0 → E_CYCLE.STOP (stoppt Taktgeber bei bestimmten Bedingungen)
- FB_TP.CNF → DigitalOutput_Q1.REQ (Impulsformer-Bestätigung an Ausgang)

**Datenverbindungen:**
- DigitalInput_I1.IN → E_SWITCH_I1.G (Eingangswert an Schalter)
- DigitalInput_I1.IN → FB_TP.IN (Eingangswert an Impulsformer)
- FB_TP.Q → DigitalOutput_Q1.OUT (Impulsformer-Ausgang an physischen Ausgang)
- FB_TP.Q → E_SWITCH_Q1.G (Impulsformer-Ausgang an Ausgangsschalter)

**Lernziele:**
- Verständnis von Taktgebern und deren Konfiguration
- Anwendung von Impulsformern (FB_TP)
- Steuerung von digitalen Ein- und Ausgängen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einfach bis Mittel

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen

**Start der Übung**: Das Programm wird automatisch gestartet, sobald der digitale Eingang I1 aktiviert wird.

## Zusammenfassung
Diese Übung zeigt eine typische Anwendung eines Impulsformers in Kombination mit einem Taktgeber. Der E_CYCLE-Baustein sorgt für eine regelmäßige Aktualisierung des FB_TP, der wiederum den digitalen Ausgang Q1 basierend auf dem Eingang I1 steuert. Die Verwendung von E_SWITCH-Bausteinen ermöglicht eine flexible Steuerung des Programmablaufs.