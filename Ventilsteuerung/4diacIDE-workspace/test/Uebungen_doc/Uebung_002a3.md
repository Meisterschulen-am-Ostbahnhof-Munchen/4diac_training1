# Uebung_002a3: DigitalInput_I1/_I2 mit OR auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verarbeitung digitaler Eingangssignale mit einer ODER-Verknüpfung. Zwei digitale Eingänge werden über einen ODER-Baustein verknüpft und das Ergebnis an einem digitalen Ausgang ausgegeben.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1 / DigitalInput_I2
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE (Aktivierung des Bausteins)
  - Input = logiBUS_DI::Input_I1 (bzw. Input_I2 für I2)

### OR_2
- **Typ**: OR_2 (2-fach ODER-Verknüpfung)
- **Funktionsweise**: Verknüpft zwei Eingangssignale mit einer logischen ODER-Operation

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Aktivierung des Bausteins)
  - Output = logiBUS_DO::Output_Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → OR_2.REQ
- DigitalInput_I2.IND → OR_2.REQ
- OR_2.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → OR_2.IN1
- DigitalInput_I2.IN → OR_2.IN2
- OR_2.OUT → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Bei Änderung an DigitalInput I1 oder I2 wird ein IND-Ereignis ausgelöst
2. Das Ereignis triggert die ODER-Verknüpfung (OR_2)
3. OR_2 verarbeitet die Eingangswerte und gibt das Ergebnis aus
4. Das CNF-Ereignis von OR_2 aktiviert den DigitalOutput
5. Der berechnete ODER-Wert wird an Ausgang Q1 ausgegeben

**Lernziele:**
- Grundlegende Verknüpfung digitaler Signale
- Verwendung von Ereignis- und Datenverbindungen
- Arbeit mit Ein-/Ausgangsbausteinen
- ODER-Logik in der Steuerungstechnik

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundverständnis von logischen Verknüpfungen und 4diac-IDE

## Zusammenfassung
Diese Übung vermittelt die grundlegende Implementierung einer ODER-Verknüpfung mit digitalen Ein- und Ausgängen. Sie zeigt das Zusammenspiel von Ereignissteuerung und Datenverarbeitung in einem einfachen Steuerungsprogramm und legt die Basis für komplexere logische Verknüpfungen.