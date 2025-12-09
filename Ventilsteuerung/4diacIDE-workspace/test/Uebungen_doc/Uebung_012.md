# Uebung_012: Numeric Value Input und Speichern

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung und Speicherung numerischer Eingabewerte in einem 4diac-System. Der Fokus liegt auf der Konvertierung von Datentypen, der persistenten Speicherung von Werten und der Anzeige der gespeicherten Daten.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

**InputNumber_I1** (Typ: NumericValue_ID)
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::InputNumber_I1

**F_DWORD_TO_UDINT** (Typ: F_DWORD_TO_UDINT)
- Datentyp-Konvertierungsbaustein

**NVS** (Typ: NVS) - Non-Volatile Storage
- **Parameter**:
  - QI = TRUE
  - KEY = NVS_Keys::KEY_I1_STORE
  - DEFAULT_VALUE = UDINT#0

**Q_NumericValue** (Typ: Q_NumericValue)
- **Parameter**:
  - u16ObjId = DefaultPool::InputNumber_I1

**CbVtStatus** (Typ: CbVtStatus)
- Statusüberwachungsbaustein

## Programmablauf und Verbindungen

### Ereignisverbindungen:
1. InputNumber_I1.IND → F_DWORD_TO_UDINT.REQ
2. F_DWORD_TO_UDINT.CNF → NVS.SET
3. NVS.GETO → Q_NumericValue.REQ
4. CbVtStatus.IND → Q_NumericValue.REQ
5. NVS.INITO → NVS.GET (Rückkopplung)

### Datenverbindungen:
1. InputNumber_I1.IN → F_DWORD_TO_UDINT.IN
2. F_DWORD_TO_UDINT.OUT → NVS.VALUE
3. NVS.VALUEO → Q_NumericValue.u32NewValue

### Ablaufbeschreibung:
1. Bei einer numerischen Eingabe über InputNumber_I1 wird ein IND-Ereignis ausgelöst
2. Der Wert wird über F_DWORD_TO_UDINT konvertiert
3. Der konvertierte Wert wird im NVS-Baustein unter dem Schlüssel KEY_I1_STORE gespeichert
4. Beim Systemstart (CbVtStatus.IND) und nach Speichervorgängen wird der gespeicherte Wert angezeigt
5. Der NVS-Baustein initialisiert sich selbst und lädt den gespeicherten Wert

**Schwierigkeitsgrad**: Einfach bis Mittel  
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Datentypen  
**Start der Übung**: Das System startet automatisch und zeigt den gespeicherten Wert an. Neue Werte können über den NumericValue-Input eingegeben werden.

## Zusammenfassung
Diese Übung vermittelt praktische Kenntnisse in der Verarbeitung numerischer Eingaben, Datentypkonvertierung und persistenter Datenspeicherung in 4diac-Systemen. Die Schüler lernen den Umgang mit Non-Volatile Storage und die Verknüpfung von Eingabe-, Verarbeitungs- und Ausgabebausteinen in einem komplett funktionierenden System.