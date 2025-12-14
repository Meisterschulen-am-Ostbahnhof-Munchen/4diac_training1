# Uebung_035: Spiegelabfolge V2 mit Schrittkette

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine erweiterte Spiegelabfolge-Steuerung mit einer Schrittkette. Das System steuert vier digitale Ausgänge in einer sequenziellen Abfolge, die über digitale Eingänge gestartet und gesteuert werden kann. Die Übung demonstriert den Einsatz von Schrittketten und Zeitsteuerungen in der Automatisierungstechnik.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalOutput_Q1-Q4** (Typ: logiBUS_QX) - Digitale Ausgänge für die Aktorik
- **DigitalInput_CLK_I1-I4** (Typ: logiBUS_IE) - Digitale Eingänge mit Tasterfunktionalität
- **E_TimeOut** (Typ: E_TimeOut) - Zeitüberwachungsbaustein
- **F_SINT_TO_UINT** (Typ: F_SINT_TO_UINT) - Datentypkonvertierung
- **Q_NumericValue** (Typ: Q_NumericValue) - Numerische Wertausgabe
- **sequence_04** (Typ: sequence_ET_04) - Schrittkettensteuerung

### Sub-Bausteine: sequence_ET_04
- **Typ**: sequence_ET_04
- **Verwendete interne FBs**: E_TimeOut (Adapterverbindung)
- **Parameter**:
  - DT_S1_S2 = T#2s (Schritt 1 zu Schritt 2 Zeitverzögerung)
  - DT_S2_S3 = T#2s (Schritt 2 zu Schritt 3 Zeitverzögerung)
  - DT_S3_S4 = T#2s (Schritt 3 zu Schritt 4 Zeitverzögerung)
  - DT_S4_START = T#2s (Schritt 4 zurück zu Start Zeitverzögerung)
- **Ereigniseingänge**: START_S1, S2_S3, S4_START, RESET
- **Ereignisausgänge**: EO_S1, EO_S2, EO_S3, EO_S4, CNF
- **Datenausgänge**: DO_S1, DO_S2, DO_S3, DO_S4, STATE_NR
- **Funktionsweise**: Implementiert eine 4-Schritt-Sequenz mit Zeitsteuerung zwischen den Schritten. Jeder Schritt aktiviert einen entsprechenden Ausgang und kann über externe Signale gesteuert werden.

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- I1-IND → START_S1: Startet Schritt 1 der Sequenz
- I2-IND → S2_S3: Wechsel von Schritt 2 zu Schritt 3
- I3-IND → S4_START: Wechsel von Schritt 4 zurück zum Start
- I4-IND → RESET: Reset der gesamten Sequenz
- EO_S1-4 → REQ der jeweiligen Ausgänge: Aktiviert die digitalen Ausgänge
- CNF → REQ der Datentypkonvertierung: Bestätigt Zustandsänderungen

### Datenverbindungen:
- STATE_NR → IN der Datentypkonvertierung: Überträgt aktuellen Zustand
- DO_S1-4 → OUT der jeweiligen Ausgänge: Steuert die digitalen Ausgänge
- Konvertierungsausgang → NumericValue: Zeigt aktuellen Zustand an

### Adapterverbindungen:
- timeOut → TimeOutSocket: Verbindung zur Zeitüberwachung

### Lernziele:
- Verständnis von Schrittketten-Programmierung
- Umgang mit Zeitsteuerungen in Sequenzen
- Implementierung von Steuerungslogik mit externen Tastern
- Datentypkonvertierung und Zustandsanzeige

### Schwierigkeitsgrad: Mittel

### Benötigte Vorkenntnisse:
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Kenntnisse in ereignisgesteuerter Programmierung

### Start der Übung:
Die Übung wird über die digitalen Eingänge I1-I4 gestartet und gesteuert. I1 startet die Sequenz, I2 und I3 steuern die Schrittübergänge, I4 resettet das System.

## Zusammenfassung
Diese Übung demonstriert eine komplexe Schrittkettensteuerung mit vier Zuständen und integrierter Zeitsteuerung. Das System ermöglicht sowohl automatischen als auch manuellen Betrieb durch externe Taster und zeigt den aktuellen Zustand über eine numerische Anzeige. Die Implementierung verbindet digitale Ein-/Ausgänge mit einer sequenziellen Steuerungslogik unter Verwendung von Zeitverzögerungen zwischen den Zustandsübergängen.