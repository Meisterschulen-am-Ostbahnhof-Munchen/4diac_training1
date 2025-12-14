# Uebung_110: Übung zum Integer Überlauf

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert das Phänomen des arithmetischen Überlaufs bei der Verwendung von Integer-Datentypen. Anhand eines praktischen Beispiels wird gezeigt, wie eine Addition zu unerwarteten Ergebnissen führen kann, wenn der Wertebereich des Datentyps überschritten wird.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Funktionsweise**: Liest digitale Eingangssignale ein und erkennt Tastendruck-Ereignisse

### ADD_2
- **Typ**: ADD_2
- **Parameter**: 
  - IN1 = USINT#200
  - IN2 = USINT#200
- **Funktionsweise**: Führt eine Addition zweier Werte durch

### F_MOVE
- **Typ**: F_MOVE
- **Datentyp**: USINT (Unsigned Short Integer)
- **Funktionsweise**: Kopiert Datenwerte ohne Änderung

### F_GT
- **Typ**: F_GT (Greater Than)
- **Parameter**: IN2 = USINT#200
- **Funktionsweise**: Vergleicht zwei Werte und gibt TRUE aus, wenn der erste Wert größer als der zweite ist

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Steuert digitale Ausgänge

## Programmablauf und Verbindungen

Das Programm wird durch einen Tastendruck am digitalen Eingang I1 gestartet. Der Ablauf erfolgt über folgende Ereignisverbindungen:

1. **DigitalInput_CLK_I1.IND** → **ADD_2.REQ**
2. **ADD_2.CNF** → **F_MOVE.REQ**
3. **F_MOVE.CNF** → **F_GT.REQ**
4. **F_GT.CNF** → **DigitalOutput_Q1.REQ**

Die Datenverbindungen transportieren die Berechnungsergebnisse:

1. **ADD_2.OUT** → **F_MOVE.IN**
2. **F_MOVE.OUT** → **F_GT.IN1**
3. **F_GT.OUT** → **DigitalOutput_Q1.OUT**

**Lernziel**: Verständnis des arithmetischen Überlaufs bei der Verwendung des USINT-Datentyps (0-255 Wertebereich)

**Schwierigkeitsgrad**: Einsteiger

**Vorkenntnisse**: Grundlagen der 4diac-IDE und Funktionsbausteine

**Start der Übung**: Durch Betätigen des Tasters am Eingang I1

## Zusammenfassung

Diese Übung verdeutlicht das wichtige Konzept des arithmetischen Überlaufs in der Programmierung. Die Addition von 200 + 200 ergibt 400, was den maximalen Wert des USINT-Datentyps (255) überschreitet und zu einem Überlauf führt. Das Ergebnis des Vergleichs mit F_GT zeigt anschaulich, wie solche Überläufe zu unerwartetem Programmverhalten führen können.