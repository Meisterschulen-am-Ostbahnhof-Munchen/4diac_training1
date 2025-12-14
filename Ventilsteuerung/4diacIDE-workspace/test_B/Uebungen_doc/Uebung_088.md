# Uebung_088: Beispiel für E_F_TRIG

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert den Einsatz des E_F_TRIG-Funktionsbausteins (Falling-Edge-Trigger) in Kombination mit verschiedenen Event- und Logikbausteinen. Die Anwendung zeigt das Verhalten bei fallenden Flanken und vergleicht dies mit alternativen Schaltmethoden.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalOutput_Q1/Q2** (Typ: logiBUS_QX) - Digitale Ausgänge für Aktoren
- **DigitalInput_I1/I2** (Typ: logiBUS_IX) - Digitale Eingänge für Sensoren
- **AND_2** (Typ: AND_2) - Logisches UND-Gatter mit zwei Eingängen
- **E_F_TRIG** (Typ: E_F_TRIG) - Falling-Edge-Trigger
- **E_T_FF_Q1/1_Q2** (Typ: E_T_FF) - Toggle-Flipflops
- **E_SWITCH** (Typ: E_SWITCH) - Event-Switch

## Programmablauf und Verbindungen

### Signalfluss:
1. Die digitalen Eingänge I1 und I2 liefern Signale an das AND-Gatter
2. Das AND-Gatter erzeugt ein Ausgangssignal nur wenn beide Eingänge aktiv sind
3. Parallel werden zwei Signalpfade verarbeitet:
   - **Pfad 1 (Q1)**: AND-Ausgang → E_F_TRIG (fallende Flanke) → Toggle-FF → Ausgang Q1
   - **Pfad 2 (Q2)**: AND-Ausgang → E_SWITCH → Toggle-FF → Ausgang Q2

### Besondere Merkmale:
- **E_F_TRIG** reagiert ausschließlich auf fallende Flanken des Eingangssignals
- **E_SWITCH** schaltet bei jedem eingehenden Event, unabhängig von der Flanke
- Zwei parallele Signalpfade ermöglichen den Vergleich der unterschiedlichen Schaltverhalten

### Konfiguration:
- Alle logiBUS-Bausteine sind mit QI="TRUE" initialisiert
- Spezifische Hardware-Zuordnungen für Ein- und Ausgänge sind konfiguriert

## Zusammenfassung
Diese Übung veranschaulicht den wichtigen Unterschied zwischen flankengesteuerten und eventbasierten Schaltvorgängen. Der E_F_TRIG-Baustein gewährleistet eine zuverlässige Erkennung fallender Flanken, während der E_SWITCH-Baustein bei jedem Event schaltet. Die parallele Anordnung beider Pfade ermöglicht einen direkten Vergleich der Schaltverhalten und zeigt die spezifischen Einsatzgebiete der verschiedenen Trigger-Methoden.