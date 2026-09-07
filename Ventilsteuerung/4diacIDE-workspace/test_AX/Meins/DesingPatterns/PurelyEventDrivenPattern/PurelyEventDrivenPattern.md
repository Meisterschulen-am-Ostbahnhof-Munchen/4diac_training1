# Design Pattern: Purely Event-Driven Function Blocks (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folie:

- **Folie 64 – "Purely Event-Driven function blocks"** (Kategorie:
  *Structural*, letzter offene Eintrag aus der Pattern-Tabelle auf
  Folie 62)

Kein Treffer im Vyatkin-Demoprojekt-Korpus (`AT_HOME`/`AT_END`/
`EXTEND_REQ`/`RETRACT_REQ`/`DoubleActingCylinder` gesucht, siehe Memory
`vyatkin-demo-corpus`) – reine Foliengrafik, kein herunterladbares
Beispielprojekt dahinter.

## Einordnung

| Feld | Wert |
|---|---|
| Name | Purely Event-Driven function blocks |
| Kategorie | Structural |
| Problem laut Folie | 1. Viele FBs mit einfacher Steuerlogik haben angehängte Ein-Zeilen-Algorithmen, die nur Ausgangsvariablen zuweisen. 2. Viele Datenverbindungen machen Modelle schwerer, was die Verifizierbarkeit beeinträchtigt |

## Das Grundproblem

Ein einfacher Steuerautomat (Folienbeispiel: `DoubleActingCylinder`,
ein doppeltwirkender Zylinder) wird oft so modelliert: Sensoren
(`atHome`, `atEnd`) als **BOOL-Dateneingänge**, die in
Transitionsbedingungen abgefragt werden (`REQ AND atHome`), und
Aktuatorausgänge (`extend`, `retract`) als **BOOL-Datenausgänge**, die
per Ein-Zeilen-ST-Algorithmus gesetzt werden (`extend := TRUE;
retract := FALSE;`). Das bläht das Modell auf zwei Arten auf:

1. Jeder BOOL-Ausgang braucht einen eigenen (trivialen) Algorithmus.
2. Jede BOOL-Datenverbindung ist ein zusätzliches Element, das die
   formale Verifikation (Zustandsraum, Modellprüfung) verlangsamt.

## Die Lösung

Sensor- und Aktuatorsignale werden konsequent als **Events** statt als
BOOL-Daten modelliert:

- **Sensoreingänge:** Statt eines kontinuierlich verfügbaren
  `atHome`-BOOL, das man in einer Transitionsbedingung abfragt, ein
  `AT_HOME`-**Event**, das genau einmal feuert, wenn der Sensor
  auslöst (die Umwandlung von digitalem BOOL-Signal in ein Event
  passiert an der Systemgrenze – siehe das verwandte, noch offene
  [IO-abstraction-layer-Pattern](../DesignPatterns.md), Folie 63).
- **Aktuatorausgänge:** Statt eines BOOL-Ausgangs `extend`, der einen
  Algorithmus braucht, ein `EXTEND`-**Event**, das direkt das
  Ausfahren auslöst – keine Zuweisung, kein Algorithmus nötig, die ECC
  routet das Event einfach direkt weiter.

Ergebnis: Transitionsbedingungen werden zu reinen Event-Namen
(`EXTEND_REQ` statt `REQ AND atHome`), und die ECC braucht keine
Algorithmen mehr, nur noch Event-Verdrahtung.

## Transformation auf der Folie (`DoubleActingCylinder`)

**Vorher:**

```
EventInputs:  INIT, REQ, EXTEND, RETRACT
EventOutputs: INITO, CNF
BOOL-Eingänge:  atHome, atEnd
BOOL-Ausgänge:  extend, retract
```

**Nachher (vollständig event-getrieben):**

```
EventInputs:  START, AT_HOME, AT_END, EXTEND_REQ, RETRACT_REQ
EventOutputs: INITO, CNF, EXTEND, RETRACT, STOP
(keine BOOL-Datenpins mehr – null Datenverbindungen)
```

Die Folie zeigt dazwischen noch einen Zwischenschritt (Ausgänge schon
eventifiziert, Sensoreingänge `atHome`/`atEnd` noch BOOL) – hier
umgesetzt wird direkt die vollständig transformierte Endversion.

**Hinweis zur exakten ECC-Verdrahtung:** Die Interface-Namen oben sind
direkt von der Folie ablesbar (Icon-Beschriftung), die genaue
Transitionsverdrahtung im komprimierten ECC-Diagramm der Folie ist es
nicht immer eindeutig (analog zur Erfahrung beim TokenRing-Pattern).
Die Umsetzung hier folgt einer eigenen, in sich schlüssigen Ableitung
(HOME/Extended als stabile Ruhezustände, `EXTEND_REQ`/`RETRACT_REQ` als
Auslöser, `AT_END`/`AT_HOME` als Abschlussbedingung, `STOP`+`CNF` am
Ende jeder Bewegung) – siehe Doku im Baustein selbst.

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

- **Baustein:** `EventDrivenCylinder.fbt` in diesem Ordner – Basic FB,
  **keine BOOL-Datenpins**, nur Events; kein Adapter nötig.
- **Kein separates Demo-Subapp nötig:** Der Baustein ist wegen der
  fehlenden Datenpins direkt im FORTE-Monitoring testbar (Events
  manuell auf der Instanz feuern), ohne dass man BOOL-Werte simulieren
  müsste – das ist gerade der Vorteil, den das Pattern demonstrieren
  soll.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Siehe `../DesignPatterns.md` für die Gesamtübersicht.
