# Uebung_012a: Numeric Value Input und Speichern

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung numerischer Eingabewerte und deren Speicherung in einem Non-Volatile Storage (NVS). Der Fokus liegt auf der Integration verschiedener Funktionsbausteine zur Datenerfassung, Typkonvertierung und persistenter Speicherung.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **CbVtStatus**: Dient als Auslöser für die Verarbeitungskette
- **Uebung_012a_sub**: Haupt-Subapplikation für die numerische Werteverarbeitung

### Sub-Bausteine: Uebung_012a_sub

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **ID** (Typ: NumericValue_ID)
        - Parameter: QI = TRUE
        - Ereignisausgang: IND
        - Dateneingang: u16ObjId
        - Datenausgang: IN
    - **F_DWORD_TO_UDINT** (Typ: F_DWORD_TO_UDINT)
        - Ereigniseingang: REQ
        - Ereignisausgang: CNF
        - Dateneingang: IN
        - Datenausgang: OUT
    - **NVS** (Typ: NVS)
        - Parameter: QI = TRUE, DEFAULT_VALUE = UDINT#0
        - Ereigniseingänge: SET, GET, INIT
        - Ereignisausgänge: SETO, GETO, INITO
        - Dateneingänge: KEY, VALUE
        - Datenausgänge: VALUEO
    - **Q_NumericValue** (Typ: Q_NumericValue)
        - Ereigniseingang: REQ
        - Dateneingänge: u16ObjId, u32NewValue

- **Funktionsweise**: Die Subapplikation verarbeitet numerische Eingaben durch Identifikation, Typkonvertierung und Speicherung im NVS. Bei Initialisierung wird der gespeicherte Wert abgerufen und ausgegeben.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- CbVtStatus.IND → Uebung_012a_sub.REQ
- ID.IND → F_DWORD_TO_UDINT.REQ
- F_DWORD_TO_UDINT.CNF → NVS.SET
- NVS.SETO → IND (Ausgang der Subapplikation)
- NVS.GETO → Q_NumericValue.REQ
- NVS.GETO → IND (Ausgang der Subapplikation)
- NVS.INITO → NVS.GET

**Datenverbindungen:**
- ID.IN → F_DWORD_TO_UDINT.IN
- u16ObjId (Parameter) → Q_NumericValue.u16ObjId
- KEY (Parameter) → NVS.KEY
- F_DWORD_TO_UDINT.OUT → NVS.VALUE
- NVS.VALUEO → Q_NumericValue.u32NewValue
- NVS.VALUEO → VALUEO (Ausgang der Subapplikation)
- u16ObjId (Parameter) → ID.u16ObjId

**Parameter:**
- KEY: NVS_Keys::KEY_I1_STORE (Speicherschlüssel)
- u16ObjId: DefaultPool::InputNumber_I1 (Objekt-ID für numerische Eingabe)

**Lernziele:**
- Verständnis der Numeric Value Input-Verarbeitung
- Umgang mit Typkonvertierungen (DWORD zu UDINT)
- Implementierung von Non-Volatile Storage für persistente Datenspeicherung
- Ereignisgesteuerte Programmabläufe in 4diac

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundkenntnisse in 4diac-IDE, Funktionsbausteinen und Ereignisverarbeitung

**Starten der Übung**: Die Übung wird durch das Eintreffen eines IND-Ereignisses am CbVtStatus-Baustein gestartet.

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit der Verarbeitung numerischer Eingabewerte und deren persistenter Speicherung. Der Aufbau demonstriert eine typische Verarbeitungskette von der Datenerfassung über Typkonvertierung bis zur Speicherung und zeigt dabei die Integration verschiedener Standard-Funktionsbausteine in 4diac.