# Design Pattern: IO Abstraction Layer (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folie:

- **Folie 63 – "Input/Output (IO) abstraction layer"** (Kategorie:
  *Architectural*, Problem: *"Separate application logic from
  input/output signal readings, convert digital IO data reading into
  event signals"*)

Letztes Pattern aus der Modul-6-Foliensammlung (Folien 62–72
vollständig durchgearbeitet). Kein Treffer im Vyatkin-Demoprojekt-
Korpus (siehe Memory `vyatkin-demo-corpus`).

## Einordnung

| Feld | Wert |
|---|---|
| Name | IO Abstraction Layer |
| Kategorie | Architectural |
| Problem laut Folie | Anwendungslogik von Ein-/Ausgangs-Signal-Lesevorgängen trennen; digitale IO-Daten in Event-Signale umwandeln |

## Das Grundproblem

Wenn Anwendungslogik direkt auf rohe Hardware-BOOL-Signale zugreift
(kontinuierlich gelesene digitale Ein-/Ausgänge), vermischen sich zwei
Zuständigkeiten: "wie wird ein Signal physisch gelesen/geschrieben"
und "was bedeutet ein Signalwechsel fachlich". Das erschwert
Wiederverwendung (dieselbe Anwendungslogik auf anderer Hardware) und
macht die Anwendungslogik unnötig BOOL-daten-lastig – genau das
Problem, das das
[Purely-Event-Driven-Pattern](../PurelyEventDrivenPattern/PurelyEventDrivenPattern.md)
lösen will.

## Die Lösung: 5-Schichten-Architektur

Folie 63 zeigt fünf Schichten, links nach rechts (Eingangsseite) bzw.
rechts nach links (Ausgangsseite):

1. **Hardware Layer (Input)** – liest die rohen digitalen Signale
   (`SYMLINKMULTIVARDST`-Baustein auf der Folie, ein
   Symbolic-Link-basierter Multi-Variablen-Lesebaustein).
2. **Input HAL** – wandelt jedes rohe BOOL-Signal per steigender-Flanke-
   Erkennung (`E_R_TRIG`) in ein diskretes Event um (`AT_HOME`,
   `AT_END`).
3. **Application Layer** – die eigentliche Fachlogik, komplett
   event-getrieben (kein einziger BOOL-Datenpin) – strukturell exakt
   das, was im
   [Purely-Event-Driven-Pattern](../PurelyEventDrivenPattern/PurelyEventDrivenPattern.md)
   gebaut wurde (`DoSomething`/`DoSomeOtherThing` auf der Folie
   entsprechen unserem `EventDrivenCylinder.fbt`).
4. **Output HAL** – wandelt jedes Kommando-Event (`EXTEND`, `RETRACT`)
   per bistabilem Latch (`E_SR`) zurück in ein persistentes BOOL-Signal
   für den Aktuator.
5. **Hardware Layer (Output)** – schreibt die rohen digitalen Signale
   (`SYMLINKMULTIVARSRC`).

## Abweichung von der Folie: Hardware-Layer-Baustein

`SYMLINKMULTIVARDST`/`SYMLINKMULTIVARSRC` sind **weder Standard-4diac-
Bausteine** (geprüft gegen die lokale 4diac-Typelibrary) **noch
irgendwo in diesem Repo vorhanden** – wahrscheinlich ein
fortiss-Forschungs-/Demo-Baustein, der nicht Teil der Standard-
Distribution ist (vgl. die Lektion aus dem Decorator-Pattern zu
`E_PERMIT` – hier umgekehrt: dieses Mal wirklich nicht vorhanden, nach
Prüfung).

Dieses Repo hat für exakt dasselbe Problem (rohes Hardware-BOOL ↔
Event) bereits einen eigenen, echten, bereits verwendeten Mechanismus:
**`logiBUS_IE`** (liest einen digitalen Eingang und feuert dabei
direkt ein Event – Hardware Layer und Input HAL in einem Baustein
vereint, kein separates `E_R_TRIG` nötig) und **`logiBUS_QX`**
(schreibt einen digitalen Ausgang, per Event getriggert) – schon
verwendet in
[`HandshakePatternDemoIO.sub`](../HandshakePattern/HandshakePattern.md).
Die Umsetzung hier nutzt diesen repo-eigenen, real funktionierenden
Mechanismus statt einer unbestätigten Nachbildung von
`SYMLINKMULTIVARDST`/`SRC`.

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

Ordner: dieser Ordner (`IOAbstractionPattern/`)

- **Application Layer:** `EventDrivenCylinder.fbt`
  (aus dem Purely-Event-Driven-Pattern, unverändert wiederverwendet).
- **Hardware Layer (Input) + Input HAL (kombiniert):** vier
  `logiBUS_IE`-Instanzen (`Input_I1`–`Input_I4`) für `EXTEND_REQ`,
  `RETRACT_REQ`, `AT_HOME`, `AT_END`.
- **Output HAL:** zwei `E_SR`-Latches (`ExtendLatch`, `RetractLatch`),
  je durch das jeweils andere Kommando-Event zurückgesetzt (eigene,
  sinnvolle Ergänzung – auf der Folie ist der `R`-Eingang der beiden
  `E_SR`-Boxen im komprimierten Bild nicht eindeutig beschriftet).
- **Hardware Layer (Output):** zwei `logiBUS_QX`-Instanzen
  (`Output_Q1`/`Output_Q2`).
- **Init-Kette:** Eine der `logiBUS_IE`-Instanzen liefert über ihr
  eigenes, beim Deployment automatisch feuerndes `INITO` den
  `START`-Trigger für `EventDrivenCylinder` (analog zum Bootstrapping
  in `HandshakePatternDemoIO.sub`).

Datei: `IOAbstractionDemo.sub`.

## Weitere Design Patterns aus Modul 6

Siehe `../DesignPatterns.md` für die Gesamtübersicht – mit diesem
Pattern sind alle zehn in Modul 6 gezeigten Patterns umgesetzt.
