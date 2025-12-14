# Uebung_002a2: DigitalInput_I1/_I2 mit AND (alt) auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung digitaler Eingangssignale mit einer logischen UND-Verknüpfung. Zwei digitale Eingänge werden über einen AND-Baustein verknüpft und das Ergebnis an einen digitalen Ausgang ausgegeben.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1 / DigitalInput_I2
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE (Aktivierung des Bausteins)
  - Input = logiBUS_DI::Input_I1 / logiBUS_DI::Input_I2 (Hardware-Zuordnung)
- **Ereignisausgang**: IND (Input Data - Signalisiert neue Eingangsdaten)
- **Datenaustgang**: IN (Eingangswert)

### F_AND
- **Typ**: F_AND (UND-Funktionsbaustein)
- **Dateneingänge**: IN1, IN2 (zwei Eingangssignale)
- **Datenausgang**: OUT (Ergebnis der UND-Verknüpfung)
- **Ereigniseingang**: REQ (Startet die Verarbeitung)
- **Ereignisausgang**: CNF (Bestätigt die Bearbeitung)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Aktivierung des Bausteins)
  - Output = logiBUS_DO::Output_Q1 (Hardware-Zuordnung)
- **Ereigniseingang**: REQ (Anforderung zur Ausgabe)
- **Dateneingang**: OUT (Ausgabewert)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → F_AND.REQ
- DigitalInput_I2.IND → F_AND.REQ
- F_AND.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → F_AND.IN1
- DigitalInput_I2.IN → F_AND.IN2
- F_AND.OUT → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Bei Änderung an DigitalInput_I1 oder DigitalInput_I2 wird ein IND-Ereignis ausgelöst
2. Das IND-Ereignis startet die Verarbeitung im F_AND-Baustein (REQ)
3. F_AND verknüpft die beiden Eingangswerte logisch UND
4. Nach der Verarbeitung sendet F_AND ein CNF-Ereignis
5. Das CNF-Ereignis aktiviert die Ausgabe an DigitalOutput_Q1 (REQ)
6. Der berechnete Wert wird an den Ausgang Q1 ausgegeben

**Lernziele:**
- Grundlegende Verwendung digitaler Ein- und Ausgänge
- Logische Verknüpfung mit AND-Funktion
- Ereignisgesteuerte Verarbeitung in 4diac
- Hardware-Zuordnung von Ein-/Ausgängen

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Logik

## Zusammenfassung
Diese Übung vermittelt die grundlegende Funktionsweise ereignisgesteuerter Systeme in 4diac. Sie zeigt, wie digitale Eingangssignale verarbeitet, logisch verknüpft und an Ausgänge weitergeleitet werden. Die UND-Verknüpfung stellt sicher, dass der Ausgang Q1 nur aktiviert wird, wenn beide Eingänge I1 und I2 aktiv sind.