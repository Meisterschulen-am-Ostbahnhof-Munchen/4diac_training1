# Uebung_039b: Spiegelabfolge V2 mit Schrittkette

* * * * * * * * * *

## Einleitung

Diese Übung implementiert eine Spiegelabfolge-Steuerung mit Schrittkette, die für hydraulische Ringsysteme mit 3/2-Wege-Ventilen (z.B. Claas) oder pneumatische 5/2-Wege-Ventile geeignet ist. Die Steuerung realisiert eine zeitgesteuerte Abfolge von Ausgängen mit unterschiedlichen Zeitparametern.

## Verwendete Funktionsbausteine (FBs)

### DigitalOutput_Q1 / DigitalOutput_Q2
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Digitale Ausgänge für die Ansteuerung der Ventile

### SoftKey_F1
- **Typ**: Softkey_IX
- **Parameter**:
  - QI = TRUE
  - u16ObjId = DefaultPool::SoftKey_F1
- **Funktion**: Software-Taste zum Starten der Abfolge

### E_TP_Q1
- **Typ**: E_TP (Impulsgeber)
- **Parameter**:
  - PT = T#8s
- **Funktion**: Erzeugt einen 8-Sekunden-Impuls für Ausgang Q1

### E_TP_Q2
- **Typ**: E_TP (Impulsgeber)
- **Parameter**:
  - PT = T#4s
- **Funktion**: Erzeugt einen 4-Sekunden-Impuls für Ausgang Q2

### E_TON
- **Typ**: E_TON (Zeitverzögerung Einschaltverzögerung)
- **Parameter**:
  - PT = T#2s
- **Funktion**: Realisiert eine 2-Sekunden-Verzögerung zwischen den Schritten

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_F1.IND → E_TP_Q1.REQ (Startimpuls)
- E_TP_Q1.CNF → DigitalOutput_Q1.REQ (Aktivierung Q1)
- E_TP_Q1.CNF → E_TON.REQ (Start Verzögerung)
- E_TON.CNF → E_TP_Q2.REQ (Aktivierung Q2)
- E_TP_Q2.CNF → DigitalOutput_Q2.REQ (Aktivierung Q2)

**Datenverbindungen:**
- E_TP_Q1.Q → DigitalOutput_Q1.OUT (Signal Q1)
- E_TP_Q1.Q → E_TON.IN (Verzögerungs-Steuersignal)
- E_TON.Q → E_TP_Q2.IN (Start Q2)
- E_TP_Q2.Q → DigitalOutput_Q2.OUT (Signal Q2)
- SoftKey_F1.IN → E_TP_Q1.IN (Start-Steuersignal)

**Ablauf:**
1. Betätigung der SoftKey_F1 startet die Abfolge
2. Q1 wird für 8 Sekunden aktiviert
3. Nach 8 Sekunden startet eine 2-Sekunden-Verzögerung
4. Nach der Verzögerung wird Q2 für 4 Sekunden aktiviert
5. Die Abfolge endet nach Abschluss von Q2

**Lernziele:**
- Verständnis von Schrittketten-Programmierung
- Zeitgesteuerte Abläufe mit E_TP und E_TON
- Verwendung von Software-Tasten zur Prozesssteuerung
- Ansteuerung digitaler Ausgänge

## Zusammenfassung

Diese Übung demonstriert eine typische Schrittkette mit zeitgesteuerten Abläufen für industrielle Anwendungen. Die Kombination aus Impulsgebern (E_TP) und Verzögerungsbausteinen (E_TON) ermöglicht präzise zeitgesteuerte Abfolgen, wie sie in vielen Automatisierungsprozessen benötigt werden. Die Steuerung ist besonders geeignet für Ventilsteuerungen in hydraulischen oder pneumatischen Systemen.