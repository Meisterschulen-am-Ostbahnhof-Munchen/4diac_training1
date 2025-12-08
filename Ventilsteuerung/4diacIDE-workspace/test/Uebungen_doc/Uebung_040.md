# Uebung_040: Lauflicht 8

* * * * * * * * * *

## Einleitung
Diese Übung implementiert ein Lauflicht mit 8 Ausgängen, das in beide Richtungen gesteuert werden kann. Das System ermöglicht die Steuerung der Laufrichtung und Geschwindigkeit über verschiedene Eingänge und zeigt den aktuellen Zustand numerisch an.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalOutput_Q1 bis Q8** (Typ: logiBUS_QX) - Digitale Ausgänge für die 8 Lichter
- **DigitalInput_CLK_I1 bis I4** (Typ: logiBUS_IE) - Digitale Eingänge für Steuerung
- **Q_NumericValue** (Typ: Q_NumericValue) - Numerische Anzeige des aktuellen Zustands
- **F_SINT_TO_UINT** (Typ: F_SINT_TO_UINT) - Typkonvertierung für die Anzeige
- **E_CTU_0 und E_CTU_1** (Typ: E_CTU) - Zählerbausteine
- **E_DEMUX_0 und E_DEMUX_1** (Typ: E_DEMUX) - Demultiplexer für Zustandsübergänge
- **F_SUB_0 und F_SUB_1** (Typ: F_SUB) - Subtraktionsbausteine

### Sub-Bausteine: sequence_E_08_loop
- **Typ**: sequence_E_08_loop
- **Funktionsweise**: Steuert die Sequenz der 8 Zustände für das Lauflicht. Verfügt über Ereignisausgänge (EO_S1 bis EO_S8) und Datenausgänge (DO_S1 bis DO_S8) für jeden Zustand, sowie Ereigniseingänge für Zustandsübergänge (START_S1, S1_S2, S2_S3, etc.) und RESET.

## Programmablauf und Verbindungen

### Steuerungseingänge:
- **I1**: Startet die Sequenz bei Zustand S1
- **I2**: Erhöht den Zähler für Vorwärtsrichtung
- **I3**: Erhöht den Zähler für Rückwärtsrichtung  
- **I4**: Reset für beide Zähler und Sequenz

### Ablauf:
1. Durch Betätigen von I1 wird die Sequenz im Zustand S1 gestartet
2. I2 und I3 steuern die Geschwindigkeit und Richtung über die Zähler E_CTU_0 und E_CTU_1
3. Die Zählerwerte werden durch F_SUB Bausteine verarbeitet und an die DEMUX Bausteine weitergeleitet
4. Die DEMUX Bausteine steuern die Zustandsübergänge in der Sequenz
5. Jeder Zustand aktiviert den entsprechenden digitalen Ausgang (Q1-Q8)
6. Der aktuelle Zustand wird numerisch auf Q_NumericValue angezeigt

### Verbindungen:
- Ereignisverbindungen steuern den Ablauf zwischen den Bausteinen
- Datenverbindungen übertragen Zählerstände und Zustandsinformationen
- Die loop-Sequenz ist mit allen 8 Ausgängen verbunden

## Zusammenfassung
Diese Übung demonstriert die Steuerung einer 8-stufigen Lauflichtsequenz mit bidirektionaler Steuerung und Geschwindigkeitskontrolle. Sie verbindet digitale Ein-/Ausgänge mit Zählern, arithmetischen Operationen und einer Zustandssequenz, wobei der aktuelle Zustand zusätzlich numerisch angezeigt wird. Die Übung eignet sich zum Verständnis von Zustandsautomaten, Zählern und der Verknüpfung verschiedener Funktionsbausteine in 4diac.