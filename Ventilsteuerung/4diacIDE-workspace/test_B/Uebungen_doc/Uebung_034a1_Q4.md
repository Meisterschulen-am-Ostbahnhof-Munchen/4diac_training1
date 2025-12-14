# Uebung_034a1_Q4: Numeric Value Input auf PWM Ausgang

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Umwandlung eines numerischen Eingabewerts in ein PWM-Signal (Pulsweitenmodulation). Die Anwendung ermöglicht es, über eine numerische Eingabekomponente einen Wert einzugeben, der dann in ein entsprechendes PWM-Signal umgewandelt und ausgegeben wird.

## Verwendete Funktionsbausteine (FBs)

### PWM_Value (NumericValue_ID)
- **Typ**: NumericValue_ID
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool_PWM::InputNumber_PWM_Value
- **Funktionsweise**: Dieser Baustein dient zur Erfassung numerischer Eingabewerte. Bei Bestätigung der Eingabe mit OK generiert er ein IND-Ereignis.

### F_DWORD_TO_UDINT
- **Typ**: F_DWORD_TO_UDINT
- **Funktionsweise**: Konvertiert einen DWORD-Datentyp in einen UDINT-Datentyp. Dieser Baustein wird für die Datentypumwandlung zwischen den verschiedenen Komponenten benötigt.

### PWMOutput_Q4 (logiBUS_QD_PWM)
- **Typ**: logiBUS_QD_PWM
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q4
- **Funktionsweise**: Erzeugt ein PWM-Signal basierend auf dem empfangenen Eingabewert und gibt es auf dem spezifizierten Ausgang aus.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- PWM_Value.IND → PWMOutput_Q4.REQ
- PWM_Value.IND → F_DWORD_TO_UDINT.REQ

**Datenverbindungen:**
- PWM_Value.IN → F_DWORD_TO_UDINT.IN
- PWM_Value.IN → PWMOutput_Q4.OUT

**Wichtiger Hinweis:** Das IND-Ereignis wird erst generiert, wenn die numerische Eingabe mit OK bestätigt wird, nicht bereits beim Drücken eines Buttons.

**Lernziele:**
- Verständnis der PWM-Signalgenerierung
- Umgang mit numerischen Eingabekomponenten
- Datentypkonvertierung zwischen verschiedenen Formaten
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad:** Einfach bis mittel

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen und deren Parametern
- Grundkenntnisse über PWM-Signale

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung zur Umwandlung numerischer Eingabewerte in PWM-Signale. Durch die Verwendung spezialisierter Funktionsbausteine für Eingabe, Datentypkonvertierung und Signalausgabe wird ein kompletter Signalverarbeitungsprozess abgebildet. Die Übung vermittelt wichtige Konzepte der ereignisgesteuerten Programmierung und der Signalverarbeitung in industriellen Steuerungssystemen.