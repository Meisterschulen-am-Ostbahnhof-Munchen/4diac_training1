# Uebung_011a: Numeric Value Output und BUTTON_PRESS_REPEAT_DONE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von numerischen Wertausgaben in Verbindung mit Tasterereignissen. Der Schwerpunkt liegt auf der Verarbeitung des BUTTON_PRESS_REPEAT_DONE-Ereignisses, das nur am Ende einer Tasterbetätigung ausgelöst wird.

## Verwendete Funktionsbausteine (FBs)

### logiBUS_IB
- **Typ**: logiBUS_IB
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (Eingang I1)
  - InputEvent = logiBUS_DI_Events::BUTTON_PRESS_REPEAT_DONE (Ereignistyp)
- **Ereignisausgang**: IND (wird bei Tasterereignis ausgelöst)
- **Datenausgang**: IN (liefert den Eingangswert)

### F_BYTE_TO_UDINT
- **Typ**: F_BYTE_TO_UDINT
- **Ereigniseingang**: REQ (startet die Konvertierung)
- **Ereignisausgang**: CNF (bestätigt abgeschlossene Konvertierung)
- **Dateneingang**: IN (BYTE-Wert)
- **Datenausgang**: OUT (konvertierter UDINT-Wert)

### Q_NumericValue
- **Typ**: Q_NumericValue
- **Parameter**:
  - u16ObjId = DefaultPool::OutputNumber_N1 (Ausgabekanal N1)
- **Ereigniseingang**: REQ (startet die Wertausgabe)
- **Dateneingang**: u32NewValue (neuer numerischer Wert)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- logiBUS_IB.IND → F_BYTE_TO_UDINT.REQ
- F_BYTE_TO_UDINT.CNF → Q_NumericValue.REQ

**Datenverbindungen:**
- logiBUS_IB.IN → F_BYTE_TO_UDINT.IN
- F_BYTE_TO_UDINT.OUT → Q_NumericValue.u32NewValue

**Programmablauf:**
1. Beim Loslassen des Tasters (BUTTON_PRESS_REPEAT_DONE) wird das IND-Ereignis ausgelöst
2. Der BYTE-Wert vom Eingang I1 wird an F_BYTE_TO_UDINT weitergeleitet
3. F_BYTE_TO_UDINT konvertiert den BYTE-Wert in einen UDINT-Wert
4. Nach erfolgreicher Konvertierung wird Q_NumericValue mit dem neuen Wert aktualisiert
5. Der numerische Wert wird auf Ausgang N1 ausgegeben

**Lernziele:**
- Verständnis von Tasterereignissen (BUTTON_PRESS_REPEAT_DONE vs. BUTTON_PRESS_REPEAT)
- Datentypkonvertierung von BYTE zu UDINT
- Numerische Wertausgabe auf logi.cals-Systemen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen über Funktionsbausteine

## Zusammenfassung
Diese Übung zeigt eine einfache Anwendung zur Verarbeitung von Tasterereignissen und numerischer Wertausgabe. Der Fokus liegt auf dem BUTTON_PRESS_REPEAT_DONE-Ereignis, das im Gegensatz zu BUTTON_PRESS_REPEAT nur einmal am Ende der Tasterbetätigung ausgelöst wird. Die Übung demonstriert zudem die Notwendigkeit von Datentypkonvertierungen in automatisierten Systemen.