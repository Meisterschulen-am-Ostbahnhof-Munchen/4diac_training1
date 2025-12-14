# Uebung_015a: Object Pointer umschalten -- 3-fach

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Umschaltung von Object Pointern in einer 3-fach Auswahlkonfiguration. Die Anwendung ermöglicht die Auswahl zwischen verschiedenen Objekt-IDs über Softkeys und die Übergabe der entsprechenden Werte an einen numerischen Anzeigebaustein.

## Verwendete Funktionsbausteine (FBs)

### Softkey_IE Bausteine
- **SoftKey_UP_F1**: Verarbeitet die Freigabe der F1-Taste
- **SoftKey_UP_F2**: Verarbeitet die Freigabe der F2-Taste  
- **SoftKey_UP_F3**: Verarbeitet die Freigabe der F3-Taste

### F_UINT_TO_UDINT Bausteine
- **F_UINT_TO_UDINT**: Konvertiert den Wert von Button_A1 von UINT zu UDINT
- **F_UINT_TO_UDINT_1**: Konvertiert den Wert von Button_A2 von UINT zu UDINT

### F_SEL_E_3 Baustein
- **F_SEL_E_3**: 3-fach Selektor für Ereignisse und Daten

### Q_NumericValue Baustein
- **Q_NumericValue**: Numerischer Anzeigebaustein für ObjectPointer_P1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- F_SEL_E_3.CNF → Q_NumericValue.REQ
- SoftKey_UP_F1.IND → F_SEL_E_3.REQ0
- SoftKey_UP_F2.IND → F_SEL_E_3.REQ1
- SoftKey_UP_F3.IND → F_SEL_E_3.REQ2

**Datenverbindungen:**
- F_UINT_TO_UDINT.OUT → F_SEL_E_3.IN1
- F_SEL_E_3.OUT → Q_NumericValue.u32NewValue
- F_UINT_TO_UDINT_1.OUT → F_SEL_E_3.IN2

**Parameterkonfiguration:**
- Softkeys sind mit den entsprechenden Tasten F1, F2, F3 verknüpft
- F_SEL_E_3.IN0 ist auf isobus::ID_NULL initialisiert
- Q_NumericValue zeigt auf ObjectPointer_P1

## Zusammenfassung
Die Übung zeigt eine typische Anwendung für die Umschaltung zwischen verschiedenen Objekt-Pointern mittels Softkey-Bedienung. Der 3-fach Selektor ermöglicht die Auswahl zwischen drei verschiedenen Eingabequellen, wobei die konvertierten Werte der Buttons A1 und A2 sowie ein Null-Wert zur Verfügung stehen. Die Lösung demonstriert grundlegende Konzepte der Ereignissteuerung und Datenkonvertierung in 4diac-Systemen.