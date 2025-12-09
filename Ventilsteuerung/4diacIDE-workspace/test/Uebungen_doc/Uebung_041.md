# Uebung_041: Lauflicht 8 mit einer Taste

* * * * * * * * * *

## Einleitung
Diese Übung implementiert ein 8-stufiges Lauflicht, das mit einer Taste gesteuert werden kann. Das System ermöglicht die sequenzielle Aktivierung von acht Ausgängen in verschiedenen Betriebsmodi.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalOutput_Q1 bis Q8** (Typ: logiBUS_QX) - Digitale Ausgänge für die Lauflicht-LEDs
- **DigitalInput_CLK_I1, I2, I4** (Typ: logiBUS_IE) - Digitale Eingänge für Tastensteuerung
- **Q_NumericValue** (Typ: Q_NumericValue) - Numerische Anzeige des aktuellen Zustands
- **F_SINT_TO_UINT** (Typ: F_SINT_TO_UINT) - Typkonvertierung für die Anzeige
- **E_CTU_0** (Typ: E_CTU) - Zählerbaustein
- **F_SUB_0** (Typ: F_SUB) - Subtraktionsbaustein
- **E_DEMUX_0** (Typ: E_DEMUX_8) - 8-fach Demultiplexer

### Sub-Bausteine: sequence_E_08_loop
- **Typ**: sequence_E_08_loop
- **Verwendete interne FBs**: Nicht spezifiziert
- **Funktionsweise**: Steuert die sequenzielle Aktivierung der acht Ausgänge und verwaltet den Lauflicht-Zyklus

## Programmablauf und Verbindungen

Das Programm arbeitet nach folgendem Prinzip:

**Eingangssteuerung:**
- I1: Startet die Sequenz bei Position S1
- I2: Inkrementiert den Zähler (E_CTU_0) für die Betriebsmodus-Auswahl
- I4: Reset-Funktion für Zähler und Sequenz

**Sequenzablauf:**
1. Die Taste I1 startet die Sequenz bei Zustand S1
2. Der Zähler E_CTU_0 zählt die Tastendrücke auf I2
3. F_SUB_0 subtrahiert 1 vom Zählerwert für die korrekte Demultiplexer-Ansteuerung
4. E_DEMUX_0 leitet basierend auf dem Zählerwert zu den entsprechenden Zustandsübergängen
5. Die Sequenz durchläuft die Zustände S1-S8 im Zyklus

**Ausgangssteuerung:**
- Jeder Zustand (S1-S8) aktiviert den entsprechenden digitalen Ausgang (Q1-Q8)
- Der aktuelle Zustand wird über F_SINT_TO_UINT an Q_NumericValue zur Anzeige übergeben

**Lernziele:**
- Verständnis von Zustandsautomaten
- Umgang mit Zählern und Demultiplexern
- Steuerung von sequenziellen Abläufen
- Integration von digitalen Ein- und Ausgängen

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignissteuerung

**Starten der Übung**: Nach dem Laden und Kompilieren kann die Übung über die Taste I1 gestartet werden. Die Betriebsmodi werden über I2 ausgewählt.

## Zusammenfassung
Diese Übung demonstriert die Implementierung eines komplexen Lauflicht-Systems mit mehreren Betriebsmodi. Sie verbindet Zustandsautomaten, Zählerfunktionalität und Ereignissteuerung zu einem kohärenten System. Die Verwendung von Demultiplexern ermöglicht flexible Zustandsübergänge, während die Integration von numerischer Anzeige den aktuellen Systemzustand visualisiert.