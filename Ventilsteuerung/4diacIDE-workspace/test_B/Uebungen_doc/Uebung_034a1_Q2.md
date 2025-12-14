# Uebung_034a1_Q2: Numeric Value Input auf PWM Ausgang

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines numerischen Wert-Eingabefelds zur Steuerung eines PWM-Ausgangs. Die Anwendung ermöglicht es, über eine numerische Eingabe einen PWM-Wert zu definieren und diesen an einen spezifischen Ausgang zu senden.

## Verwendete Funktionsbausteine (FBs)

### PWM_Value (NumericValue_ID)
- **Typ**: NumericValue_ID
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool_PWM::InputNumber_PWM_Value
- **Funktionsweise**: Dieser Baustein ermöglicht die numerische Werteingabe über eine Benutzeroberfläche. Bei Bestätigung der Eingabe mit OK wird das IND-Ereignis ausgelöst.

### PWMOutput_Q2 (logiBUS_QD_PWM)
- **Typ**: logiBUS_QD_PWM
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q2
- **Funktionsweise**: Dieser Baustein steuert den PWM-Ausgang Q2 auf dem logiBUS-System und gibt den empfangenen Wert als PWM-Signal aus.

### F_DWORD_TO_UDINT (F_DWORD_TO_UDINT)
- **Typ**: F_DWORD_TO_UDINT
- **Funktionsweise**: Dieser Konvertierungsbaustein wandelt DWORD-Daten in UDINT-Daten um und wird für die Datenverarbeitung zwischen den Komponenten verwendet.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- PWM_Value.IND → PWMOutput_Q2.REQ
- PWM_Value.IND → F_DWORD_TO_UDINT.REQ

**Datenverbindungen:**
- PWM_Value.IN → F_DWORD_TO_UDINT.IN
- PWM_Value.IN → PWMOutput_Q2.OUT

**Wichtiger Hinweis:**
Das IND-Ereignis wird erst ausgelöst, wenn die numerische Eingabe mit OK bestätigt wird, nicht bereits beim Drücken eines Buttons.

**Lernziele:**
- Verwendung von numerischen Eingabefeldern in 4diac
- PWM-Ausgangssteuerung
- Datenkonvertierung zwischen verschiedenen Datentypen
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad:** Einfach bis mittel

**Benötigte Vorkenntnisse:**
- Grundkenntnisse in 4diac IDE
- Verständnis von Ereignis- und Datenverbindungen
- Grundlagen der PWM-Signalgebung

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung zur Steuerung eines PWM-Ausgangs über eine numerische Eingabeschnittstelle. Sie verdeutlicht die Ereignissteuerung in 4diac und die Verarbeitung von Benutzereingaben in Echtzeit-Steuerungssystemen. Die Implementierung demonstriert wichtige Konzepte der industriellen Automatisierungstechnik.