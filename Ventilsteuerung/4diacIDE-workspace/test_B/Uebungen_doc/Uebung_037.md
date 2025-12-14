# Uebung_037: Spiegelabfolge V2 mit Schrittkette ENDLOS

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine endlose Spiegelabfolge mit einer Schrittkette. Das System steuert vier digitale Ausgänge in einer zyklischen Sequenz, die durch Tastereingaben gestartet und zurückgesetzt werden kann. Die aktuelle Schrittnummer wird auf einem numerischen Display angezeigt.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalOutput_Q1-Q4** (Typ: logiBUS_QX) - Steuerung der digitalen Ausgänge Q1-Q4
- **DigitalInput_CLK_I1** (Typ: logiBUS_IE) - Tastereingang I1 für Start der Sequenz
- **DigitalInput_CLK_I4** (Typ: logiBUS_IE) - Tastereingang I4 für Reset
- **Q_NumericValue** (Typ: Q_NumericValue) - Anzeige der aktuellen Schrittnummer
- **F_SINT_TO_UINT** (Typ: F_SINT_TO_UINT) - Datentypkonvertierung
- **E_TimeOut** (Typ: E_TimeOut) - Zeitüberwachung

### Sub-Bausteine: sequence_04
- **Typ**: sequence_ET_04_loop
- **Verwendete interne FBs**: Nicht spezifiziert
- **Funktionsweise**: Implementiert eine 4-stufige endlose Schrittkette mit folgenden Zeitparametern:
  - DT_S1_S2: T#200ms (Schritt 1 zu Schritt 2)
  - DT_S2_S3: T#200ms (Schritt 2 zu Schritt 3)
  - DT_S3_S4: T#200ms (Schritt 3 zu Schritt 4)
  - DT_S4_S1: T#200ms (Schritt 4 zu Schritt 1)

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- I1-Taster startet Schritt 1 der Sequenz
- I4-Taster resetet die gesamte Sequenz
- Jeder Schritt aktiviert den entsprechenden digitalen Ausgang
- Die Schrittkette triggert die Anzeigeaktualisierung

### Datenverbindungen:
- Schrittnummer wird an Display weitergeleitet
- Digitale Ausgangszustände werden an die Ausgabebausteine übergeben
- Datentypkonvertierung für die Anzeige

### Adapterverbindungen:
- TimeOut-Adapter für Zeitüberwachung der Sequenz

**Lernziele:**
- Implementierung endloser Schrittketten
- Zeitgesteuerte Zustandsübergänge
- Integration von Ein-/Ausgabebausteinen
- Datentypkonvertierung und Anzeigesteuerung

**Schwierigkeitsgrad:** Mittel

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von Schrittketten
- Kenntnisse digitaler Ein-/Ausgänge

**Start der Übung:**
- Taster I1 drücken, um die Sequenz zu starten
- Taster I4 drücken, um die Sequenz zurückzusetzen

## Zusammenfassung
Diese Übung demonstriert eine praktische Anwendung einer endlosen Schrittkette mit vier Zuständen. Die Sequenz durchläuft zyklisch die Schritte 1-4 mit je 200ms Verweilzeit und steuert dabei vier digitale Ausgänge. Die Integration von Tastersteuerung, Zeitüberwachung und visueller Rückmeldung macht diese Übung zu einem umfassenden Beispiel für sequenzielle Steuerungen in 4diac.