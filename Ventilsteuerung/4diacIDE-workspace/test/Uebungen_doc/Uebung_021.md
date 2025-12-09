# Uebung_021: Spiegelabfolge (1)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert eine grundlegende Steuerungslogik für eine Spiegelabfolge mit Start- und Stopp-Funktionalität. Die Anwendung verwendet Softkeys zur Aktivierung und Deaktivierung eines digitalen Ausgangs.

## Verwendete Funktionsbausteine (FBs)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1

### SoftKey_UP_F1
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::SoftKey_F1
  - InputEvent = SoftKeyActivationCode::SK_RELEASED

### E_SR
- **Typ**: E_SR (Set-Reset Flip-Flop)

### SoftKey_F2_DOWN
- **Typ**: Softkey_IE
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::SoftKey_F2
  - InputEvent = SoftKeyActivationCode::SK_PRESSED

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → E_SR.S (Set-Eingang)
- SoftKey_F2_DOWN.IND → E_SR.R (Reset-Eingang)
- E_SR.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_SR.Q → DigitalOutput_Q1.OUT

**Funktionsweise:**
- SoftKey_F1 (START-Knopf) beim Loslassen setzt den Flip-Flop
- SoftKey_F2 (Endlage) beim Drücken resettet den Flip-Flop
- Der E_SR Baustein steuert den digitalen Ausgang Q1 basierend auf dem Set/Reset-Zustand

**Lernziele:**
- Verständnis von Set-Reset Flip-Flops
- Umgang mit Softkey-Eingaben
- Steuerung digitaler Ausgänge
- Ereignis- und Datenverbindungen in 4diac

**Schwierigkeitsgrad**: Einfach
**Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen

## Zusammenfassung

Diese Übung zeigt eine grundlegende Steuerungslogik mit Set-Reset-Funktionalität. Der digitale Ausgang Q1 wird durch das Loslassen des F1-Softkeys aktiviert und durch das Drücken des F2-Softkeys deaktiviert. Die Übung vermittelt essentielle Konzepte der Ereignissteuerung und digitalen Signalverarbeitung in 4diac.