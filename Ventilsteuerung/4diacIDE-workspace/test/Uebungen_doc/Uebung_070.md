# Uebung_070: WBSD auf UT ausgeben

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Ausgabe von radbasierter Maschinengeschwindigkeit (WBSD - Wheel Based machine Speed) auf einem User Terminal (UT). Der Fokus liegt auf der Verarbeitung und Übertragung von Geschwindigkeitsdaten innerhalb eines 4diac-Systems.

## Verwendete Funktionsbausteine (FBs)

### I_WBSD
- **Typ**: Eingangsbaustein für radbasierte Maschinengeschwindigkeit
- **Parameter**: QI = TRUE (Qualified Input aktiviert)
- **Ereignisausgang**: IND (Indication - Signalisiert verfügbare Daten)
- **Datenausgang**: WHEELBASEDMACHINESPEED (Geschwindigkeitswert)

### Q_NumericValue
- **Typ**: Ausgangsbaustein für numerische Werte
- **Parameter**: u16ObjId = "DefaultPool_TECU::NumberVariable_Wheel_based_machine_speed" (Objekt-ID für die Geschwindigkeitsvariable)
- **Ereigniseingang**: REQ (Request - Anfrage zur Wertausgabe)
- **Dateneingang**: u32NewValue (Neuer numerischer Wert)

## Programmablauf und Verbindungen

**Ereignisverbindung:**
- I_WBSD.IND → Q_NumericValue.REQ

**Datenverbindung:**
- I_WBSD.WHEELBASEDMACHINESPEED → Q_NumericValue.u32NewValue

**Programmablauf:**
1. Der I_WBSD-Baustein erfasst kontinuierlich die radbasierte Maschinengeschwindigkeit
2. Bei verfügbaren neuen Geschwindigkeitsdaten wird das IND-Ereignis ausgelöst
3. Dieses Ereignis triggert den Q_NumericValue-Baustein über die REQ-Verbindung
4. Der Geschwindigkeitswert wird über die Datenverbindung an Q_NumericValue übertragen
5. Q_NumericValue gibt den Wert unter der spezifizierten Objekt-ID auf dem User Terminal aus

**Lernziele:**
- Verständnis der Datenverarbeitungskette in 4diac
- Umgang mit Geschwindigkeitssensordaten
- Konfiguration von Ausgabebausteinen für User Terminal
- Ereignisgesteuerte Datenübertragung

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Datenverbindungen

## Zusammenfassung
Diese Übung zeigt eine grundlegende Implementierung zur Erfassung und Ausgabe von Maschinengeschwindigkeitsdaten. Sie demonstriert das Prinzip der ereignisgesteuerten Datenverarbeitung in 4diac-Systemen und die Integration von Sensordaten mit User Terminal-Ausgaben. Die einfache Struktur macht sie ideal für den Einstieg in die Datenverarbeitung mit 4diac.