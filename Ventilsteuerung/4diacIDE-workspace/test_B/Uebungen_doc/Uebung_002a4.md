# Uebung_002a4: DigitalInput_I1/_I2 mit AND_BOOL auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung digitaler Eingangssignale mit einer logischen UND-Verknüpfung. Zwei digitale Eingänge werden über einen AND-Baustein verknüpft und das Ergebnis an einen digitalen Ausgang ausgegeben.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1 / DigitalInput_I2
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_I1 / logiBUS_DI::Input_I2 (physikalische Eingangsadressen)
- **Ereignisausgang**: IND (Input Data Event)
- **Datenaustgang**: IN (Eingangswert)

### AND_2_BOOL
- **Typ**: AND_2_BOOL
- **Ereigniseingang**: REQ (Request Event)
- **Ereignisausgang**: CNF (Confirm Event)
- **Dateneingänge**: IN1, IN2 (zwei boolesche Eingänge)
- **Datenausgang**: OUT (Ergebnis der UND-Verknüpfung)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (physikalische Ausgangsadresse)
- **Ereigniseingang**: REQ (Request Event)
- **Dateneingang**: OUT (Ausgangswert)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → AND_2_BOOL.REQ
- DigitalInput_I2.IND → AND_2_BOOL.REQ
- AND_2_BOOL.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → AND_2_BOOL.IN1
- DigitalInput_I2.IN → AND_2_BOOL.IN2
- AND_2_BOOL.OUT → DigitalOutput_Q1.OUT

**Lernziele:**
- Grundlegende Verknüpfung digitaler Eingänge
- Verwendung von UND-Logikbausteinen
- Ereignisgesteuerte Datenverarbeitung
- Anbindung an physikalische Ein-/Ausgänge

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, digitale Logik

**Starten der Übung**: Die Übung wird automatisch gestartet, sobald das System initialisiert ist. Die Eingänge I1 und I2 müssen extern gesetzt werden, um den Ausgang Q1 zu aktivieren.

## Zusammenfassung
Diese Übung zeigt eine grundlegende UND-Verknüpfung zweier digitaler Eingänge. Nur wenn beide Eingänge (I1 und I2) aktiv sind, wird der Ausgang Q1 aktiviert. Die Übung vermittelt essentielle Konzepte der ereignisgesteuerten Automatisierungstechnik und logischen Verknüpfungen in 4diac-IDE.