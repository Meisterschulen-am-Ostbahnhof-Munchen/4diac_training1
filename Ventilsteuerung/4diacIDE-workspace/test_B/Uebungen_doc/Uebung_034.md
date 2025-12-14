# Uebung_034: Analog-Eingang auf PWM Ausgang

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung eines analogen Eingangssignals und dessen Umwandlung in ein PWM-Ausgangssignal. Das System liest einen analogen Wert ein, verarbeitet diesen und gibt ihn als Pulsweitenmodulationssignal aus.

## Verwendete Funktionsbausteine (FBs)

### AnalogInput_I7
- **Typ**: logiBUS_AI_ID
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_AI::AnalogInput_I7
  - AnalogInput_hysteresis = 50
- **Funktionsweise**: Liest analoge Eingangswerte vom logiBUS System ein

### F_SHL
- **Typ**: F_SHL (Shift Left)
- **Parameter**:
  - N = UINT#1
- **Funktionsweise**: Führt eine Linksverschiebung der Eingangsdaten um 1 Bit durch

### F_DWORD_TO_UDINT_I7
- **Typ**: F_DWORD_TO_UDINT
- **Funktionsweise**: Konvertiert DWORD-Datentyp in UDINT-Datentyp

### PWMOutput_Q4
- **Typ**: logiBUS_QD_PWM
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q4
- **Funktionsweise**: Erzeugt ein PWM-Signal am logiBUS Ausgang

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- AnalogInput_I7.IND → F_SHL.REQ
- F_SHL.CNF → F_DWORD_TO_UDINT_I7.REQ
- F_SHL.CNF → PWMOutput_Q4.REQ

**Datenverbindungen:**
- AnalogInput_I7.IN → F_SHL.IN
- F_SHL.OUT → PWMOutput_Q4.OUT
- F_SHL.OUT → F_DWORD_TO_UDINT_I7.IN

**Ablauf:**
1. Der Analog-Eingang liest kontinuierlich Werte ein
2. Bei neuen Daten (IND-Event) wird die Linksverschiebung aktiviert
3. Das verschobene Signal wird sowohl an den PWM-Ausgang als auch an den Typkonverter gesendet
4. Der PWM-Ausgang generiert entsprechend dem verarbeiteten Signal ein Ausgangssignal

**Lernziele:**
- Verarbeitung analoger Eingangssignale
- Bit-Operationen mit F_SHL
- PWM-Signalgenerierung
- Datentyp-Konvertierung
- Event- und Datenflusssteuerung in 4diac

**Schwierigkeitsgrad**: Einsteiger
**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, logiBUS System

## Zusammenfassung
Diese Übung zeigt eine komplette Signalverarbeitungskette von der analogen Eingabe bis zur PWM-Ausgabe. Sie vermittelt praktische Kenntnisse in der Signalverarbeitung, Bit-Operationen und der Ansteuerung von PWM-Ausgängen im 4diac Framework.