# Uebung_008: Blinker mit E_CYCLE, E_SWITCH und E_SR

* * * * * * * * * *

## Einleitung
Diese Übung implementiert einen Blinkerschaltkreis mit zyklischer Ansteuerung unter Verwendung von IEC 61499-Basis-Funktionsbausteinen. Das System erzeugt ein regelmäßiges Blinksignal, das an einen digitalen Ausgang ausgegeben wird.

## Verwendete Funktionsbausteine (FBs)

### E_CYCLE
- **Typ**: Zyklischer Ereignisgenerator
- **Parameter**: DT = T#1s (Zykluszeit von 1 Sekunde)
- **Ereignisausgang**: EO (Ereignisausgang bei jedem Zyklus)

### E_SWITCH
- **Typ**: Ereignis-Weichenschaltung
- **Ereigniseingang**: EI (Eingangsereignis)
- **Ereignisausgänge**: EO0, EO1 (alternierende Ausgänge)
- **Dateneingang**: G (Steuersignal für Ausgangswahl)

### E_SR
- **Typ**: Set-Reset-Flipflop
- **Ereigniseingänge**: S (Set), R (Reset)
- **Ereignisausgang**: EO (Auslöser bei Zustandsänderung)
- **Datenausgang**: Q (aktueller Zustand)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX (Digitaler Ausgangsbaustein)
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zielausgang definiert)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
1. E_CYCLE.EO → E_SWITCH.EI (Zyklische Triggerung der Weiche)
2. E_SWITCH.EO0 → E_SR.S (Set-Signal für Flipflop)
3. E_SWITCH.EO1 → E_SR.R (Reset-Signal für Flipflop)
4. E_SR.EO → DigitalOutput_Q1.REQ (Auslösung der Ausgabefunktion)

**Datenverbindungen:**
1. E_SR.Q → E_SWITCH.G (Rückkopplung des Flipflop-Zustands zur Weichensteuerung)
2. E_SR.Q → DigitalOutput_Q1.OUT (Direkte Ausgabe des Blinksignals)

**Funktionsweise:**
Der E_CYCLE-Baustein generiert alle 1 Sekunde ein Ereignis, das die E_SWITCH-Weiche ansteuert. Abhängig vom aktuellen Zustand des E_SR-Flipflops (Q-Ausgang) wählt die Weiche alternierend zwischen Set- und Reset-Eingang. Dies führt zu einem kontinuierlichen Wechsel des Flipflop-Zustands, der als Blinksignal an den digitalen Ausgang Q1 ausgegeben wird.

**Lernziele:**
- Verständnis zyklischer Ereignisgeneratoren
- Anwendung von Set-Reset-Flipflops
- Implementierung von Rückkopplungsschleifen
- Steuerung digitaler Ausgänge

**Schwierigkeitsgrad:** Einsteiger

**Benötigte Vorkenntnisse:** Grundlagen IEC 61499, Basis-Funktionsbausteine

**Starten der Übung:** Die Anwendung wird automatisch nach dem Laden gestartet und läuft kontinuierlich.

## Zusammenfassung
Diese Übung demonstriert eine grundlegende Blinkerschaltung mit IEC 61499-Funktionsbausteinen. Durch die Kombination von E_CYCLE, E_SWITCH und E_SR wird ein robustes Blinksystem mit regelmäßiger Takterzeugung und Zustandssteuerung realisiert. Die Rückkopplung des Flipflop-Zustands zur Weichensteuerung sorgt für einen automatischen Wechsel zwischen Set- und Reset-Operationen.