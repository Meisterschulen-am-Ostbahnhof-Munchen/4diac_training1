# Uebung_006c: SR-Flip-Flop mit IB auf DI_REPEAT

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von SR-Flip-Flops in Kombination mit Eingabebausteinen, die auf Tastendruck-Wiederholung reagieren. Das System steuert acht digitale Ausgänge (Q1-Q8) über zwei Eingänge, wobei ein Demultiplexer zur Verteilung der Signale eingesetzt wird.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_RPT_I1/I2** (logiBUS_IB): Digitale Eingabebausteine mit Wiederholfunktion
- **F_BYTE_TO_UINT_S/R** (F_BYTE_TO_UINT): Datentyp-Konvertierung von Byte zu Unsigned Integer
- **E_DEMUX8_S/R** (E_DEMUX_8): 8-fach Ereignis-Demultiplexer
- **E_SR_Q1-Q8** (E_SR): SR-Flip-Flop Bausteine
- **DigitalOutput_Q1-Q8** (logiBUS_QX): Digitale Ausgabebausteine

### Sub-Bausteine: E_SR (SR-Flip-Flop)
- **Typ**: E_SR
- **Verwendete interne FBs**: Basis-SR-Flip-Flop
- **Funktionsweise**: Setzt (S) oder Rücksetzt (R) den Ausgang Q basierend auf den Eingangsereignissen

### Sub-Bausteine: E_DEMUX_8 (8-fach Demultiplexer)
- **Typ**: E_DEMUX_8
- **Verwendete interne FBs**: Ereignis-Demultiplexer
- **Funktionsweise**: Leitet eingehende Ereignisse basierend auf dem K-Wert an einen der 8 Ausgänge weiter

## Programmablauf und Verbindungen

**Eingabeverarbeitung:**
- DigitalInput_RPT_I1 (I1) und I2 erfassen Tastendrücke mit Wiederholfunktion
- F_BYTE_TO_UINT Bausteine konvertieren die Eingabedaten für die Demultiplexer

**Signalverteilung:**
- E_DEMUX8_S verteilt Set-Signale an die SR-Flip-Flops Q1-Q8
- E_DEMUX8_R verteilt Reset-Signale an die SR-Flip-Flops

**Ausgabesteuerung:**
- Acht E_SR Bausteine steuern die entsprechenden DigitalOutput_Q1-Q8 Ausgänge
- Jeder SR-Flip-Flop kann unabhängig gesetzt und zurückgesetzt werden

**Lernziele:**
- Verständnis von SR-Flip-Flops in IEC 61499
- Umgang mit Ereignis-Demultiplexern
- Datentyp-Konvertierung in Steuerungssystemen
- Verwendung von Wiederhol-Eingabefunktionen

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen IEC 61499, Digitale Ein-/Ausgänge

**Starten der Übung**: 
1. System in 4diac-IDE laden
2. Auf logiBUS-Hardware deployen
3. Eingänge I1 und I2 mit Tastern testen

## Zusammenfassung
Diese Übung zeigt eine erweiterte Anwendung von SR-Flip-Flops mit multiplexer-basierter Steuerung. Die Verwendung von Wiederhol-Eingabebausteinen und Demultiplexern ermöglicht eine flexible Steuerung mehrerer Ausgänge mit minimalen Eingabegeräten. Die Übung vermittelt praktische Kenntnisse in Signalverteilung und Zustandsspeicherung in verteilten Steuerungssystemen.