# Uebung_111: Übung zum Integer Überlauf

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert das Konzept des Integer-Überlaufs in der Automatisierungstechnik. Sie zeigt, wie durch mathematische Operationen Wertebereiche überschritten werden können und wie dies in einem Steuerungssystem behandelt wird.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktionsweise**: Erfasst digitale Eingangssignale und erkennt Einzelklick-Ereignisse

### ADD_2
- **Typ**: ADD_2
- **Parameter**:
  - IN1 = USINT#128
  - IN2 = USINT#128
- **Funktionsweise**: Führt eine Addition zweier vorzeichenloser 8-Bit-Integer-Werte durch

### F_USINT_TO_UDINT
- **Typ**: F_USINT_TO_UDINT
- **Funktionsweise**: Konvertiert vorzeichenlose 8-Bit-Integer-Werte in vorzeichenlose 32-Bit-Integer-Werte

### F_DIV
- **Typ**: F_DIV
- **Parameter**:
  - IN1 = UDINT#5000
- **Funktionsweise**: Führt eine Division durch, wobei IN1 durch IN2 geteilt wird

### F_MOVE
- **Typ**: F_MOVE
- **Attribute**:
  - DataType = UDINT
- **Funktionsweise**: Kopiert Datenwerte ohne Änderung

### F_GT
- **Typ**: F_GT
- **Parameter**:
  - IN2 = UDINT#200
- **Funktionsweise**: Vergleicht zwei Werte und gibt TRUE aus, wenn IN1 größer als IN2 ist

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert digitale Ausgänge basierend auf Eingangssignalen

## Programmablauf und Verbindungen

Der Programmablauf beginnt mit einem Tastendruck-Ereignis am digitalen Eingang I1. Dies löst folgende Ereigniskette aus:

1. **DigitalInput_CLK_I1.IND** → **ADD_2.REQ**: Startet die Addition
2. **ADD_2.CNF** → **F_USINT_TO_UDINT.REQ**: Startet die Typkonvertierung
3. **F_USINT_TO_UDINT.CNF** → **F_DIV.REQ**: Startet die Division
4. **F_DIV.CNF** → **F_MOVE.REQ**: Startet die Datenübertragung
5. **F_MOVE.CNF** → **F_GT.REQ**: Startet den Vergleich
6. **F_GT.CNF** → **DigitalOutput_Q1.REQ**: Aktiviert den Ausgang

Die Datenverbindungen transportieren die berechneten Werte durch die Verarbeitungskette:
- ADD_2.OUT → F_USINT_TO_UDINT.IN
- F_USINT_TO_UDINT.OUT → F_DIV.IN2
- F_DIV.OUT → F_MOVE.IN
- F_MOVE.OUT → F_GT.IN1
- F_GT.OUT → DigitalOutput_Q1.OUT

**Lernziele**:
- Verständnis von Integer-Überläufen bei arithmetischen Operationen
- Umgang mit verschiedenen Integer-Datentypen (USINT, UDINT)
- Typkonvertierung zwischen verschiedenen Datentypen
- Ereignisgesteuerte Programmabläufe in IEC 61499

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, Verständnis von Datentypen und arithmetischen Operationen

**Start der Übung**: Die Übung wird durch Betätigen des Tasters I1 gestartet

## Zusammenfassung
Diese Übung veranschaulicht das kritische Thema des Integer-Überlaufs in der Automatisierungstechnik. Durch die Addition von 128 + 128 entsteht ein Überlauf im USINT-Bereich (0-255), der anschließend durch Typkonvertierung und Division behandelt wird. Der Vergleich mit dem Schwellwert 200 entscheidet über die Aktivierung des digitalen Ausgangs Q1. Die Übung zeigt wichtige Konzepte der Datentypbehandlung und arithmetischen Operationen in Echtzeitsystemen.