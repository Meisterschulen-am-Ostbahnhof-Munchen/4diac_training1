# Uebung_054: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren direkte Ausgabe auf digitale Ausgänge. Die Anwendung zeigt die grundlegende Signalverarbeitung zwischen Eingängen I1-I4 und Ausgängen Q1-Q4 unter Verwendung von Array-Konvertierungsbausteinen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput Bausteine
- **DigitalInput_I1**, **DigitalInput_I2**, **DigitalInput_I3**, **DigitalInput_I4**
  - **Typ**: logiBUS_IX
  - **Parameter**: 
    - QI = TRUE
    - Input = logiBUS_DI::Input_I1 / Input_I2 / Input_I3 / Input_I4

### DigitalOutput Bausteine  
- **DigitalOutput_Q1**, **DigitalOutput_Q2**, **DigitalOutput_Q3**, **DigitalOutput_Q4**
  - **Typ**: logiBUS_QX
  - **Parameter**:
    - QI = TRUE
    - Output = logiBUS_DO::Output_Q1 / Output_Q2 / Output_Q3 / Output_Q4

### Konvertierungsbausteine
- **BOOLS_TO_ARR08B**
  - **Typ**: BOOLS_TO_ARR08B
  - Wandelt einzelne BOOL-Signale in ein 8-Bit-Array um

- **ARR08B_TO_BOOLS**  
  - **Typ**: ARR08B_TO_BOOLS
  - Wandelt ein 8-Bit-Array zurück in einzelne BOOL-Signale

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- Die IND-Ereignisse der vier DigitalInput-Bausteine triggern BOOLS_TO_ARR08B.REQ
- BOOLS_TO_ARR08B.CNF triggert ARR08B_TO_BOOLS.REQ
- ARR08B_TO_BOOLS.CNF triggert alle vier DigitalOutput-Bausteine (REQ)

### Datenverbindungen:
- DigitalInput I1-I4 IN → BOOLS_TO_ARR08B IN_00 bis IN_03
- BOOLS_TO_ARR08B.OUT → ARR08B_TO_BOOLS.IN
- ARR08B_TO_BOOLS.OUT_00 bis OUT_03 → DigitalOutput Q1-Q4 OUT

### Lernziele:
- Verständnis der digitalen Ein-/Ausgabeverarbeitung
- Umgang mit Array-Konvertierungsbausteinen
- Ereignisgesteuerte Signalverarbeitung
- Verbindungsaufbau zwischen Funktionsbausteinen

### Schwierigkeitsgrad: 
Einfach - geeignet für Einsteiger

### Vorkenntnisse:
- Grundlagen der 4diac-IDE
- Verständnis digitaler Ein-/Ausgänge
- Basiswissen über Funktionsbausteine

### Start der Übung:
Die Übung wird automatisch gestartet, sobald die Anwendung auf einen geeigneten Laufzeitcontainer deployed wird. Die DigitalInput-Signale werden kontinuierlich verarbeitet.

## Zusammenfassung
Diese Übung zeigt eine grundlegende Signalverarbeitungskette von digitalen Eingängen zu digitalen Ausgängen. Durch die Verwendung von Array-Konvertierungsbausteinen wird demonstriert, wie einzelne BOOL-Signale effizient in Arrays zusammengefasst und wieder aufgeteilt werden können. Die Übung vermittelt essentielle Konzepte der ereignisgesteuerten Automatisierungstechnik.