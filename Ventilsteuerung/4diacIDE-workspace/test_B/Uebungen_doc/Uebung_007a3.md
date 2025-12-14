# Uebung_007a3: Blinker mit E_CYCLE, E_SWITCH und E_SR

* * * * * * * * * *

## Einleitung
Diese Übung implementiert einen Blinker mit der Besonderheit, dass er immer im AUS-Zustand stehen bleibt. Die Schaltung verwendet zyklische Ereignisse und eine Set-Reset-Logik zur Steuerung der Blinkfunktion.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **E_CYCLE**: Zyklischer Ereignisgenerator
- **E_SWITCH**: Ereignis-Weichenschaltung
- **E_SR**: Set-Reset-Flipflop
- **logiBUS_IE**: Eingangsbaustein für Taster
- **logiBUS_QX**: Ausgangsbaustein für Aktoren

### Sub-Bausteine: logiBUS_IE (START/STOP)
- **Typ**: Eingangsbaustein für logiBUS
- **Verwendete interne FBs**: Keine internen FBs
- **Parameter**: 
  - QI = TRUE (aktiviert)
  - Input = logiBUS_DI::Input_I1 (START) / Input_I2 (STOP)
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Ereignisausgang**: IND (Ereignis bei Tastendruck)
- **Funktionsweise**: Erfasst Einzeltastendrücke an den definierten Eingängen

### Sub-Bausteine: logiBUS_QX (DigitalOutput_Q1)
- **Typ**: Ausgangsbaustein für logiBUS
- **Verwendete interne FBs**: Keine internen FBs
- **Parameter**:
  - QI = TRUE (aktiviert)
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingang**: REQ (Anforderung zur Ausgabesteuerung)
- **Dateneingang**: OUT (Ausgabewert)
- **Funktionsweise**: Steuert den physischen Ausgang Q1 basierend auf dem empfangenen Wert

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- START.IND → E_CYCLE.START (Startet Zyklus)
- STOP.IND → E_CYCLE.STOP (Stoppt Zyklus)
- STOP.IND → E_SR.R (Direktes Reset)
- E_CYCLE.EO → E_SWITCH.EI (Zyklische Ereigniseingabe)
- E_SWITCH.EO0 → E_SR.S (Set-Operation)
- E_SWITCH.EO1 → E_SR.R (Reset-Operation)
- E_SR.EO → DigitalOutput_Q1.REQ (Ausgabesteuerung)

**Datenverbindungen:**
- E_SR.Q → E_SWITCH.G (Steuerung der Weichenschaltung)
- E_SR.Q → DigitalOutput_Q1.OUT (Ausgabewert)

**Lernziele:**
- Verständnis von zyklischen Ereignissen mit E_CYCLE
- Anwendung von Set-Reset-Logik mit E_SR
- Steuerung von Ereigniswegen mit E_SWITCH
- Integration von Ein-/Ausgabebausteinen

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen der IEC 61499, Ereignissteuerung

**Start der Übung**: 
1. START-Taster (I1) betätigen zum Beginn des Blinkvorgangs
2. STOP-Taster (I2) betätigen zum Anhalten (Ausgang bleibt aus)

## Zusammenfassung
Diese Übung demonstriert eine robuste Blinkerschaltung, die durch die kombinierte Verwendung von E_CYCLE, E_SWITCH und E_SR sicherstellt, dass der Ausgang nach dem Stoppen immer im AUS-Zustand verbleibt. Die direkte Reset-Verbindung vom STOP-Taster zum E_SR gewährleistet eine sofortige Deaktivierung unabhängig vom aktuellen Zykluszustand.