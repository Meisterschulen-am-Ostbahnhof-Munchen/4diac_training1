# Uebung_020c2: DigitalInput_I1 auf DigitalOutput_Q1; E_TON Einschaltverzögert; Zeit eingeben und speichern.

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung einer einschaltverzögerten Zeitsteuerung mit E_TON-Funktionsbaustein. Das System ermöglicht das Eingeben und Speichern einer Verzögerungszeit, die dann auf die Schaltvorgänge angewendet wird.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_I1** (logiBUS_IX): Liest den digitalen Eingang I1 ein
- **E_TON**: Einschaltverzögerter Timer
- **DigitalOutput_Q1** (logiBUS_QX): Steuert den digitalen Ausgang Q1
- **F_MULTIME**: Multiplikationsbaustein für Zeitwerte
- **Uebung_020c2_sub**: Sub-Applikation für Zeitverwaltung

### Sub-Bausteine: Uebung_020c2_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **InputNumber_I1** (NumericValue_ID)
        - Parameter: QI = TRUE, u16ObjId = DefaultPool::InputNumber_I1
        - Ereignisausgang/-eingang: IND → F_DWORD_TO_UDINT.REQ
        - Datenausgang/-eingang: IN → F_DWORD_TO_UDINT.IN
    
    - **F_DWORD_TO_UDINT** (F_DWORD_TO_UDINT)
        - Ereignisausgang/-eingang: CNF → NVS_UDINT.SET
        - Datenausgang/-eingang: IN ← InputNumber_I1.IN, OUT → NVS_UDINT.VALUE
    
    - **NVS_UDINT** (NVS)
        - Parameter: QI = TRUE, DEFAULT_VALUE = UDINT#0
        - Ereignisausgang/-eingang: SETO → IND, GETO → Q_NumericValue.REQ, GETO → IND, INITO → GET
        - Datenausgang/-eingang: KEY ← KEY, VALUEO → Q_NumericValue.u32NewValue, VALUEO → VALUEO
    
    - **Q_NumericValue** (Q_NumericValue)
        - Ereignisausgang/-eingang: REQ ← REQ
        - Datenausgang/-eingang: u16ObjId ← u16ObjId, u32NewValue ← NVS_UDINT.VALUEO

- **Funktionsweise**: Die Sub-Applikation verwaltet die Zeitwerteingabe über eine numerische Eingabe, konvertiert den Wert und speichert ihn im NVS (Non-Volatile Storage). Bei Anforderung wird der gespeicherte Wert ausgegeben.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_TON.REQ
- E_TON.CNF → DigitalOutput_Q1.REQ
- Uebung_020c2_sub.IND → F_MULTIME.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_TON.IN
- E_TON.Q → DigitalOutput_Q1.OUT
- F_MULTIME.OUT → E_TON.PT
- Uebung_020c2_sub.VALUEO → F_MULTIME.IN2

**Programmablauf:**
1. Beim Betätigen des digitalen Eingangs I1 wird das IND-Ereignis ausgelöst
2. Der E_TON-Timer startet mit der eingestellten Verzögerungszeit
3. Nach Ablauf der Verzögerungszeit wird der digitale Ausgang Q1 aktiviert
4. Die Verzögerungszeit wird durch die Sub-Applikation verwaltet und kann konfiguriert werden

**Parameterkonfiguration:**
- F_MULTIME.IN1 ist auf T#1s voreingestellt
- Die Verzögerungszeit ergibt sich aus der Multiplikation von IN1 und IN2
- Der Sub-Baustein verwendet KEY_I1_STORE für die Speicherung

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Ein-/Ausgänge, Timer-Funktionen

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit einschaltverzögerten Timern und der persistenten Speicherung von Parametern. Die Kombination aus E_TON-Baustein, Zeitmultiplikation und NVS-Speicherung zeigt eine typische industrielle Anwendung für konfigurierbare Verzögerungszeiten. Die Übung deckt wichtige Konzepte der SPS-Programmierung ab, darunter Ereignissteuerung, Datenkonvertierung und Parameterpersistenz.