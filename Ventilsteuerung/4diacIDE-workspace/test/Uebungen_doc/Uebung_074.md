# Uebung_074: RPTO auf UT ausgeben

* * * * * * * * * *
## Einleitung
Diese Übung demonstriert die Verarbeitung und Ausgabe von Drehzahl-Daten eines Heckzapfwellenantriebs (Rear Power Take-Off). Der Funktionsbaustein liest die Drehzahlwerte und gibt sie über einen numerischen Wert an die Benutzeroberfläche aus.

## Verwendete Funktionsbausteine (FBs)

### I_RPTO
- **Typ**: Eingangsbaustein für Heckzapfwellen-Drehzahl
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
- **Ereignisausgänge**: IND (Indication), TIMEOUT
- **Datenausgänge**: REAR_PTO_OUTP_SHAFT_SPEED

### F_SEL_E_2
- **Typ**: Selektionsbaustein mit zwei Eingängen
- **Parameter**: 
  - IN1 = UDINT#0 (Unsigned Double Integer 0)
- **Ereigniseingänge**: REQ0, REQ1
- **Ereignisausgänge**: CNF (Confirmation)
- **Dateneingänge**: IN0
- **Datenausgänge**: OUT

### Q_NumericValue_GBSD
- **Typ**: Ausgabebaustein für numerische Werte
- **Parameter**: 
  - u16ObjId = DefaultPool_TECU::NumberVariable_Rear_PTO_output_shaft_speed
- **Ereigniseingänge**: REQ
- **Dateneingänge**: u32NewValue

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- I_RPTO.IND → F_SEL_E_2.REQ0
- F_SEL_E_2.CNF → Q_NumericValue_GBSD.REQ
- I_RPTO.TIMEOUT → F_SEL_E_2.REQ1

**Datenverbindungen:**
- I_RPTO.REAR_PTO_OUTP_SHAFT_SPEED → F_SEL_E_2.IN0
- F_SEL_E_2.OUT → Q_NumericValue_GBSD.u32NewValue

**Programmablauf:**
1. Der I_RPTO Baustein liest kontinuierlich die Drehzahl der Heckzapfwelle
2. Bei neuen Daten (IND) oder Timeout (TIMEOUT) wird der F_SEL_E_2 Baustein aktiviert
3. F_SEL_E_2 selektiert zwischen den beiden Eingangsquellen und gibt die Daten weiter
4. Q_NumericValue_GBSD empfängt die verarbeiteten Daten und stellt sie auf der Benutzeroberfläche dar

**Lernziele:**
- Verarbeitung von Drehzahlsensordaten
- Verwendung von Selektionsbausteinen
- Ausgabe von numerischen Werten auf der Benutzeroberfläche
- Umgang mit Timeout-Ereignissen

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen über Funktionsbausteine

## Zusammenfassung
Diese Übung zeigt eine typische Anwendung zur Erfassung und Visualisierung von Maschinendaten. Der Aufbau demonstriert, wie Sensordaten (Drehzahl) erfasst, verarbeitet und schließlich auf einer Benutzeroberfläche angezeigt werden können. Die Verwendung des Selektionsbausteins ermöglicht eine flexible Datenverarbeitung mit unterschiedlichen Auslösebedingungen.