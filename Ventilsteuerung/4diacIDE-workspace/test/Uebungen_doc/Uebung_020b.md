# Uebung_020b: DigitalInput_I1 auf DigitalOutput_Q1; TON Einschaltverzögert; aufgelöst

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung einer einschaltverzögerten Steuerung mit einem TON-Baustein (Timer On-Delay). Das Programm verarbeitet ein digitales Eingangssignal und gibt es nach einer definierten Verzögerungszeit an den Ausgang weiter.

## Verwendete Funktionsbausteine (FBs)

### logiBUS_IX (DigitalInput_I1)
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Liest den digitalen Eingang I1 des logiBUS Systems

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt auf den digitalen Ausgang Q1 des logiBUS Systems

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktion**: Schalter-Baustein zur Verteilung von Ereignissen basierend auf dem Eingangssignal

### E_DELAY
- **Typ**: E_DELAY
- **Parameter**:
  - DT = T#2S (2 Sekunden Verzögerung)
- **Funktion**: Timer-Baustein für die Einschaltverzögerung

### E_RS
- **Typ**: E_RS
- **Funktion**: RS-Flipflop zur Speicherung des Zustands

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_SWITCH.EI
- E_SWITCH.EO1 → E_DELAY.START
- E_SWITCH.EO0 → E_DELAY.STOP
- E_SWITCH.EO0 → E_RS.R
- E_DELAY.EO → E_RS.S
- E_RS.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_SWITCH.G
- E_RS.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Beim Betätigen des Eingangs I1 wird das Signal an E_SWITCH weitergeleitet
2. E_SWITCH leitet das Ereignis über EO1 an E_DELAY weiter und startet den Timer
3. Nach Ablauf der 2-Sekunden-Verzögerung gibt E_DELAY ein Ereignis an E_RS.S aus
4. E_RS setzt den Ausgang Q und triggert DigitalOutput_Q1
5. Beim Loslassen von I1 wird über E_SWITCH.EO0 der Timer gestoppt und E_RS zurückgesetzt

**Lernziele:**
- Verständnis von einschaltverzögerten Schaltungen
- Anwendung von Timer-Bausteinen (TON)
- Einsatz von RS-Flipflops zur Zustandsspeicherung
- Verarbeitung digitaler Ein- und Ausgänge

**Schwierigkeitsgrad**: Einsteiger
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Ein-/Ausgänge

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung einer einschaltverzögerten Steuerung mit einer Verzögerungszeit von 2 Sekunden. Der Ausgang Q1 wird erst aktiviert, nachdem der Eingang I1 für mindestens 2 Sekunden aktiv war. Die Lösung verwendet Standard-Funktionsbausteine für Ereignisverarbeitung, Zeitverzögerung und Zustandsspeicherung.