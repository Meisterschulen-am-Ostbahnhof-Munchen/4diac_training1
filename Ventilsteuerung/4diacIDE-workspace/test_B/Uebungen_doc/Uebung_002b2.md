# Uebung_002b2: DigitalInput_I1/_I2/_I3 auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren logische Verknüpfung zur Steuerung eines digitalen Ausgangs. Die Schaltung verknüpft drei digitale Eingänge (I1, I2, I3) über logische Operationen, um den Ausgang Q1 zu steuern.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1, DigitalInput_I2, DigitalInput_I3
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_I1 / Input_I2 / Input_I3

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

### AND_2
- **Typ**: AND_2 (2-fach UND-Verknüpfung)

### OR_2
- **Typ**: OR_2 (2-fach ODER-Verknüpfung)

### F_MOVE
- **Typ**: F_MOVE (Datenübertragungsbaustein)
- **Attribute**: DataType = BOOL

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → AND_2.REQ
- DigitalInput_I2.IND → AND_2.REQ
- DigitalInput_I3.IND → OR_2.REQ
- AND_2.CNF → F_MOVE.REQ
- F_MOVE.CNF → OR_2.REQ
- OR_2.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → AND_2.IN1
- DigitalInput_I2.IN → AND_2.IN2
- AND_2.OUT → F_MOVE.IN
- F_MOVE.OUT → OR_2.IN1
- DigitalInput_I3.IN → OR_2.IN2
- OR_2.OUT → DigitalOutput_Q1.OUT

**Logikablauf:**
1. Die Eingänge I1 und I2 werden durch eine UND-Verknüpfung (AND_2) verarbeitet
2. Das Ergebnis wird über F_MOVE an den ersten Eingang der ODER-Verknüpfung (OR_2) weitergeleitet
3. Der Eingang I3 wird direkt mit dem zweiten Eingang der ODER-Verknüpfung verbunden
4. Das Ausgangssignal der ODER-Verknüpfung steuert den digitalen Ausgang Q1

**Lernziele:**
- Verständnis logischer Verknüpfungen (UND, ODER)
- Umgang mit digitalen Ein- und Ausgängen
- Datenflusssteuerung mit F_MOVE-Baustein
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, digitale Logik

## Zusammenfassung
Diese Übung zeigt eine grundlegende logische Schaltung, die digitale Eingangssignale verarbeitet und kombiniert, um einen Ausgang zu steuern. Die Kombination aus UND- und ODER-Verknüpfungen demonstriert typische Steuerungslogiken in der Automatisierungstechnik. Der F_MOVE-Baustein sorgt für eine saubere Datenübertragung zwischen den logischen Operationen.