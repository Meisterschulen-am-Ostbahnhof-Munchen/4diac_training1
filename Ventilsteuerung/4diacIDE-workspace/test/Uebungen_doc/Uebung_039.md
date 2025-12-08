# Uebung_039: Spiegelabfolge V2 mit Schrittkette

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Spiegelabfolge-Steuerung mit einer Schrittkette, die für hydraulische 4/3-Wege-Ventile oder pneumatische 5/3-Wege-Ventile mit gesperrter Mittelstellung geeignet ist. Die Steuerung ermöglicht eine sequenzielle Abfolge von Ausgängen, die durch Tastereingaben und Zeitverzögerungen gesteuert wird.

## Verwendete Funktionsbausteine (FBs)

### Haupt-FBs:
- **E_TimeOut**: Zeitgeber für Zeitverzögerungen
- **DigitalInput_DOWN_I1 bis I4**: Digitale Eingänge für Taster (I1-I4)
- **sequence_05**: Schrittkette mit 5 Zuständen und Zeitparametern
- **SoftKey_UP_F1**: Softkey-Eingang für Startbefehl

### Sub-Bausteine:

#### Uebung_039_sub_NumbAnzeig
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **F_SINT_TO_UINT**: Typ F_SINT_TO_UINT
    - Parameter: Keine
    - Datenausgang: OUT (UINT)
    - Dateneingang: IN (SINT)
  - **Q_NumericValue**: Typ Q_NumericValue
    - Parameter: u16ObjId = DefaultPool::OutputNumber_N1
    - Dateneingang: u32NewValue (UINT)
- **Funktionsweise**: Zeigt den aktuellen Zustand der Schrittkette als numerischen Wert auf einem Display an. Konvertiert den SINT-Zustand in UINT für die Anzeige.

#### Uebung_039_sub_Outputs
- **Typ**: SubApp
- **Verwendete interne FBs**:
  - **QX**: Typ logiBUS_QX
    - Parameter: QI = TRUE
    - Datenausgang: OUT (BOOL)
  - **IX**: Typ Softkey_IX
    - Parameter: QI = TRUE
    - Dateneingang: u16ObjId (UINT)
  - **OR_2**: Typ OR_2
    - Datenausgang: OUT (BOOL)
    - Dateneingänge: IN1, IN2 (BOOL)
  - **GreenWhiteBackground**: Typ GreenWhiteBackground
    - Dateneingang: DI1 (BOOL), u16ObjId (UINT)
- **Funktionsweise**: Steuert die Ausgänge Q1-Q4 mit zusätzlicher Softkey-Funktionalität und visueller Rückmeldung. Ermöglicht sowohl automatische als auch manuelle Steuerung der Ausgänge.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Taster I1-I4 lösen die Zustandsübergänge der Schrittkette aus
- Softkey F1 startet die Sequenz (START_S1)
- Jeder Schritt aktiviert den entsprechenden Ausgang (EO_S1-S5 → Q1-Q4)
- Die Schrittkette liefert Zustandsinformationen zur numerischen Anzeige

**Datenverbindungen:**
- Zustandsnummer (STATE_NR) wird zur Anzeige übertragen
- Ausgangsdaten (DO_S1-S5) steuern die physikalischen Ausgänge
- Zeitparameter für Schrittübergänge sind konfigurierbar

**Zeitparameter der Schrittkette:**
- S3 → S4: 5 Sekunden Verzögerung
- Andere Übergänge: ohne Zeitverzögerung

**Lernziele:**
- Verständnis von Schrittketten-Programmierung
- Umgang mit Zeitverzögerungen in Sequenzen
- Integration von Eingangs- und Ausgangsmodulen
- Visualisierung von Prozesszuständen

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignissteuerung

**Starten der Übung**: 
1. Taster F1 drücken zum Starten der Sequenz
2. Taster I1-I4 in der vorgegebenen Reihenfolge betätigen
3. Beobachten der Zustandsanzeige und Ausgangsaktivierungen

## Zusammenfassung
Diese Übung demonstriert eine komplexe Schrittkettensteuerung mit integrierter Zustandsvisualisierung. Sie kombiniere digitale Eingänge, Zeitsteuerung, Ausgangsansteuerung und Benutzerinteraktion über Softkeys. Die modulare Struktur mit Sub-Applikationen ermöglicht eine klare Trennung der Funktionen und erleichtert die Wartung und Erweiterung des Systems.