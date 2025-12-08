# Uebung_039a: Spiegelabfolge V2 mit Schrittkette

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Spiegelabfolge-Steuerung mit Schrittkette, die für hydraulische Ringsysteme mit 3/2-Wege-Ventilen oder pneumatische 5/2-Wege-Ventile geeignet ist. Die Steuerung ermöglicht eine sequenzielle Abfolge von Ausgängen mit konfigurierbaren Zeitverzögerungen zwischen den Schritten.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **E_TimeOut**: Zeitüberwachung für Schrittketten
- **logiBUS_IE**: Digitale Eingänge für Taster (I1-I4)
- **sequence_ET_05**: Schrittkette mit 5 Zuständen
- **Softkey_IE**: Softkey-Eingabe (F1)
- **Uebung_039_sub_NumbAnzeig**: Numerische Anzeige des aktuellen Zustands

### Sub-Bausteine: Uebung_039a_sub_Outputs

- **Typ**: SubApplication
- **Verwendete interne FBs**:
    - **QX**: logiBUS_QX
        - Parameter: QI = TRUE
    - **GreenWhiteBackground**: GreenWhiteBackground
    - **E_SWITCH**: E_SWITCH
    - **E_SR**: E_SR (Set-Reset-Flipflop)
    - **IE**: Softkey_IE
        - Parameter: QI = TRUE, InputEvent = SoftKeyActivationCode::SK_RELEASED
- **Funktionsweise**: 
  - Verwaltet die Ausgänge Q1 und Q2 mit Set/Reset-Funktionalität
  - Ermöglicht manuelle Steuerung über Softkeys (F8 für Q1, F2 für Q2)
  - Visualisiert den Zustand mit GreenWhiteBackground
  - Verwendet ein E_SR-Element für die Speicherfunktion und E_SWITCH für die Umschaltung

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Taster I1-I4 lösen Zustandsübergänge in der Schrittkette aus
- Softkey F1 startet die Sequenz (START_S1)
- Die Schrittkette steuert Q1 und Q2 über SET/RESET-Ereignisse
- Zustandsnummer wird an die numerische Anzeige übertragen

**Zeitparameter der Schrittkette:**
- S3→S4: 5 Sekunden Verzögerung
- Alle anderen Übergänge: ohne Zeitverzögerung

**Lernziele:**
- Aufbau und Funktionsweise von Schrittketten
- Zeitgesteuerte Zustandsübergänge
- Parallele Ausgangssteuerung
- Integration von Softkey-Steuerung
- Visualisierung von Prozesszuständen

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**:
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Kenntnisse über Ereignis- und Datenverbindungen

**Starten der Übung**:
1. System initialisieren
2. Mit Softkey F1 die Sequenz starten
3. Taster I1-I4 in der vorgegebenen Reihenfolge betätigen

## Zusammenfassung
Diese Übung demonstriert eine praxisnahe Anwendung einer Schrittkette zur Steuerung einer Spiegelabfolge. Sie kombiniert manuelle Eingaben über Taster und Softkeys mit automatischen Zeitverzögerungen. Die modular aufgebaute Lösung mit Sub-Applikationen ermöglicht eine klare Trennung der Funktionalitäten und erleichtert die Wartung und Erweiterbarkeit des Systems.