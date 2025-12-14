# Uebung_020e: DigitalInput_I1 auf DigitalOutput_Q1; E_TOF; Ausschaltverzögert

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines ausschaltverzögerten Zeitglieds (E_TOF) in der 4diac-IDE. Ein digitaler Eingangssignal wird über einen Zeitbaustein verzögert und an einen digitalen Ausgang weitergeleitet.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktionsweise**: Liest den digitalen Eingang I1 des logiBUS-Systems aus

### E_TOF
- **Typ**: E_TOF (Ausschaltverzögerung)
- **Parameter**: 
  - PT = T#5s (Verzögerungszeit von 5 Sekunden)
- **Funktionsweise**: Verzögert das Ausschaltsignal um die eingestellte Zeit von 5 Sekunden

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**: 
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Schreibt das Signal auf den digitalen Ausgang Q1 des logiBUS-Systems

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_TOF.REQ
- E_TOF.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_TOF.IN
- E_TOF.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Beim Betätigen des digitalen Eingangs I1 wird sofort das Signal an den Ausgang Q1 weitergeleitet
2. Beim Loslassen des Eingangs I1 bleibt der Ausgang Q1 für weitere 5 Sekunden aktiv
3. Nach Ablauf der 5-Sekunden-Verzögerung schaltet der Ausgang Q1 ab

**Lernziele:**
- Verständnis der Ausschaltverzögerung (E_TOF)
- Anwendung von Zeitbausteinen in Steuerungsprogrammen
- Verbindung von Ein-/Ausgängen mit Zeitfunktionen

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen

## Zusammenfassung
Diese Übung zeigt die praktische Anwendung eines ausschaltverzögerten Zeitglieds in einem Steuerungsprogramm. Der E_TOF-Baustein sorgt dafür, dass ein Ausgangssignal nach dem Abschalten des Eingangssignals für eine definierte Zeit (hier 5 Sekunden) aktiv bleibt, bevor es endgültig abschaltet.