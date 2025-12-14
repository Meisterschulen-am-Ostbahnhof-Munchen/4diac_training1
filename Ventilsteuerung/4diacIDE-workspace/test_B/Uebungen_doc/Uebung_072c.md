# Uebung_072c: GBSD auf UT ausgeben

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung und Ausgabe von GBSD-Daten (Ground Based Speed and Distance) auf einem UT (User Terminal). Das System verarbeitet Geschwindigkeits- und Distanzdaten von einem Boden-basierten System und berechnet daraus weitere Werte für die Ausgabe.

## Verwendete Funktionsbausteine (FBs)

### I_GBSD
- **Typ**: I_GBSD
- **Parameter**: QI = TRUE
- **Ereignisausgänge**: IND
- **Datenausgänge**: GROUNDBASEDMACHINESPEED, GROUNDBASEDMACHINEDISTANCE, timestamp_data

### Q_NumericValue_GBSD
- **Typ**: Q_NumericValue
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Ground_based_machine_speed"

### Q_NumberVariable_Wheel_based_machine_distance
- **Typ**: Q_NumericValue
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Wheel_based_machine_distance"

### INTEGRAL
- **Typ**: utils::math::INTEGRAL
- **Funktionsweise**: Führt eine Integration über Zeit durch

### OFFSET_UDINT
- **Typ**: utils::math::OFFSET_UDINT
- **Funktionsweise**: Wendet einen Offset auf UDINT-Werte an

### CYCLE_TIME
- **Typ**: utils::timing::CYCLE_TIME
- **Funktionsweise**: Berechnet die Zykluszeit

### F_UINT_TO_REAL
- **Typ**: F_UINT_TO_REAL
- **Funktionsweise**: Konvertiert UINT zu REAL

### F_REAL_TO_UDINT
- **Typ**: F_REAL_TO_UDINT
- **Funktionsweise**: Konvertiert REAL zu UDINT

### F_SUB
- **Typ**: F_SUB
- **Funktionsweise**: Führt eine Subtraktion durch

### F_UDINT_TO_LINT
- **Typ**: F_UDINT_TO_LINT
- **Funktionsweise**: Konvertiert UDINT zu LINT

### F_UDINT_TO_LINT_1
- **Typ**: F_UDINT_TO_LINT
- **Funktionsweise**: Konvertiert UDINT zu LINT

## Programmablauf und Verbindungen

**Ereignisfluss:**
1. I_GBSD.IND → Q_NumericValue_GBSD.REQ
2. I_GBSD.IND → OFFSET_UDINT.REQ
3. I_GBSD.IND → CYCLE_TIME.REQ
4. OFFSET_UDINT.CNF → Q_NumberVariable_Wheel_based_machine_distance.REQ
5. CYCLE_TIME.CNF → F_UINT_TO_REAL.REQ
6. F_UINT_TO_REAL.CNF → INTEGRAL.REQ
7. INTEGRAL.CNF → F_REAL_TO_UDINT.REQ
8. F_REAL_TO_UDINT.CNF → F_UDINT_TO_LINT_1.REQ
9. OFFSET_UDINT.CNF → F_UDINT_TO_LINT.REQ
10. F_UDINT_TO_LINT_1.CNF → F_SUB.REQ

**Datenfluss:**
- Geschwindigkeitsdaten werden direkt ausgegeben und für Integration verwendet
- Distanzdaten werden mit Offset verarbeitet und ausgegeben
- Zeitstempel werden für Zykluszeitberechnung genutzt
- Integrierte Werte werden konvertiert und für Subtraktion vorbereitet

**Lernziele:**
- Verarbeitung von GBSD-Daten
- Verwendung von mathematischen Operationen (Integration, Subtraktion)
- Datentyp-Konvertierungen
- Zeitbasierte Berechnungen
- Ausgabe von Prozessdaten auf UT

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Datenfluss

## Zusammenfassung
Diese Übung zeigt ein komplexes Datenverarbeitungssystem für GBSD-Daten, das verschiedene mathematische Operationen, Datentyp-Konvertierungen und zeitbasierte Berechnungen kombiniert. Das System verarbeitet sowohl Geschwindigkeits- als auch Distanzdaten und gibt diese nach entsprechender Verarbeitung auf dem User Terminal aus. Die Übung demonstriert die Integration verschiedener Funktionsbausteine zu einem funktionierenden Gesamtsystem.