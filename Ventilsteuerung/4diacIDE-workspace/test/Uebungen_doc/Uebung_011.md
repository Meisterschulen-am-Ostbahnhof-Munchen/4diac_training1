# Uebung_011: Numeric Value Input

* * * * * * * * * *
## Einleitung
Diese Übung demonstriert die Verarbeitung numerischer Eingabewerte in einem 4diac-IDE System. Die Anwendung konvertiert einen numerischen Eingabewert von einem Datentyp in einen anderen und zeigt grundlegende Konzepte der Datenverarbeitung in IEC 61499-Systemen.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: NumericValue_ID
- **Typ**: NumericValue_ID
- **Verwendete interne FBs**: Keine
- **Funktionsweise**: Dieser Baustein dient zur Erfassung numerischer Eingabewerte. Bei Aktivierung durch ein Ereignis liefert er den aktuellen numerischen Wert an seinem Datenausgang.

### Sub-Bausteine: F_DWORD_TO_UDINT
- **Typ**: F_DWORD_TO_UDINT
- **Verwendete interne FBs**: Keine
- **Funktionsweise**: Dieser Konvertierungsbaustein wandelt einen DWORD-Datentyp in einen UDINT-Datentyp um. Er wird durch ein REQ-Ereignis aktiviert und gibt nach erfolgreicher Konvertierung ein CNF-Ereignis aus.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- InputNumber_I1.IND → F_DWORD_TO_UDINT.REQ

**Datenverbindungen:**
- InputNumber_I1.IN → F_DWORD_TO_UDINT.IN

**Parameterkonfiguration:**
- InputNumber_I1: QI = TRUE (immer aktiviert)
- InputNumber_I1: u16ObjId = "DefaultPool::InputNumber_I1"

**Programmablauf:**
1. Der NumericValue_ID-Baustein erfasst einen numerischen Eingabewert
2. Bei Wertänderung wird das IND-Ereignis ausgelöst
3. Das IND-Ereignis aktiviert den F_DWORD_TO_UDINT-Konvertierungsbaustein
4. Der numerische Wert wird über die Datenverbindung an den Konvertierungsbaustein übergeben
5. F_DWORD_TO_UDINT führt die Typkonvertierung durch

**Lernziele:**
- Verständnis der Datenkonvertierung zwischen verschiedenen Datentypen
- Umgang mit numerischen Eingabebausteinen
- Grundlagen der Ereignis- und Datenverbindungen in 4diac

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis von IEC 61499-Funktionsbausteinen
- Basiswissen über Datentypen in Automatisierungssystemen

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der numerischen Datenverarbeitung in 4diac-Systemen. Sie zeigt, wie numerische Eingabewerte erfasst und zwischen verschiedenen Datentypen konvertiert werden können. Die einfache Struktur mit nur zwei Funktionsbausteinen macht diese Übung ideal für den Einstieg in die Datenverarbeitung mit IEC 61499-Standards.