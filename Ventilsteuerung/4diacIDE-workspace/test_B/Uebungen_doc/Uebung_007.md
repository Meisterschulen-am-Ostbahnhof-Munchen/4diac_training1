# Uebung_007: Blinker mit E_CYCLE und E_T_FF

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Blinkersystems unter Verwendung von zyklischen Ereignissen und einem Toggle-Flipflop. Das System erzeugt eine periodische Ausgabe, die zwischen zwei Zuständen wechselt.

## Verwendete Funktionsbausteine (FBs)

### E_CYCLE
- **Typ**: E_CYCLE (Zyklusgeber)
- **Parameter**: DT = T#1s (Zykluszeit von 1 Sekunde)
- **Funktionsweise**: Generiert in regelmäßigen Abständen Ereignisse am Ausgang EO. Die Zykluszeit beträgt 1 Sekunde.

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flipflop)
- **Funktionsweise**: Wechselt bei jedem eingehenden Ereignis am CLK-Eingang den Zustand des Q-Ausgangs zwischen TRUE und FALSE.

### DigitalOutput_Q1
- **Typ**: logiBUS_QX (Digitaler Ausgang)
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zugewiesener Hardware-Ausgang)
- **Funktionsweise**: Setzt den physischen Ausgang Q1 entsprechend dem Wert am Daten-Eingang OUT, wenn ein REQ-Ereignis eintrifft.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_CYCLE.EO → E_T_FF.CLK
- E_T_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Der E_CYCLE-Baustein generiert alle 1 Sekunde ein Ereignis
2. Dieses Ereignis triggert den CLK-Eingang des E_T_FF
3. Der E_T_FF wechselt seinen Ausgangszustand Q bei jedem Ereignis
4. Bei jedem Zustandswechsel wird ein REQ-Ereignis an DigitalOutput_Q1 gesendet
5. DigitalOutput_Q1 setzt den physischen Ausgang Q1 entsprechend dem Q-Wert

**Lernziele:**
- Verständnis von zyklischen Ereignisgebern
- Funktionsweise von Toggle-Flipflops
- Kombination von Ereignis- und Datenverbindungen
- Ansteuerung von physischen Ausgängen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen über Funktionsbausteine

**Starten der Übung**: Nach dem Laden der Anwendung wird der Blinker automatisch gestartet und die Ausgabe Q1 beginnt mit einer Frequenz von 0,5 Hz zu blinken.

## Zusammenfassung
Diese Übung zeigt ein einfaches Blinkersystem, das mit drei grundlegenden Funktionsbausteinen realisiert wird. Der E_CYCLE-Baustein erzeugt die Zeitbasis, der E_T_FF generiert das Taktsignal und der logiBUS_QX-Baustein steuert den physischen Ausgang an. Die Übung vermittelt wichtige Konzepte der Ereignisverarbeitung und Zustandssteuerung in IEC 61499-Systemen.