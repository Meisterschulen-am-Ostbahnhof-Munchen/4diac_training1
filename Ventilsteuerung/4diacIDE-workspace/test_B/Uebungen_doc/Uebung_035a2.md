# Uebung_035a2: Ampelschaltung Österreich

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine österreichische Ampelschaltung für den Straßenverkehr. Die Steuerung realisiert den typischen Ablauf einer Verkehrsampel mit den Phasen Rot, Rot-Gelb, Grün, Grün-Blinken und Gelb. Die Schaltung wird über einen Taster gestartet und durchläuft automatisch den definierten Ablauf mit festgelegten Zeitintervallen.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_CLK_I1** (logiBUS_IE): Digitaler Eingang für Tasterbetätigung
- **sequence_T_04_loop** (sequence_T_05_loop): Sequenzer für den Ampelablauf
- **CAR_RED_LIGHT** (logiBUS_QX): Ausgang für rotes Licht
- **CAR_ORANGE_LIGHT** (logiBUS_QX): Ausgang für gelbes Licht  
- **CAR_GREEN_LIGHT** (logiBUS_QX): Ausgang für grünes Licht
- **E_TimeOut** (E_TimeOut): Zeitüberwachung
- **E_TRAIN** (E_TRAIN): Blinkgeber für Grünphase
- **E_T_FF** (E_T_FF): T-FlipFlop für Blinksignal

### Sub-Bausteine:

#### RED
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **OR_RED** (OR_2): ODER-Verknüpfung
    - Parameter: keine
    - Ereigniseingang: REQ
    - Ereignisausgang: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgang: OUT
- **Funktionsweise**: Kombiniert die Signale für Rot- und Rot-Gelb-Phase mittels ODER-Verknüpfung

#### ORANGE
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **OR_ORANGE** (OR_2): ODER-Verknüpfung
    - Parameter: keine
    - Ereigniseingang: REQ
    - Ereignisausgang: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgang: OUT
- **Funktionsweise**: Kombiniert die Signale für Rot-Gelb- und Gelb-Phase mittels ODER-Verknüpfung

#### GREEN
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **OR_2** (OR_2): ODER-Verknüpfung
    - Parameter: keine
    - Ereigniseingang: REQ
    - Ereignisausgang: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgang: OUT
- **Funktionsweise**: Kombiniert die Signale für Grün- und Grün-Blink-Phase mittels ODER-Verknüpfung

## Programmablauf und Verbindungen

**Zeitparameter der Ampelphasen:**
- Rot: 6 Sekunden
- Rot+Gelb: 2 Sekunden  
- Grün: 6 Sekunden
- Grün blinkend: 4 Sekunden (500ms Blinkintervall, 4 Blitze)
- Gelb: 2 Sekunden

**Start und Ablauf:**
- Die Ampel wird über den Taster I1 gestartet
- Der Sequenzer durchläuft automatisch alle Phasen in der definierten Reihenfolge
- Die Grün-Blinkphase wird durch den E_TRAIN-Baustein mit 500ms Intervall und 4 Blitzen realisiert

**Signalverarbeitung:**
- Die Sub-Bausteine RED, ORANGE und GREEN kombinieren jeweils die entsprechenden Phasensignale
- Die Ausgänge steuern direkt die physischen Lampenausgänge Q1-Q3

**Schwierigkeitsgrad**: Mittel
**Vorkenntnisse**: Grundkenntnisse in IEC 61499, Sequenzer-Programmierung, ODER-Verknüpfungen

## Zusammenfassung
Diese Übung demonstriert eine praxisnahe Anwendung einer Verkehrsampelsteuerung nach österreichischem Standard. Sie verbindet Sequenzer-Technik mit logischen Verknüpfungen und Zeitsteuerungen. Die modulare Struktur mit Sub-Bausteinen ermöglicht eine klare Trennung der Funktionalitäten und erleichtert die Wartung und Erweiterung des Systems.