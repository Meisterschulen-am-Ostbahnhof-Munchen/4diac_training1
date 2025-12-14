# Uebung_012c: String Input und Speichern (WIP)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung von String-Eingaben und deren Speicherung in einem nicht-flüchtigen Speicher (NVS). Das Programm ermöglicht das Einlesen numerischer Werte, deren Konvertierung und die persistente Speicherung von String-Daten.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **InputNumber_I1** (Typ: NumericValue_ID)
  - Liest numerische Eingabewerte ein
  - Objekt-ID: DefaultPool::InputNumber_I1

- **F_DWORD_TO_UDINT** (Typ: F_DWORD_TO_UDINT)
  - Führt eine Datentypkonvertierung von DWORD zu UDINT durch

- **INI** (Typ: INI)
  - Verwaltet nicht-flüchtige Speicheroperationen
  - Parameter:
    - SECTION: NVS_Keys::SECTION_S1_STORE
    - KEY: NVS_Keys::KEY_S1_STORE
    - VALUE: STRING#'Test'
    - DEFAULT_VALUE: STRING#'Test'

- **Q_NumericValue** (Typ: Q_StringValue)
  - Gibt String-Werte aus
  - Objekt-ID: DefaultPool::InputNumber_I1

- **CbVtStatus** (Typ: CbVtStatus)
  - Überwacht den Status der Visualisierungskomponente

## Programmablauf und Verbindungen

### Ereignisverbindungen:
1. `InputNumber_I1.IND` → `F_DWORD_TO_UDINT.REQ`
2. `F_DWORD_TO_UDINT.CNF` → `INI.SET`
3. `INI.GETO` → `Q_NumericValue.REQ`
4. `CbVtStatus.IND` → `Q_NumericValue.REQ`
5. `INI.INITO` → `INI.GET` (interne Rückkopplung)

### Datenverbindungen:
1. `InputNumber_I1.IN` → `F_DWORD_TO_UDINT.IN`
2. `INI.VALUEO` → `Q_NumericValue.pau8String`

### Ablaufbeschreibung:
1. Die Übung startet mit der Initialisierung des INI-Bausteins
2. Numerische Eingaben werden über InputNumber_I1 erfasst
3. Die Daten werden konvertiert und an den INI-Baustein zur Speicherung weitergeleitet
4. Gleichzeitig werden gespeicherte Werte über Q_NumericValue ausgegeben
5. Der CbVtStatus-Baustein sorgt für eine aktuelle Statusanzeige

**Schwierigkeitsgrad**: Mittel  
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Datentypkonvertierung, NVS-Speicherkonzepte

## Zusammenfassung
Diese Übung vermittelt praktische Kenntnisse im Umgang mit String-Verarbeitung und persistenter Datenspeicherung in IEC 61499-Systemen. Die Teilnehmer lernen die Konvertierung zwischen verschiedenen Datentypen, die Verwaltung von nicht-flüchtigem Speicher und die Integration von Visualisierungskomponenten in automatisierungstechnische Anwendungen.