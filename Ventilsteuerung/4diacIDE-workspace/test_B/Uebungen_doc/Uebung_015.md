# Uebung_015: Object Pointer umschalten

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Umschaltung eines Object Pointers zwischen zwei verschiedenen Werten. Die Steuerung erfolgt über Softkeys, wobei die Auswahl zwischen einem Null-Wert und einem konvertierten Button-Wert getroffen werden kann.

## Verwendete Funktionsbausteine (FBs)

### Softkey_IE
- **Typ**: Softkey_IE
- **Funktionsweise**: Verarbeitet Softkey-Ereignisse und gibt entsprechende Indikationsereignisse aus

### E_SR
- **Typ**: E_SR (Set-Reset-Flipflop)
- **Funktionsweise**: Speichert den Zustand basierend auf Set- und Reset-Eingängen

### F_UINT_TO_UDINT
- **Typ**: F_UINT_TO_UDINT
- **Funktionsweise**: Konvertiert einen 16-Bit unsigned integer Wert in einen 32-Bit unsigned integer Wert

### F_SEL
- **Typ**: F_SEL (Selektor)
- **Funktionsweise**: Wählt zwischen zwei Eingangswerten basierend auf einem Steuersignal aus

### Q_NumericValue
- **Typ**: Q_NumericValue
- **Funktionsweise**: Schreibt numerische Werte in ein Objekt im DefaultPool

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_F1 (Released) → E_SR (Set)
- SoftKey_F2 (Released) → E_SR (Reset)
- E_SR (EO) → F_SEL (REQ)
- F_SEL (CNF) → Q_NumericValue (REQ)

**Datenverbindungen:**
- F_UINT_TO_UDINT (OUT) → F_SEL (IN1)
- E_SR (Q) → F_SEL (G)
- F_SEL (OUT) → Q_NumericValue (u32NewValue)

**Parameterkonfiguration:**
- SoftKey_F1: Object ID = DefaultPool::SoftKey_F1, InputEvent = SK_RELEASED
- SoftKey_F2: Object ID = DefaultPool::SoftKey_F2, InputEvent = SK_RELEASED
- F_UINT_TO_UDINT: IN = DefaultPool::Button_A1
- F_SEL: IN0 = isobus::ID_NULL
- Q_NumericValue: u16ObjId = DefaultPool::ObjectPointer_P1

**Ablauf:**
1. Drücken von SoftKey_F1 setzt das E_SR Flipflop
2. Drücken von SoftKey_F2 resetet das E_SR Flipflop
3. Der Ausgang Q von E_SR steuert die Selektion in F_SEL
4. Bei Q=1 wird IN1 (konvertierter Button_A1 Wert) ausgewählt
5. Bei Q=0 wird IN0 (Null-Wert) ausgewählt
6. Der selektierte Wert wird an ObjectPointer_P1 geschrieben

## Zusammenfassung
Diese Übung zeigt die praktische Anwendung eines Set-Reset-Flipflops in Kombination mit einem Selektor-Baustein zur dynamischen Auswahl zwischen verschiedenen Werten. Die Umschaltung erfolgt über Softkeys, wobei zwischen einem Null-Wert und einem konvertierten Button-Wert gewählt werden kann. Die Übung vermittelt grundlegende Konzepte der Signalverarbeitung und dynamischen Wertauswahl in 4diac.