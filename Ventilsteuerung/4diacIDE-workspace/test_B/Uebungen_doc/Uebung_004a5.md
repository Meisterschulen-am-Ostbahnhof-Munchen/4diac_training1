# Uebung_004a5: wie Uebung_004a4 aber ohne E_SPLIT

* * * * * * * * * *

## Einleitung
Diese Übung baut auf der vorherigen Übung 004a4 auf, jedoch wurde der E_SPLIT-Baustein entfernt. Die Übung demonstriert die Verwendung von T-Flipflops zur Steuerung digitaler Ausgänge basierend auf Tasterereignissen.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_CLK_I1** (Typ: logiBUS_IE)
- **E_T_FF_Q1** (Typ: E_T_FF)
- **E_T_FF_Q2** (Typ: E_T_FF)
- **DigitalOutput_Q1** (Typ: logiBUS_QX)
- **DigitalOutput_Q2** (Typ: logiBUS_QX)

### Sub-Bausteine: E_T_FF (T-Flipflop)
- **Typ**: E_T_FF (Ereignisgesteuertes T-Flipflop)
- **Verwendete interne FBs**: Keine weiteren internen FBs angegeben
- **Funktionsweise**: Das T-Flipflop ändert seinen Ausgangszustand bei jedem eingehenden Taktimpuls (CLK-Ereignis). Der Ausgang Q wechselt bei jedem Takt zwischen den Zuständen TRUE und FALSE.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_T_FF_Q1.CLK
- DigitalInput_CLK_I1.IND → E_T_FF_Q2.CLK
- E_T_FF_Q1.EO → DigitalOutput_Q1.REQ
- E_T_FF_Q2.EO → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- E_T_FF_Q1.Q → DigitalOutput_Q1.OUT
- E_T_FF_Q2.Q → DigitalOutput_Q2.OUT

**Parameterkonfiguration:**
- DigitalInput_CLK_I1: InputEvent = BUTTON_SINGLE_CLICK, Input = Input_I1
- DigitalOutput_Q1: Output = Output_Q1
- DigitalOutput_Q2: Output = Output_Q2
- Alle Bausteine haben QI = TRUE aktiviert

**Lernziele:**
- Verständnis von T-Flipflops und deren Verhalten
- Umgang mit parallelen Signalverarbeitung ohne Event-Splitter
- Steuerung mehrerer Ausgänge mit gemeinsamer Eingabequelle
- Implementierung von Toggling-Funktionalität für digitale Ausgänge

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, Verständnis von Flipflops, Erfahrung mit 4diac-IDE

**Start der Übung**: Das Programm wird durch Betätigen des Tasters I1 gestartet, der einen Single-Click-Event auslöst.

## Zusammenfassung
Diese Übung zeigt die parallele Ansteuerung zweier T-Flipflops mit einem gemeinsamen Tasterereignis. Im Vergleich zur vorherigen Version wurde der E_SPLIT-Baustein entfernt, was eine direktere Verbindung zwischen Eingabe und Flipflops ermöglicht. Beide Ausgänge Q1 und Q2 werden unabhängig voneinander durch die Tasterbetätigung getoggelt, wobei jeder Ausgang seinen eigenen Zustand beibehält und unabhängig vom anderen schaltet.