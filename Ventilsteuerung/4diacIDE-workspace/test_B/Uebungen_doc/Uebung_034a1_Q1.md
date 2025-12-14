# Uebung_034a1_Q1: Numeric Value Input auf PWM Ausgang

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Umwandlung eines numerischen Eingabewerts in ein PWM-Signal (Pulsweitenmodulation). Die Anwendung ermöglicht es, über eine numerische Eingabekomponente einen Wert zu setzen, der dann als PWM-Signal ausgegeben wird.

## Verwendete Funktionsbausteine (FBs)

### PWM_Value (NumericValue_ID)
- **Typ**: NumericValue_ID
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool_PWM::InputNumber_PWM_Value
- **Funktionsweise**: Dieser Baustein dient zur Eingabe eines numerischen Wertes über eine Benutzeroberfläche. Bei Bestätigung der Eingabe mit OK wird das IND-Ereignis ausgelöst.

### PWMOutput_Q1 (logiBUS_QD_PWM)
- **Typ**: logiBUS_QD_PWM
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktionsweise**: Dieser Baustein erzeugt ein PWM-Signal basierend auf dem empfangenen Eingangswert und gibt es auf dem konfigurierten Ausgang aus.

### F_DWORD_TO_UDINT (F_DWORD_TO_UDINT)
- **Typ**: F_DWORD_TO_UDINT
- **Funktionsweise**: Dieser Baustein konvertiert einen DWORD-Wert in einen UDINT-Wert (unsigned double integer).

## Programmablauf und Verbindungen

Das Programm startet mit der numerischen Werteingabe über den PWM_Value-Baustein. Sobald der eingegebene Wert mit OK bestätigt wird, wird das IND-Ereignis ausgelöst. Dieses Ereignis aktiviert sowohl den PWMOutput_Q1-Baustein als auch den F_DWORD_TO_UDINT-Konverter.

Die Datenverbindungen übertragen den eingegebenen Wert (IN) parallel zu beiden Bausteinen:
- Direkt zum PWMOutput_Q1 für die PWM-Erzeugung
- Zum F_DWORD_TO_UDINT-Konverter für die Datentypumwandlung

**Wichtiger Hinweis**: Das IND-Ereignis wird erst ausgelöst, wenn die numerische Eingabe mit OK bestätigt wird, nicht bereits beim Drücken eines Buttons.

**Schwierigkeitsgrad**: Einfach
**Lernziele**: 
- Verständnis der PWM-Signalgenerierung
- Umgang mit numerischen Eingabekomponenten
- Datentypkonvertierung in 4diac
- Ereignisgesteuerte Programmabläufe

## Zusammenfassung
Diese Übung zeigt eine grundlegende Anwendung zur Erzeugung von PWM-Signalen aus numerischen Eingabewerten. Sie vermittelt wichtige Konzepte der ereignisgesteuerten Programmierung und der Datentypkonvertierung in der 4diac-Umgebung. Die parallele Verarbeitung des Eingabewerts für verschiedene Zwecke demonstriert zudem die Flexibilität des IEC 61499-Standards.