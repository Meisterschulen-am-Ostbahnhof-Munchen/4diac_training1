# Uebung_012b: Numeric Value Input und Speichern

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung numerischer Eingabewerte und deren dauerhafte Speicherung in 4diac. Der Fokus liegt auf der Verwendung von Non-Volatile Storage (NVS) zur Persistierung von Daten und der Anzeige von numerischen Werten auf einer Visualisierungsoberfläche.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_012b
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **InputNumber_I1**: NumericValue_ID
        - Parameter: u16ObjId = DefaultPool::InputNumber_I1
        - Ereignisausgang/-eingang: IND → F_DWORD_TO_UDINT.REQ
        - Datenausgang/-eingang: IN → F_DWORD_TO_UDINT.IN
    
    - **F_DWORD_TO_UDINT**: F_DWORD_TO_UDINT
        - Parameter: Keine
        - Ereignisausgang/-eingang: REQ ← InputNumber_I1.IND, CNF → INI.SET
        - Datenausgang/-eingang: IN ← InputNumber_I1.IN, OUT → INI.VALUE
    
    - **INI**: INI
        - Parameter: QI = TRUE, SECTION = NVS_Keys::SECTION_I1_STORE, KEY = NVS_Keys::KEY_I1_STORE, DEFAULT_VALUE = UDINT#55
        - Ereignisausgang/-eingang: SET ← F_DWORD_TO_UDINT.CNF, GETO → Q_NumericValue.REQ, INITO → INI.GET
        - Datenausgang/-eingang: VALUE ← F_DWORD_TO_UDINT.OUT, VALUEO → Q_NumericValue.u32NewValue
    
    - **Q_NumericValue**: Q_NumericValue
        - Parameter: u16ObjId = DefaultPool::InputNumber_I1
        - Ereignisausgang/-eingang: REQ ← INI.GETO, REQ ← CbVtStatus.IND
        - Datenausgang/-eingang: u32NewValue ← INI.VALUEO
    
    - **CbVtStatus**: CbVtStatus
        - Parameter: STATUS = "", u8Instance = "", qWsActive = "", wPage = ""
        - Ereignisausgang/-eingang: IND → Q_NumericValue.REQ
        - Datenausgang/-eingang: Keine

- **Funktionsweise**: Die Sub-App verarbeitet numerische Eingaben über InputNumber_I1, konvertiert sie mittels F_DWORD_TO_UDINT und speichert sie persistent im NVS-Speicher mittels INI-Baustein. Bei Statusänderungen oder Initialisierung werden die Werte über Q_NumericValue angezeigt.

## Programmablauf und Verbindungen

**Lernziele:**
- Verständnis der numerischen Werteingabe und -verarbeitung
- Umgang mit Datentypkonvertierungen (DWORD zu UDINT)
- Implementierung von persistenter Datenspeicherung mit NVS
- Anzeige von numerischen Werten auf der Visualisierungsoberfläche
- Verwendung von Statusüberwachung für die Visualisierung

**Schwierigkeitsgrad:** Mittel

**Benötigte Vorkenntnisse:**
- Grundkenntnisse in 4diac-IDE
- Verständnis von Funktionsbausteinen und Event-/Datenverbindungen
- Grundwissen über Datentypen in IEC 61499

**Programmstart:**
Die Übung wird in der 4diac-IDE geladen und auf einem geeigneten Zielgerät ausgeführt. Der numerische Eingabewert kann über die konfigurierte Visualisierungsoberfläche (InputNumber_I1) geändert werden.

**Verbindungsablauf:**
1. Bei Eingabe eines neuen numerischen Werts löst InputNumber_I1 das IND-Ereignis aus
2. F_DWORD_TO_UDINT konvertiert den Wert und triggert INI.SET
3. INI speichert den Wert im NVS-Speicher unter dem konfigurierten Schlüssel
4. Bei Initialisierung oder Statusänderung werden gespeicherte Werte über Q_NumericValue angezeigt
5. CbVtStatus überwacht den Visualisierungsstatus und aktualisiert die Anzeige bei Bedarf

## Zusammenfassung
Diese Übung vermittelt praxisnah die Verarbeitung und persistente Speicherung numerischer Eingabewerte in 4diac. Der Schwerpunkt liegt auf der Integration von Eingabekomponenten, Datentypkonvertierung, NVS-Speicherung und Visualisierungsaktualisierung. Die Standardkonfiguration verwendet den Anfangswert 55, der bei Programmstart geladen wird.