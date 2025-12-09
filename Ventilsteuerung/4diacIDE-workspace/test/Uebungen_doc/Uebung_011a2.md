# Uebung_011a2: Numeric Value Output und BUTTON_PRESS_REPEAT_DONE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von Tasterereignissen und die Ausgabe numerischer Werte. Der Schwerpunkt liegt auf der Verwendung des BUTTON_LONG_PRESS_UP-Ereignisses und der Konvertierung von Datenformaten für die numerische Ausgabe.

## Verwendete Funktionsbausteine (FBs)

### logiBUS_ID
- **Typ**: logiBUS_ID
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Input = logiBUS_DI::Input_I1 (Eingang I1 des logiBUS-Digitalinputs)
  - InputEvent = logiBUS_DI_Events::BUTTON_LONG_PRESS_UP (verwendetes Tasterereignis)
- **Ereignisausgang**: IND (Indikation bei Ereigniseingang)
- **Datenausgang**: IN (Eingangswert)

### F_DWORD_TO_UDINT
- **Typ**: F_DWORD_TO_UDINT
- **Ereigniseingang**: REQ (Konvertierungsanforderung)
- **Ereignisausgang**: CNF (Konvertierungsbestätigung)
- **Dateneingang**: IN (DWORD-Eingangswert)
- **Datenausgang**: OUT (UDINT-Ausgangswert)

### Q_NumericValue
- **Typ**: Q_NumericValue
- **Parameter**:
  - u16ObjId = DefaultPool::OutputNumber_N1 (Ausgabekanal für numerische Werte)
- **Ereigniseingang**: REQ (Ausgabeanforderung)
- **Dateneingang**: u32NewValue (neuer numerischer Wert für die Ausgabe)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
1. logiBUS_ID.IND → F_DWORD_TO_UDINT.REQ
2. F_DWORD_TO_UDINT.CNF → Q_NumericValue.REQ

**Datenverbindungen:**
1. logiBUS_ID.IN → F_DWORD_TO_UDINT.IN
2. F_DWORD_TO_UDINT.OUT → Q_NumericValue.u32NewValue

**Programmablauf:**
1. Beim Loslassen eines lang gedrückten Tasters (BUTTON_LONG_PRESS_UP) an Eingang I1 wird das IND-Ereignis ausgelöst
2. Der Eingangswert wird an den Konvertierungsbaustein F_DWORD_TO_UDINT weitergeleitet
3. Nach erfolgreicher Konvertierung von DWORD zu UDINT wird das CNF-Ereignis ausgelöst
4. Der konvertierte Wert wird an Q_NumericValue zur Ausgabe auf dem definierten Ausgabekanal übergeben

**Lernziele:**
- Verarbeitung von Tasterereignissen
- Datenkonvertierung zwischen verschiedenen Datentypen
- Numerische Wertausgabe
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Basiswissen über Funktionsbausteine und Ereignisverarbeitung

## Zusammenfassung
Diese Übung zeigt eine einfache Ereignisverarbeitungskette, bei der ein Tasterereignis (BUTTON_LONG_PRESS_UP) erkannt, der zugehörige Wert konvertiert und anschließend numerisch ausgegeben wird. Die Übung vermittelt grundlegende Konzepte der ereignisgesteuerten Programmierung und Datenkonvertierung in 4diac-Systemen.