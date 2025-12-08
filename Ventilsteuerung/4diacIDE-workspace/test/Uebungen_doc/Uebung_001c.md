# Uebung_001c: DigitalInput_I1 auf DigitalOutput_Q1 --&gt; Eingang abfragen bei Boot.

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung eines digitalen Eingangs mit einem digitalen Ausgang in der 4diac-IDE. Das System liest den Zustand eines digitalen Eingangs und gibt diesen direkt an einen digitalen Ausgang weiter.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_I1 (Zuweisung zum physischen Eingang I1)
- **Ereigniseingänge**: REQ, INITO
- **Ereignisausgänge**: IND, CNF
- **Dateneingänge**: -
- **Datenausgänge**: IN

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zuweisung zum physischen Ausgang Q1)
- **Ereigniseingänge**: REQ
- **Ereignisausgänge**: -
- **Dateneingänge**: OUT
- **Datenausgänge**: -

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → DigitalOutput_Q1.REQ (Auslösung bei Eingangsänderung)
- DigitalInput_I1.INITO → DigitalInput_I1.REQ (Initialisierungs-Schleife)
- DigitalInput_I1.CNF → DigitalOutput_Q1.REQ (Bestätigung der Eingabe)

**Datenverbindung:**
- DigitalInput_I1.IN → DigitalOutput_Q1.OUT (direkte Datenübertragung)

**Lernziele:**
- Grundlegende Verknüpfung von Ein- und Ausgängen
- Verständnis der Ereignissteuerung in IEC 61499
- Umgang mit logiBUS-Schnittstellenbausteinen
- Initialisierungsprozesse bei Systemstart

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis digitaler Ein- und Ausgänge
- Basiswissen IEC 61499-Funktionsbausteine

**Starten der Übung:**
Das Programm wird automatisch beim Booten des Systems initialisiert und überwacht kontinuierlich den Zustand des digitalen Eingangs I1.

## Zusammenfassung
Diese Übung zeigt eine grundlegende E/A-Verknüpfung, bei der ein digitaler Eingangswert direkt an einen digitalen Ausgang weitergeleitet wird. Der Schwerpunkt liegt auf der Initialisierung und kontinuierlichen Überwachung des Eingangszustands, wobei alle Änderungen sofort an den Ausgang propagiert werden.