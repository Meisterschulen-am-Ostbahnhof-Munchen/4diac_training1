# Uebung_035a3: Ampelschaltung Österreich

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Ampelschaltung nach österreichischem Standard. Die Ampelsteuerung durchläuft verschiedene Phasen für den Fahrzeugverkehr und beinhaltet eine spezielle Blinkphase für die Grünphase.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_CLK_I1** (logiBUS_IE): Digitaler Eingang für Tasterbetätigung
- **sequence_T_04_loop** (sequence_T_05_loop): Sequenzer für Ampelphasensteuerung
- **E_TimeOut** (E_TimeOut): Zeitüberwachung
- **E_BLINK_TRAIN** (E_BLINK_TRAIN): Blinkgenerator für Grünblinkphase
- **CAR_RED_LIGHT** (logiBUS_QX): Ausgang für rotes Licht
- **CAR_ORANGE_LIGHT** (logiBUS_QX): Ausgang für oranges Licht  
- **CAR_GREEN_LIGHT** (logiBUS_QX): Ausgang für grünes Licht

### Sub-Bausteine:

#### RED
- **Typ**: Sub-Applikation
- **Verwendete interne FBs**:
  - **OR_RED** (OR_2): ODER-Verknüpfung
    - Parameter: keine
    - Ereigniseingang: REQ
    - Ereignisausgang: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgang: OUT
- **Funktionsweise**: Kombiniert die Signale für Rot- und Rot-Orange-Phase mittels ODER-Verknüpfung

#### ORANGE
- **Typ**: Sub-Applikation
- **Verwendete interne FBs**:
  - **OR_ORANGE** (OR_2): ODER-Verknüpfung
    - Parameter: keine
    - Ereigniseingang: REQ
    - Ereignisausgang: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgang: OUT
- **Funktionsweise**: Kombiniert die Signale für Rot-Orange- und Orange-Phase mittels ODER-Verknüpfung

#### GREEN
- **Typ**: Sub-Applikation
- **Verwendete interne FBs**:
  - **OR_2** (OR_2): ODER-Verknüpfung
    - Parameter: keine
    - Ereigniseingang: REQ
    - Ereignisausgang: CNF
    - Dateneingänge: IN1, IN2
    - Datenausgang: OUT
- **Funktionsweise**: Kombiniert die Signale für Dauer-Grün- und Grün-Blink-Phase mittels ODER-Verknüpfung

## Programmablauf und Verbindungen

**Phasenablauf:**
1. **ROT** (6 Sekunden)
2. **ROT+ORANGE** (2 Sekunden)
3. **GRÜN** (6 Sekunden)
4. **GRÜN BLINK** (4 Sekunden)
5. **ORANGE** (2 Sekunden)

**Start der Übung:**
- Die Ampelsequenz wird durch Betätigung des Tasters an Eingang I1 gestartet

**Zeitparameter:**
- ROT: 6 Sekunden
- ROT+ORANGE: 2 Sekunden
- GRÜN: 6 Sekunden
- GRÜN BLINK: 4 Sekunden (mit 500ms Ein/Aus-Zeit, 2 Blinkzyklen)
- ORANGE: 2 Sekunden

**Verbindungen:**
- Der Sequenzer steuert die Phasenübergänge und aktiviert entsprechende Ausgänge
- Die Sub-Bausteine kombinieren die Phasensignale für die jeweiligen Lampen
- Der Blinkgenerator erzeugt das Blinksignal für die Grünblinkphase
- Zeitüberwachung erfolgt über E_TimeOut

## Zusammenfassung
Diese Übung demonstriert eine vollständige Ampelschaltung mit allen relevanten Phasen nach österreichischem Standard. Besonderes Merkmal ist die Implementierung der Grünblinkphase vor dem Übergang zur Orange-Phase. Die modulare Struktur mit Sub-Bausteinen ermöglicht eine klare Trennung der Funktionalitäten und erleichtert die Wartung und Erweiterung des Systems.