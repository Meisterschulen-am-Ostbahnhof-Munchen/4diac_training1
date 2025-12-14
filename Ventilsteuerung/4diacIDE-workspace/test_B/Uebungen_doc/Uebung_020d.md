# Uebung_020d: DigitalInput_I1 auf DigitalOutput_Q1; TOF Ausschaltverzögert; aufgelöst

* * * * * * * * * *
## Einleitung
Diese Übung demonstriert die Verwendung einer ausschaltverzögerten Zeitfunktion (TOF - Time Off Delay) in Verbindung mit digitalen Ein- und Ausgängen. Das Programm verarbeitet ein digitales Eingangssignal und gibt es mit einer Ausschaltverzögerung von 2 Sekunden an einen digitalen Ausgang weiter.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktion**: Liest den Zustand des digitalen Eingangs I1 ein

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Schreibt den Ausgangswert auf den digitalen Ausgang Q1

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktion**: Schalter-Baustein, der das Eingangssignal auf verschiedene Ausgänge verteilt

### E_RS
- **Typ**: E_RS
- **Funktion**: RS-Flipflop zur Speicherung des Schaltzustands

### E_DELAY
- **Typ**: E_DELAY
- **Parameter**:
  - DT = T#2S (2 Sekunden Verzögerung)
- **Funktion**: Zeitverzögerungsbaustein für die Ausschaltverzögerung

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_SWITCH.EI
- E_RS.EO → DigitalOutput_Q1.REQ
- E_SWITCH.EO1 → E_RS.S
- E_SWITCH.EO0 → E_DELAY.START
- E_DELAY.EO → E_RS.R
- E_SWITCH.EO1 → E_DELAY.STOP

**Datenverbindungen:**
- DigitalInput_I1.IN → E_SWITCH.G
- E_RS.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Beim Betätigen des Eingangs I1 wird das Signal über E_SWITCH an den Setz-Eingang (S) des RS-Flipflops (E_RS) weitergeleitet
2. Das RS-Flipflop setzt den Ausgang Q1 sofort auf HIGH
3. Beim Loslassen des Eingangs I1 startet die Zeitverzögerung (E_DELAY) mit 2 Sekunden
4. Nach Ablauf der 2 Sekunden wird der Reset-Eingang (R) des RS-Flipflops aktiviert
5. Das RS-Flipflop setzt den Ausgang Q1 auf LOW zurück

**Lernziele:**
- Verständnis der ausschaltverzögerten Zeitfunktion (TOF)
- Anwendung von RS-Flipflops zur Zustandsspeicherung
- Verarbeitung digitaler Ein- und Ausgangssignale
- Zeitgesteuerte Schaltvorgänge

**Schwierigkeitsgrad**: Einsteiger
**Benötigte Vorkenntnisse**: Grundlagen der digitalen Schaltungen, Verständnis von Zeitfunktionen

## Zusammenfassung
Diese Übung zeigt die praktische Implementierung einer ausschaltverzögerten Schaltung mit einer Verzögerungszeit von 2 Sekunden. Der Ausgang Q1 bleibt nach dem Loslassen des Eingangs I1 für weitere 2 Sekunden aktiv, bevor er automatisch abschaltet. Dieses Verhalten ist typisch für TOF-Funktionen und findet in der Praxis häufig Anwendung, z.B. bei Beleuchtungssteuerungen oder Sicherheitsschaltungen.