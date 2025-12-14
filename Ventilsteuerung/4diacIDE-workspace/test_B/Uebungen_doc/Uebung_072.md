# Uebung_072: GBSD auf UT ausgeben

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Ausgabe von Geschwindigkeitsdaten auf ein Bedienpanel. Es werden zwei verschiedene Geschwindigkeitswerte verarbeitet und ausgegeben: die bodenbasierten und die radbasierten Maschinengeschwindigkeiten.

## Verwendete Funktionsbausteine (FBs)

### I_GBSD
- **Typ**: I_GBSD
- **Parameter**: QI = TRUE
- **Ereignisausgang**: IND
- **Datenausgang**: GROUNDBASEDMACHINESPEED

### Q_NumericValue_GBSD
- **Typ**: Q_NumericValue
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Ground_based_machine_speed"
- **Ereigniseingang**: REQ

### I_WBSD
- **Typ**: I_WBSD
- **Parameter**: QI = TRUE
- **Ereignisausgang**: IND
- **Datenausgang**: WHEELBASEDMACHINESPEED

### Q_NumericValue_WBSD
- **Typ**: Q_NumericValue
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Wheel_based_machine_speed"
- **Ereigniseingang**: REQ

## Programmablauf und Verbindungen

Das Programm besteht aus zwei parallelen Verarbeitungsketten:

**Erste Verarbeitungskette (GBSD):**
- I_GBSD erzeugt die bodenbasierte Maschinengeschwindigkeit
- Bei IND-Ereignis wird Q_NumericValue_GBSD über REQ aktiviert
- Der Geschwindigkeitswert GROUNDBASEDMACHINESPEED wird an Q_NumericValue_GBSD.u32NewValue übergeben

**Zweite Verarbeitungskette (WBSD):**
- I_WBSD erzeugt die radbasierte Maschinengeschwindigkeit
- Bei IND-Ereignis wird Q_NumericValue_WBSD über REQ aktiviert
- Der Geschwindigkeitswert WHEELBASEDMACHINESPEED wird an Q_NumericValue_WBSD.u32NewValue übergeben

**Ereignisverbindungen:**
- I_GBSD.IND → Q_NumericValue_GBSD.REQ
- I_WBSD.IND → Q_NumericValue_WBSD.REQ

**Datenverbindungen:**
- I_GBSD.GROUNDBASEDMACHINESPEED → Q_NumericValue_GBSD.u32NewValue
- I_WBSD.WHEELBASEDMACHINESPEED → Q_NumericValue_WBSD.u32NewValue

## Zusammenfassung
Diese Übung zeigt die grundlegende Verarbeitung und Ausgabe von numerischen Werten in 4diac. Zwei unabhängige Geschwindigkeitssensoren liefern Daten, die parallel verarbeitet und auf dem Bedienpanel ausgegeben werden. Die Übung vermittelt das Verständnis für ereignisgesteuerte Datenverarbeitung und die Verwendung von numerischen Ausgabebausteinen.