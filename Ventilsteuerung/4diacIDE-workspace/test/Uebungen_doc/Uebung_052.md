# Uebung_052: DigitalInput_I1-_I4 auf DigitalOutput_Q1-_Q4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren Weiterleitung an digitale Ausgänge unter Verwendung von Strukturdatentypen. Die Übung zeigt die Verbindung zwischen physischen Ein-/Ausgängen und deren logischer Verarbeitung in einem Steuerungssystem.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1, DigitalInput_I2, DigitalInput_I3, DigitalInput_I4
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1 bis Input_I4
- **Funktion**: Lesen digitaler Eingangssignale von den entsprechenden Hardware-Eingängen

### DigitalOutput_Q4
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreiben eines digitalen Ausgangssignals auf den Hardware-Ausgang

### STRUCT_MUX
- **Typ**: STRUCT_MUX
- **Parameter**:
  - B_00, B_01, B_02, B_03 (BIT-Werte)
- **StructuredType**: ST04B
- **Funktion**: Multiplexen einzelner BIT-Werte in eine strukturierte Datentyp

### GET_STRUCT_VALUE
- **Typ**: GET_STRUCT_VALUE
- **Parameter**:
  - member = 'B_00'
- **Funktion**: Extrahieren eines spezifischen Members aus einer strukturierten Datentyp

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Alle DigitalInput-FBs senden ihr IND-Ereignis an STRUCT_MUX.REQ
- STRUCT_MUX.CNF triggert GET_STRUCT_VALUE.REQ
- GET_STRUCT_VALUE.CNF aktiviert DigitalOutput_Q4.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → STRUCT_MUX.B_00
- DigitalInput_I2.IN → STRUCT_MUX.B_01
- DigitalInput_I3.IN → STRUCT_MUX.B_02
- DigitalInput_I4.IN → STRUCT_MUX.B_03
- STRUCT_MUX.OUT → GET_STRUCT_VALUE.in_struct
- GET_STRUCT_VALUE.output → DigitalOutput_Q4.OUT

**Programmablauf:**
1. Bei Änderung eines digitalen Eingangssignals wird das IND-Ereignis ausgelöst
2. STRUCT_MUX sammelt alle vier Eingangssignale in einer ST04B-Struktur
3. GET_STRUCT_VALUE extrahiert das Bit B_00 aus der Struktur
4. Der extrahierte Wert wird an den digitalen Ausgang Q1 weitergeleitet

**Lernziele:**
- Verständnis der Verbindung zwischen Hardware-Ein-/Ausgängen und logischen FBs
- Arbeit mit strukturierten Datentypen
- Verwendung von Multiplexing und Struktur-Extraktion
- Ereignisgesteuerte Programmabläufe

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Signalverarbeitung in Automatisierungssystemen. Sie zeigt, wie digitale Eingangssignale erfasst, in strukturierte Datentypen zusammengefasst und selektiv an Ausgänge weitergeleitet werden können. Die Übung bildet eine Basis für komplexere Steuerungsaufgaben mit strukturierten Daten und ereignisgesteuerten Abläufen.