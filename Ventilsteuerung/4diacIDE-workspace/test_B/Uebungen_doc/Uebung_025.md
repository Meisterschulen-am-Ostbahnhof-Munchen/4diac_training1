# Uebung_025: Spiegelabfolge (5)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Steuerung für eine Spiegelabfolge mit zwei Zylindern. Das System steuert das Ausfahren und Einfahren der beiden Zylinder in einer festgelegten Abfolge mit zeitgesteuerten Abläufen und Endlagenerkennung.

## Verwendete Funktionsbausteine (FBs)

### Softkey-Funktionsbausteine
- **SoftKey_UP_F1** (Typ: Softkey_IE) - Start-Knopf für Ausfahren
- **SoftKey_F2_DOWN** (Typ: Softkey_IE) - F2-Taste für Zylindersteuerung
- **SoftKey_F3_DOWN** (Typ: Softkey_IE) - F3-Taste für Zylindersteuerung  
- **SoftKey_F8_DOWN** (Typ: Softkey_IE) - F8-Taste für Einfahren
- **SoftKey_F9_DOWN** (Typ: Softkey_IE) - F9-Taste für Einfahren

### Zylindersteuerungs-FBs
- **E_SR_Ausfahren_Cyl_1** (Typ: E_SR) - Set-Reset für Ausfahren Zylinder 1
- **E_SR_Ausfahren_Cyl_2** (Typ: E_SR) - Set-Reset für Ausfahren Zylinder 2
- **E_SR_Einfahren_Cyl_1** (Typ: E_SR) - Set-Reset für Einfahren Zylinder 1
- **E_SR_Einfahren_Cyl_2** (Typ: E_SR) - Set-Reset für Einfahren Zylinder 2

### Ausgabebausteine
- **DigitalOutput_Q1** (Typ: logiBUS_QX) - Ausgang für Zylinder 1 Ausfahren
- **DigitalOutput_Q2** (Typ: logiBUS_QX) - Ausgang für Zylinder 2 Ausfahren
- **DigitalOutput_Q3** (Typ: logiBUS_QX) - Ausgang für Zylinder 2 Einfahren
- **DigitalOutput_Q4** (Typ: logiBUS_QX) - Ausgang für Zylinder 1 Einfahren

### Steuerungs- und Verzögerungs-FBs
- **E_DELAY** (Typ: E_DELAY) - Zeitverzögerung von 2 Sekunden
- **E_REND_Ausfahren_Cyl_1** (Typ: E_REND) - Rücksetzende Flanke für Ausfahren Zylinder 1
- **E_REND_Ausfahren_Cyl_2** (Typ: E_REND) - Rücksetzende Flanke für Ausfahren Zylinder 2
- **E_REND_Einfahren_Cyl_1** (Typ: E_REND) - Rücksetzende Flanke für Einfahren Zylinder 1
- **E_REND_Einfahren_Cyl_2** (Typ: E_REND) - Rücksetzende Flanke für Einfahren Zylinder 2
- **E_SWITCH_Q1-Q4** (Typ: E_SWITCH) - Schalter für Signalverteilung

## Programmablauf und Verbindungen

### Ablaufsequenz:
1. **Start mit F1**: Auslösung des Ausfahrvorgangs für Zylinder 1
2. **Zylinder 1 ausfahren**: Über DigitalOutput_Q1
3. **Endlage Zylinder 1 erreicht**: Signal über E_SWITCH_Q1 an E_REND_Ausfahren_Cyl_1
4. **Zylinder 2 ausfahren**: Nach Bestätigung durch F2-Taste
5. **Endlage Zylinder 2 erreicht**: Signal über E_SWITCH_Q2 an E_REND_Ausfahren_Cyl_2
6. **Zeitverzögerung**: 2 Sekunden Wartezeit über E_DELAY
7. **Zylinder 2 einfahren**: Nach Ablauf der Verzögerung
8. **Zylinder 1 einfahren**: Nach Bestätigung durch F8-Taste
9. **Zyklusende**: Rückkehr in Ausgangsposition

### Wichtige Verbindungen:
- Softkey-Ereignisse lösen Set/Reset-Operationen aus
- E_SR-Bausteine steuern die Digitalausgänge
- E_REND-Bausteine ermöglichen Rücksetzvorgänge
- E_SWITCH-Bausteine verteilen Signale an die entsprechenden REND-Bausteine
- Zeitgesteuerte Abläufe über E_DELAY mit 2 Sekunden Verzögerung

### Lernziele:
- Verständnis von Set-Reset-Funktionsbausteinen
- Implementierung von Ablaufsteuerungen
- Zeitgesteuerte Prozesse
- Endlagenerkennung und -verarbeitung
- Softkey-Integration für Benutzerinteraktion

## Zusammenfassung
Die Übung demonstriert eine komplexe Ablaufsteuerung für eine Spiegelabfolge mit zwei Zylindern. Sie kombiniert Benutzereingaben über Softkeys, zeitgesteuerte Abläufe und Endlagenerkennung zu einem vollständigen Steuerungsprozess. Die Implementierung zeigt das Zusammenspiel verschiedener Funktionsbausteine zur Realisierung einer zuverlässigen Ablaufsteuerung in der Automatisierungstechnik.