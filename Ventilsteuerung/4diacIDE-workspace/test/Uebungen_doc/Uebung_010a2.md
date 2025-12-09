# Uebung_010a2: Button_A1 auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert eine einfache Verbindung zwischen einem Eingabe-Button und einem digitalen Ausgang. Der Funktionsbaustein "Button_A1" steuert direkt den Ausgang "DigitalOutput_Q1" an.

## Verwendete Funktionsbausteine (FBs)

### Button_IX (Button_A1)
- **Typ**: Eingabe-Button Funktionsbaustein
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - u16ObjId = DefaultPool::Button_A1 (Objekt-ID für Button-Konfiguration)
- **Ereignisausgang**: IND (Indicator Event)
- **Datenaustgang**: IN (Input Data)

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: Digitaler Ausgangsbaustein für logiBUS
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zugewiesener Ausgang)
- **Ereigniseingang**: REQ (Request Event)
- **Dateneingang**: OUT (Output Data)

## Programmablauf und Verbindungen

**Ereignisverbindung:**
- Button_A1.IND → DigitalOutput_Q1.REQ

**Datenverbindung:**
- Button_A1.IN → DigitalOutput_Q1.OUT

**Ablauf:**
1. Bei Betätigung des Buttons A1 wird das IND-Ereignis ausgelöst
2. Das Ereignis wird an den REQ-Eingang des Digitalausgangs Q1 weitergeleitet
3. Gleichzeitig wird der Datenwert (IN) vom Button an den OUT-Eingang des Digitalausgangs übertragen
4. Der Digitalausgang Q1 schaltet entsprechend dem empfangenen Signal

**Lernziele:**
- Grundlegende Verbindung von Eingabe- und Ausgabebausteinen
- Verständnis von Ereignis- und Datenverbindungen
- Einfache Signalverarbeitung in 4diac

**Schwierigkeitsgrad:** Einfach

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Basiswissen über Ereignissteuerung

**Starten der Übung:**
Die Übung wird durch Betätigen des Buttons A1 gestartet, woraufhin der Ausgang Q1 entsprechend reagiert.

## Zusammenfassung
Diese Übung vermittelt die grundlegende Funktionsweise der Signalverarbeitung in 4diac durch direkte Verbindung eines Eingabe-Buttons mit einem digitalen Ausgang. Sie dient als Einstieg in die Ereignisgesteuerte Automatisierungstechnik und demonstriert das Zusammenspiel von Ereignis- und Datenverbindungen zwischen Funktionsbausteinen.