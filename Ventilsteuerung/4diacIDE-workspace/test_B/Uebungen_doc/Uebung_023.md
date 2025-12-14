# Uebung_023: Spiegelabfolge (3)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Steuerung für eine Spiegelabfolge mit zwei Zylindern. Das System ermöglicht das unabhängige Ausfahren und Einfahren beider Zylinder über separate Softkeys, wobei die Endlagen der Zylinder über Sensorsignale erfasst werden.

## Verwendete Funktionsbausteine (FBs)

### Softkey-Funktionsbausteine
- **SoftKey_UP_F1** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F1, InputEvent = SK_RELEASED
  - Startet das Ausfahren von Zylinder 1

- **SoftKey_F2_DOWN** (Typ: Softkey_IE)  
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F2, InputEvent = SK_PRESSED
  - Steuert Ausfahren von Zylinder 2 und Rücksetzen von Zylinder 1

- **SoftKey_F3_DOWN** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F3, InputEvent = SK_PRESSED
  - Rücksetzen von Zylinder 2

- **SoftKey_F7_UP** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F7, InputEvent = SK_PRESSED
  - Startet das Einfahren von Zylinder 2

- **SoftKey_F8_DOWN** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F8, InputEvent = SK_PRESSED
  - Steuert Einfahren von Zylinder 1 und Rücksetzen von Zylinder 2

- **SoftKey_F9_DOWN** (Typ: Softkey_IE)
  - Parameter: QI = TRUE, u16ObjId = DefaultPool::SoftKey_F9, InputEvent = SK_PRESSED
  - Rücksetzen von Zylinder 1

### Set-Reset-Funktionsbausteine
- **E_SR_Ausfahren_Cyl_1** (Typ: E_SR)
  - Steuert das Ausfahren von Zylinder 1

- **E_SR_Ausfahren_Cyl_2** (Typ: E_SR)  
  - Steuert das Ausfahren von Zylinder 2

- **E_SR_Einfahren_Cyl_1** (Typ: E_SR)
  - Steuert das Einfahren von Zylinder 1

- **E_SR_Einfahren_Cyl_2** (Typ: E_SR)
  - Steuert das Einfahren von Zylinder 2

### Ausgabebausteine
- **DigitalOutput_Q1** bis **DigitalOutput_Q4** (Typ: logiBUS_QX)
  - Parameter: QI = TRUE
  - Steuern die physischen Ausgänge für die Zylinderbewegungen

## Programmablauf und Verbindungen

### Ausfahrsequenz:
1. **Zylinder 1 ausfahren**: SoftKey_F1 (Released) → E_SR_Ausfahren_Cyl_1.S → DigitalOutput_Q1
2. **Zylinder 2 ausfahren**: SoftKey_F2 (Pressed) → E_SR_Ausfahren_Cyl_2.S → DigitalOutput_Q2
3. **Zylinder 1 zurück**: SoftKey_F2 (Pressed) → E_SR_Ausfahren_Cyl_1.R
4. **Zylinder 2 zurück**: SoftKey_F3 (Pressed) → E_SR_Ausfahren_Cyl_2.R

### Einfahrsequenz:
1. **Zylinder 2 einfahren**: SoftKey_F7 (Pressed) → E_SR_Einfahren_Cyl_2.S → DigitalOutput_Q3
2. **Zylinder 1 einfahren**: SoftKey_F8 (Pressed) → E_SR_Einfahren_Cyl_1.S → DigitalOutput_Q4
3. **Zylinder 2 zurück**: SoftKey_F8 (Pressed) → E_SR_Einfahren_Cyl_2.R
4. **Zylinder 1 zurück**: SoftKey_F9 (Pressed) → E_SR_Einfahren_Cyl_1.R

### Lernziele:
- Verständnis von Set-Reset-Funktionsbausteinen (E_SR)
- Implementierung unabhängiger Zylindersteuerungen
- Umgang mit Softkey-Eingaben
- Strukturierung komplexer Ablaufsteuerungen

### Schwierigkeitsgrad:
Mittel - erfordert Grundkenntnisse in SPS-Programmierung und Verständnis von Set-Reset-Logik

## Zusammenfassung
Die Übung demonstriert eine erweiterte Spiegelabfolge-Steuerung mit zwei unabhängig steuerbaren Zylindern. Durch die Verwendung von E_SR-Bausteinen und Softkey-Steuerung wird eine flexible und sichere Steuerung implementiert, die sowohl das Ausfahren als auch das Einfahren beider Zylinder in beliebiger Reihenfolge ermöglicht. Die klare Trennung der Steuerfunktionen erleichtert die Wartung und Erweiterbarkeit des Systems.