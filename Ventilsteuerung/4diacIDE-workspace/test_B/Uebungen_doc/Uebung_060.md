# Uebung_060: für TC-SC also Task Controller Section Control

* * * * * * * * * *
## Einleitung
Diese Übung behandelt die Implementierung einer Task Controller Section Control (TC-SC) Funktionalität in der 4diac-IDE. Die Anwendung demonstriert die Verarbeitung von kondensierten Arbeitszuständen und Sektionskontroll-Daten gemäß ISOBUS-Standards.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **SETPOINT_CONDENSED_WORK_STATE_1_16** (TC_ID): Empfängt Soll-Werte für kondensierte Arbeitszustände
- **SPLIT_DWORD_INTO_QUARTERS**: Teilt ein 32-Bit-Wort in 16 Quarter-Bytes auf
- **QUARTERS_TO_BOOLS**: Wandelt Quarter-Bytes in boolesche Werte um
- **BOOLS_TO_QUARTERS**: Wandelt boolesche Werte zurück in Quarter-Bytes
- **ASSEMBLE_DWORD_FROM_QUARTERS**: Setzt Quarter-Bytes zu einem 32-Bit-Wort zusammen
- **ACTUAL_CONDENSED_WORK_STATE_1_16** (TC_QD): Sendet Ist-Werte für kondensierte Arbeitszustände
- **SECTION_CONTROL_STATE_IN** (TC_ID): Empfängt Sektionskontroll-Zustände
- **SECTION_CONTROL_STATE_OUT** (TC_QD): Sendet Sektionskontroll-Zustände
- **ACTUAL_RATE** (TC_QD): Sendet aktuelle Applikationsraten
- **ACTUAL_WORK_STATE** (TC_QD): Sendet aktuelle Arbeitszustände
- **F_GT** (Vergleichsfunktion): Größer-Vergleich für DWORD-Werte
- **F_SEL** (Selektor): Wählt zwischen zwei Eingangswerten basierend auf einem Steuersignal

### Sub-Bausteine: Uebung_060_sub_Outputs

- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **DigitalOutput_Q1 bis DigitalOutput_Q8** (logiBUS_QX)
    - Parameter: QI = TRUE
    - Parameter: Output = logiBUS_DO::Output_Qx (entsprechende Ausgänge)
    - Ereigniseingang: REQ
    - Datenausgang: OUT
- **Funktionsweise**: Die Sub-Applikation empfängt boolesche Signale von Q_00 bis Q_08 und gibt diese über entsprechende logiBUS-Digitalausgänge aus. Jeder Ausgang wird über ein REQ-Ereignis angesteuert.

## Programmablauf und Verbindungen

Der Programmablauf beginnt mit dem Empfang von Sollwerten durch SETPOINT_CONDENSED_WORK_STATE_1_16. Das eingehende DWORD wird in Quarter-Bytes aufgeteilt und in boolesche Signale umgewandelt. Diese Signale werden teilweise an die Ausgabesubapplikation weitergeleitet und gleichzeitig zurück in Quarter-Bytes konvertiert. 

Die rückkonvertierten Quarter-Bytes werden zu einem DWORD zusammengesetzt und an ACTUAL_CONDENSED_WORK_STATE_1_16 gesendet. Parallel dazu werden Sektionskontrollzustände direkt durchgereicht und Applikationsraten/Arbeitszustände basierend auf Vergleichsoperationen selektiert.

**Lernziele:**
- Verständnis der ISOBUS TC-SC Kommunikation
- Umgang mit DWORD-zu-BOOL-Konvertierungen
- Implementierung von Datenverarbeitungsketten
- Verwendung von Vergleichs- und Selektionsfunktionen

**Schwierigkeitsgrad:** Mittel

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Basiswissen über ISOBUS-Kommunikation

**Starten der Übung:** Die Übung wird in der 4diac-IDE geladen und kann nach Konfiguration der Geräteparameter gestartet werden.

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit der Implementierung von Task Controller Section Control Funktionalitäten unter Verwendung standardisierter ISOBUS-Kommunikationsbausteine. Der Schwerpunkt liegt auf der Datenverarbeitung zwischen verschiedenen Darstellungsformen (DWORD, Quarter-Bytes, BOOL) und der Steuerung von Ausgabesignalen über eine strukturierte Sub-Applikation.