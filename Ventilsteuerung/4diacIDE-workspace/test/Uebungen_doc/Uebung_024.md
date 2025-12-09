# Uebung_024: Spiegelabfolge (4)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Steuerung für eine Spiegelabfolge mit zwei Zylindern. Die Anwendung demonstriert die sequenzielle Steuerung von pneumatischen Zylindern mit Endlagenerkennung und zeitgesteuerten Abläufen.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

**DigitalOutput_Q1, Q2, Q3, Q4** (logiBUS_QX)
- **Parameter**: 
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1, Q2, Q3, Q4

**SoftKey_IE Bausteine** (Softkey_IE)
- SoftKey_UP_F1, SoftKey_F2_DOWN, SoftKey_F3_DOWN, SoftKey_F8_DOWN, SoftKey_F9_DOWN
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::SoftKey_F1, F2, F3, F8, F9
  - InputEvent = SoftKeyActivationCode::SK_RELEASED/SK_PRESSED

**E_SR Bausteine** (E_SR)
- E_SR_Ausfahren_Cyl_1, E_SR_Ausfahren_Cyl_2, E_SR_Einfahren_Cyl_1, E_SR_Einfahren_Cyl_2

**E_DELAY** (E_DELAY)
- **Parameter**: DT = T#2s (2 Sekunden Verzögerung)

## Programmablauf und Verbindungen

### Ablaufsequenz:

1. **Start Ausfahren Zylinder 1**
   - SoftKey_F1 (released) → E_SR_Ausfahren_Cyl_1.S
   - Aktiviert DigitalOutput_Q1 (Ausfahren_Cyl_1)

2. **Ausfahren Zylinder 2**
   - SoftKey_F2 (pressed) → E_SR_Ausfahren_Cyl_2.S
   - Aktiviert DigitalOutput_Q2 (Ausfahren_Cyl_2)

3. **Rückzug Zylinder 2**
   - SoftKey_F3 (pressed) → E_SR_Ausfahren_Cyl_2.R
   - Gleichzeitig Start E_DELAY Timer

4. **Zeitgesteuertes Einfahren Zylinder 2**
   - Nach 2 Sekunden (E_DELAY) → E_SR_Einfahren_Cyl_2.S
   - Aktiviert DigitalOutput_Q3 (Einfahren_Cyl_2)

5. **Einfahren Zylinder 1**
   - SoftKey_F8 (pressed) → E_SR_Einfahren_Cyl_1.S
   - Aktiviert DigitalOutput_Q4 (Einfahren_Cyl_1)

6. **Reset Zylinder 1**
   - SoftKey_F9 (pressed) → E_SR_Einfahren_Cyl_1.R

### Ereignisverbindungen:
- SoftKey-Ereignisse steuern Set/Reset der E_SR Bausteine
- E_SR Ausgänge aktivieren DigitalOutputs
- Zeitverzögerung zwischen Zylinder 2 Rückzug und Einfahren

### Datenverbindungen:
- E_SR.Q Ausgänge verbunden mit DigitalOutput.OUT
- Sicherstellung des korrekten Signalflusses

## Lernziele
- Verständnis von Set-Reset-Funktionsbausteinen (E_SR)
- Implementierung zeitgesteuerter Abläufe mit E_DELAY
- Steuerung von Softkeys für Benutzerinteraktion
- Sequenzielle Steuerung mehrerer Aktoren
- Endlagenerkennung und -verarbeitung

## Schwierigkeitsgrad
Mittel - Erfordert Verständnis von Zustandsautomaten und zeitgesteuerten Abläufen

## Vorkenntnisse
- Grundlagen der 4diac-IDE
- Verständnis von E_SR und E_DELAY Bausteinen
- Kenntnisse über Softkey-Implementation

## Zusammenfassung
Diese Übung demonstriert eine komplexe Spiegelabfolge mit zwei Zylindern, die sequenziell gesteuert werden. Besonderes Merkmal ist die zeitgesteuerte Verzögerung zwischen den Zylinderbewegungen und die Verwendung von Softkeys für die Benutzersteuerung. Die Anwendung zeigt praxisnah die Steuerung pneumatischer Systeme mit Endlagenerkennung.