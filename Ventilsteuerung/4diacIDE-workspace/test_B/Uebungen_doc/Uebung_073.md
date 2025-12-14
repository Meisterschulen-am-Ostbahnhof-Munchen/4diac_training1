# Uebung_073: VDS auf UT ausgeben

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Ausgabe von Fahrzeuggeschwindigkeitsdaten auf ein Bedienpanel. Es werden zwei verschiedene Geschwindigkeitsmesswerte verarbeitet und an entsprechende numerische Variablen übergeben.

## Verwendete Funktionsbausteine (FBs)

### I_GBSD
- **Typ**: Eingangsbaustein für bodengestützte Maschinengeschwindigkeit
- **Parameter**: QI = TRUE (aktiviert den Baustein)
- **Ereignisausgang**: IND (Indikator-Ereignis)
- **Datenausgang**: GROUNDBASEDMACHINESPEED (bodengestützte Maschinengeschwindigkeit)

### Q_NumericValue_GBSD
- **Typ**: Ausgabebaustein für numerische Werte
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Ground_based_machine_speed"
- **Ereigniseingang**: REQ (Anfrage-Ereignis)
- **Dateneingang**: u32NewValue (neuer numerischer Wert)

### I_VDS
- **Typ**: Eingangsbaustein für navigationsbasierte Fahrzeuggeschwindigkeit
- **Parameter**: QI = TRUE (aktiviert den Baustein)
- **Ereignisausgang**: IND (Indikator-Ereignis)
- **Datenausgang**: NavigationBasedVehicleSpeed (navigationsbasierte Fahrzeuggeschwindigkeit)

### Q_NumericValue_WBSD
- **Typ**: Ausgabebaustein für numerische Werte
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Wheel_based_machine_speed"
- **Ereigniseingang**: REQ (Anfrage-Ereignis)
- **Dateneingang**: u32NewValue (neuer numerischer Wert)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- I_GBSD.IND → Q_NumericValue_GBSD.REQ
- I_VDS.IND → Q_NumericValue_WBSD.REQ

**Datenverbindungen:**
- I_GBSD.GROUNDBASEDMACHINESPEED → Q_NumericValue_GBSD.u32NewValue
- I_VDS.NavigationBasedVehicleSpeed → Q_NumericValue_WBSD.u32NewValue

**Programmablauf:**
1. Die Eingangsbausteine I_GBSD und I_VDS werden mit QI=TRUE aktiviert
2. Bei neuen Geschwindigkeitsdaten generieren die Eingangsbausteine IND-Ereignisse
3. Diese Ereignisse lösen die REQ-Ereignisse der Ausgabebausteine aus
4. Gleichzeitig werden die Geschwindigkeitsdaten an die entsprechenden numerischen Variablen übergeben
5. Die Werte werden in den definierten Objekten "NumberVariable_Ground_based_machine_speed" und "NumberVariable_Wheel_based_machine_speed" gespeichert

**Lernziele:**
- Verarbeitung von Geschwindigkeitsdaten aus verschiedenen Quellen
- Verwendung von numerischen Ausgabevariablen
- Ereignisgesteuerte Datenübertragung
- Konfiguration von Objekt-IDs für Variablenzugriff

## Zusammenfassung
Diese Übung zeigt ein einfaches aber effektives System zur Verarbeitung und Ausgabe von Geschwindigkeitsdaten. Zwei unabhängige Geschwindigkeitsmesssysteme (bodengestützt und radbasiert) werden parallel verarbeitet und ihre Werte an entsprechende numerische Variablen auf dem Bedienpanel übergeben. Die ereignisgesteuerte Architektur gewährleistet eine effiziente Datenverarbeitung ohne unnötige Zyklen.