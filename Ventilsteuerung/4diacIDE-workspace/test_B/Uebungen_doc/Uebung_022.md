# Uebung_022: Spiegelabfolge (2)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung einer Zylinderabfolge mit zwei Zylindern. Das Programm realisiert eine spezifische Abfolge von Ausfahrbewegungen, die durch Softkeys gesteuert werden.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalOutput_Q1** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q1
  - Steuert den digitalen Ausgang für Zylinder 1

- **DigitalOutput_Q2** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Q2
  - Steuert den digitalen Ausgang für Zylinder 2

- **SoftKey_UP_F1** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F1, InputEvent = SoftKeyActivationCode::SK_RELEASED
  - Erfasst das Loslassen der F1-Taste

- **SoftKey_F2_DOWN** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F2, InputEvent = SoftKeyActivationCode::SK_PRESSED
  - Erfasst das Drücken der F2-Taste

- **SoftKey_F3_DOWN** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F3, InputEvent = SoftKeyActivationCode::SK_PRESSED
  - Erfasst das Drücken der F3-Taste

- **E_SR_Ausfahren_Cyl_1** (Typ: E_SR)
  - Set-Reset-Flipflop für Zylinder 1

- **E_SR_Ausfahren_Cyl_2** (Typ: E_SR)
  - Set-Reset-Flipflop für Zylinder 2

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- SoftKey_UP_F1.IND → E_SR_Ausfahren_Cyl_1.S (Setzt Zylinder 1)
- SoftKey_F2_DOWN.IND → E_SR_Ausfahren_Cyl_1.R (Rücksetzt Zylinder 1)
- SoftKey_F2_DOWN.IND → E_SR_Ausfahren_Cyl_2.S (Setzt Zylinder 2)
- SoftKey_F3_DOWN.IND → E_SR_Ausfahren_Cyl_2.R (Rücksetzt Zylinder 2)
- E_SR_Ausfahren_Cyl_1.EO → DigitalOutput_Q1.REQ (Aktiviert Ausgang für Zylinder 1)
- E_SR_Ausfahren_Cyl_2.EO → DigitalOutput_Q2.REQ (Aktiviert Ausgang für Zylinder 2)

### Datenverbindungen:
- E_SR_Ausfahren_Cyl_1.Q → DigitalOutput_Q1.OUT (Datenausgang Zylinder 1)
- E_SR_Ausfahren_Cyl_2.Q → DigitalOutput_Q2.OUT (Datenausgang Zylinder 2)

### Bedienablauf:
1. **START-Knopf**: Loslassen der F1-Taste startet den Prozess
2. **Zylinder 1 Ausfahren**: Wird durch F1-Loslassen aktiviert
3. **Zylinder 1 Einfahren**: Wird durch F2-Drücken deaktiviert
4. **Zylinder 2 Ausfahren**: Wird gleichzeitig mit Zylinder 1 Einfahren aktiviert
5. **Zylinder 2 Einfahren**: Wird durch F3-Drücken deaktiviert

## Zusammenfassung
Diese Übung vermittelt die Grundlagen der Zylindersteuerung mit Set-Reset-Flipflops und demonstriert die Abhängigkeit zwischen verschiedenen Zylinderbewegungen. Die Verwendung von Softkeys zur Prozesssteuerung und die Kaskadierung von Zylinderbewegungen sind zentrale Lerninhalte dieser Übung.