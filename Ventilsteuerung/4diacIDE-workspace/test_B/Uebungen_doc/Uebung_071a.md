# Uebung_071a: WBSD auf UT ausgeben, Q1 Schalten wenn Speed &gt;0

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von WBSD-Daten (Wheel Based Machine Speed) und die Steuerung eines digitalen Ausgangs basierend auf Geschwindigkeitswerten. Das System gibt die Geschwindigkeitswerte auf einem Display aus und schaltet einen digitalen Ausgang, wenn die Geschwindigkeit größer als 0 ist.

## Verwendete Funktionsbausteine (FBs)

### I_WBSD
- **Typ**: Eingangsbaustein für WBSD-Daten
- **Parameter**: QI = TRUE (aktiviert den Baustein)
- **Ereignisausgänge**: IND
- **Datenausgänge**: WHEELBASEDMACHINESPEED

### Q_NumericValue_WBSD
- **Typ**: Ausgabebaustein für numerische Werte
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Wheel_based_machine_speed"
- **Ereigniseingänge**: REQ
- **Dateneingänge**: u32NewValue

### F_GT
- **Typ**: Vergleichsbaustein (Greater Than)
- **Parameter**: IN2 = UINT#0 (Vergleichswert 0)
- **Ereigniseingänge**: REQ
- **Ereignisausgänge**: CNF
- **Dateneingänge**: IN1
- **Datenausgänge**: OUT

### E_D_FF
- **Typ**: D-Flipflop
- **Ereigniseingänge**: CLK
- **Ereignisausgänge**: EO
- **Dateneingänge**: D
- **Datenausgänge**: Q

### DigitalOutput_Q1
- **Typ**: Digitaler Ausgang (logiBUS_QX)
- **Parameter**: 
  - QI = TRUE (aktiviert den Baustein)
  - Output = "logiBUS_DO::Output_Q1"
- **Ereigniseingänge**: REQ
- **Dateneingänge**: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- I_WBSD.IND → Q_NumericValue_WBSD.REQ
- I_WBSD.IND → F_GT.REQ
- F_GT.CNF → E_D_FF.CLK
- E_D_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- I_WBSD.WHEELBASEDMACHINESPEED → Q_NumericValue_WBSD.u32NewValue
- I_WBSD.WHEELBASEDMACHINESPEED → F_GT.IN1
- F_GT.OUT → E_D_FF.D
- E_D_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Der I_WBSD Baustein empfängt Geschwindigkeitsdaten und triggert das IND-Ereignis
2. Gleichzeitig wird die Geschwindigkeit an Q_NumericValue_WBSD zur Anzeige und an F_GT zum Vergleich gesendet
3. F_GT vergleicht die Geschwindigkeit mit 0 und gibt das Ergebnis an E_D_FF weiter
4. E_D_FF speichert den Vergleichswert und triggert bei positiver Flanke den Digitalausgang
5. DigitalOutput_Q1 schaltet den Ausgang Q1 entsprechend dem gespeicherten Wert

**Lernziele:**
- Verarbeitung von Geschwindigkeitsdaten
- Verwendung von Vergleichsbausteinen
- Einsatz von Flipflops zur Signalverarbeitung
- Steuerung digitaler Ausgänge basierend auf Sensordaten

## Zusammenfassung
Diese Übung zeigt eine typische Anwendung zur Geschwindigkeitsüberwachung und -verarbeitung. Das System kombiniert Datenerfassung, Vergleichslogik und Speicherelemente, um basierend auf Geschwindigkeitswerten eine digitale Ausgangssteuerung zu realisieren. Der D-Flipflop sorgt für eine stabile Ausgangssteuerung, während die WBSD-Daten parallel zur Anzeige gebracht werden.