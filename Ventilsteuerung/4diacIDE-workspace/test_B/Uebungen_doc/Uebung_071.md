# Uebung_071: WBSD auf UT ausgeben, Q1 Schalten wenn Speed &gt;0

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von Geschwindigkeitsdaten und die Steuerung eines digitalen Ausgangs basierend auf Geschwindigkeitsbedingungen. Die Anwendung liest radbasierte Maschinengeschwindigkeitsdaten und gibt diese auf einem WBSD-Display aus, während gleichzeitig ein digitaler Ausgang (Q1) aktiviert wird, wenn die Geschwindigkeit größer als 0 ist.

## Verwendete Funktionsbausteine (FBs)

### I_WBSD
- **Typ**: Eingangsbaustein für radbasierte Maschinengeschwindigkeit
- **Parameter**: QI = TRUE
- **Ereignisausgänge**: IND
- **Datenausgänge**: WHEELBASEDMACHINESPEED

### Q_NumericValue_WBSD
- **Typ**: Numerischer Wertausgabe-Baustein
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Wheel_based_machine_speed"
- **Ereigniseingänge**: REQ
- **Dateneingänge**: u32NewValue

### F_GT
- **Typ**: Vergleichsbaustein (Größer als)
- **Parameter**: IN2 = UINT#0
- **Ereigniseingänge**: REQ
- **Ereignisausgänge**: CNF
- **Dateneingänge**: IN1
- **Datenausgänge**: OUT

### DigitalOutput_Q1
- **Typ**: Digitaler Ausgangsbaustein (logiBUS_QX)
- **Parameter**: 
  - QI = TRUE
  - Output = "logiBUS_DO::Output_Q1"
- **Ereigniseingänge**: REQ
- **Dateneingänge**: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- I_WBSD.IND → Q_NumericValue_WBSD.REQ
- I_WBSD.IND → F_GT.REQ
- F_GT.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- I_WBSD.WHEELBASEDMACHINESPEED → Q_NumericValue_WBSD.u32NewValue
- I_WBSD.WHEELBASEDMACHINESPEED → F_GT.IN1
- F_GT.OUT → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Der I_WBSD-Baustein liest kontinuierlich die radbasierte Maschinengeschwindigkeit
2. Bei neuen Geschwindigkeitsdaten wird das IND-Ereignis ausgelöst
3. Parallel werden die Geschwindigkeitsdaten an Q_NumericValue_WBSD zur Anzeige und an F_GT zur Vergleichsoperation gesendet
4. F_GT vergleicht die Geschwindigkeit mit 0 und gibt TRUE aus, wenn die Geschwindigkeit größer als 0 ist
5. Bei positivem Vergleichsergebnis wird der digitale Ausgang Q1 aktiviert

## Zusammenfassung
Diese Übung zeigt die grundlegende Verarbeitung von Sensordaten und die bedingte Steuerung von Aktoren. Sie vermittelt Kenntnisse in der Datenverarbeitung, Vergleichsoperationen und der Steuerung digitaler Ausgänge basierend auf Eingangsbedingungen. Die Anwendung kombiniert Datenvisualisierung mit logischer Steuerung in einem kompakten Steuerungssystem.