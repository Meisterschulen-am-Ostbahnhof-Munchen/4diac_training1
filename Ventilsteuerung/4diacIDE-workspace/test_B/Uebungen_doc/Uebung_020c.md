# Uebung_020c: DigitalInput_I1 auf DigitalOutput_Q1; E_TON; Einschaltverzögert

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines Einschaltverzögerungstimers (E_TON) in Verbindung mit digitalen Ein- und Ausgängen. Das Programm realisiert eine verzögerte Signalweitergabe von einem digitalen Eingang zu einem digitalen Ausgang.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Liest den Zustand des digitalen Eingangs I1 ein

### E_TON
- **Typ**: E_TON (Einschaltverzögerung)
- **Parameter**:
  - PT = T#5s (Verzögerungszeit von 5 Sekunden)
- **Funktion**: Verzögert das eingehende Signal um die eingestellte Zeit

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt den Ausgangswert auf den digitalen Ausgang Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_TON.REQ
- E_TON.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_TON.IN
- E_TON.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Bei einer Zustandsänderung am digitalen Eingang I1 wird ein Ereignis an den E_TON-Baustein gesendet
2. Der E_TON-Baustein startet die Zeitverzögerung von 5 Sekunden
3. Nach Ablauf der Verzögerungszeit wird das Signal an den digitalen Ausgang Q1 weitergeleitet
4. Der Ausgang Q1 übernimmt den Zustand des Eingangs I1 mit 5 Sekunden Verzögerung

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen und Timer-Funktionen

## Zusammenfassung
Diese Übung vermittelt die praktische Anwendung eines Einschaltverzögerungstimers in der Automatisierungstechnik. Sie zeigt, wie ein digitales Eingangssignal mit einer definierten Zeitverzögerung an einen digitalen Ausgang weitergegeben werden kann. Die Verwendung des E_TON-Bausteins und die korrekte Parametrierung der Verzögerungszeit sind zentrale Lerninhalte dieser Übung.