# Uebung_036: Spiegelabfolge V2 mit Schrittkette

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Spiegelabfolge-Steuerung mit einer Schrittkette. Das System steuert vier digitale Ausgänge in einer sequenziellen Abfolge, die durch digitale Eingänge getriggert wird. Die Steuerung ermöglicht das schrittweise Durchlaufen der Sequenz mit konfigurierbaren Zeitverzögerungen zwischen den Schritten.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:

- **DigitalOutput_Q1, Q2, Q3, Q4** (Typ: logiBUS_QX)
  - Steuern die digitalen Ausgänge Q1-Q4
  - Parameter: QI = TRUE, Output = logiBUS_DO::Output_Qx

- **DigitalInput_CLK_I1, I2, I3, I4** (Typ: logiBUS_IE)
  - Verarbeiten digitale Eingänge mit Tasterfunktionalität
  - Parameter: QI = TRUE, Input = logiBUS_DI::Input_Ix, InputEvent = BUTTON_SINGLE_CLICK

- **sequence_04** (Typ: sequence_ET_04)
  - Schrittketten-Steuerung mit 4 Schritten
  - Zeitparameter: DT_S3_S4 = T#2s, DT_S4_START = T#2s

- **F_SINT_TO_UINT** (Typ: F_SINT_TO_UINT)
  - Typkonvertierung von SINT zu UINT

- **Q_NumericValue** (Typ: Q_NumericValue)
  - Numerische Wertausgabe
  - Parameter: u16ObjId = DefaultPool::OutputNumber_N1

- **E_TimeOut** (Typ: E_TimeOut)
  - Zeitüberwachungsfunktionalität

### Sub-Bausteine: sequence_ET_04
- **Typ**: sequence_ET_04
- **Verwendete interne FBs**: Nicht spezifiziert
- **Funktionsweise**: 
  - Implementiert eine 4-stufige Schrittkette
  - Unterstützt Zeitverzögerungen zwischen Schritten
  - Bietet Ereignis- und Datenausgänge für jeden Schritt
  - Ermöglicht Reset-Funktionalität
  - Zeitparameter: DT_S3_S4 = 2s, DT_S4_START = 2s

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → sequence_04.START_S1 (Start Schritt 1)
- DigitalInput_CLK_I2.IND → sequence_04.S1_S2 (Schritt 1 → Schritt 2)
- DigitalInput_CLK_I3.IND → sequence_04.S2_S3 (Schritt 2 → Schritt 3)
- DigitalInput_CLK_I4.IND → sequence_04.RESET (Reset der Sequenz)
- sequence_04.EO_Sx → DigitalOutput_Qx.REQ (Schrittaktivierung → Ausgang)
- sequence_04.CNF → F_SINT_TO_UINT.REQ → Q_NumericValue.REQ (Zustandsnummer-Anzeige)

**Datenverbindungen:**
- sequence_04.STATE_NR → F_SINT_TO_UINT.IN → Q_NumericValue.u32NewValue (Zustandsnummer)
- sequence_04.DO_Sx → DigitalOutput_Qx.OUT (Schritt-Daten zu Ausgängen)

**Adapterverbindungen:**
- sequence_04.timeOut ↔ E_TimeOut.TimeOutSocket (Zeitüberwachung)

**Lernziele:**
- Verständnis von Schrittketten-Programmierung
- Umgang mit Zeitverzögerungen in Sequenzen
- Integration von digitalen Ein- und Ausgängen
- Typkonvertierung und numerische Ausgabe
- Ereignisgesteuerte Programmabläufe

**Schwierigkeitsgrad**: Mittel
**Vorkenntnisse**: Grundlagen der 4diac-IDE, digitale Ein-/Ausgänge, Schrittketten

## Zusammenfassung
Die Übung "Spiegelabfolge V2 mit Schrittkette" demonstriert eine komplexe sequenzielle Steuerung mit vier Schritten. Die Schrittkette wird durch Tastereingänge gesteuert und verfügt über konfigurierbare Zeitverzögerungen. Das System zeigt den aktuellen Zustand numerisch an und ermöglicht einen vollständigen Reset. Die Übung vermittelt praktische Erfahrungen mit ereignisgesteuerten Abläufen, Zeitsteuerungen und der Integration verschiedener Funktionsbausteine in einem Gesamtsystem.