# IEC 61499 Design Patterns – Übersicht

Sammlung von Design-Pattern-Umsetzungen für dieses Repository, angelehnt an
UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Quelle: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Jedes Pattern bekommt einen eigenen Unterordner hier in `DesingPatterns/`
mit mindestens:

- einer `*.md`-Datei, die das Pattern erklärt (Problem, Mechanismus,
  Bezug zur Kursfolie, Umsetzung in diesem Repo),
- den zugehörigen `.fbt`/`.sub`-Beispielbausteinen,
- ggf. einem neuen Adapter-Typ in `.lib/adapter-3.0.0/typelib/…`, falls
  das Pattern einen eigenen Adapter braucht.

## Patterns laut Folie 62 ("Design Patterns for IEC 61499")

| Kategorie | Pattern | Ordner | Status |
|---|---|---|---|
| Structural (creational) | Purely Event-Driven function blocks | [`PurelyEventDrivenPattern/`](PurelyEventDrivenPattern/PurelyEventDrivenPattern.md) | **umgesetzt, ungetestet in 4diac** |
| Structural (creational) | Generic Actuation | [`ChainOfActionsPattern/`](ChainOfActionsPattern/ChainOfActionsPattern.md) (`TrueUntil.fbt`) | **umgesetzt** (zusammen mit Chain of actions, Folie 65) |
| Structural (creational) | Decorator | [`DecoratorPattern/`](DecoratorPattern/DecoratorPattern.md) | **umgesetzt, ungetestet in 4diac** |
| Architectural | IO abstraction layer | – | offen |
| Compositional | Chain of actions | [`ChainOfActionsPattern/`](ChainOfActionsPattern/ChainOfActionsPattern.md) | **umgesetzt, ungetestet in 4diac** |
| Behavioural | Chain of actions | [`ChainOfActionsPattern/`](ChainOfActionsPattern/ChainOfActionsPattern.md) | **umgesetzt, ungetestet in 4diac** |

## Weitere Patterns laut Folie 69 ("Miscellaneous design patterns")

| Kategorie | Pattern | Ordner | Status |
|---|---|---|---|
| Compositional / Architectural | Start/Stop pattern | [`StartStopPattern/`](StartStopPattern/StartStopPattern.md) | **umgesetzt, ungetestet in 4diac** |
| Compositional / Architectural | reset pattern | [`ResetPattern/`](ResetPattern/ResetPattern.md) | **umgesetzt, ungetestet in 4diac** |
| Behavioural | **Handshake pattern** | [`HandshakePattern/`](HandshakePattern/HandshakePattern.md) | **umgesetzt** (Adapter `EVENT_HS`, dataless, wie auf Folie 72) |

## Weitere Adapter-Patterns (nicht in der Folie-62/69-Taxonomie, aber konkret vorgeschlagen)

| Pattern | Fundstelle | Ordner | Status |
|---|---|---|---|
| **TokenRing (Mutual Exclusion)** | Folie 15, Quelle: Dai/Vyatkin/Christensen/Dubinin, IEEE INDIN 2014 | [`TokenRingPattern/`](TokenRingPattern/TokenRingPattern.md) | **umgesetzt, ungetestet in 4diac** |
| service-Adapter (datentragende Handshake-Variante) | Folie 48 | [`HandshakePattern/`](HandshakePattern/HandshakePattern.md) (`EVENT_HS_WSTRING`) | **umgesetzt** |

## Umgesetzt

### Handshake pattern

Ordner: [`HandshakePattern/`](HandshakePattern/HandshakePattern.md)

- Adapter-Typ `EVENT_HS` (dataless, REQ/RSP-Eingänge, CNF/IND-Ausgänge) in
  `.lib/adapter-3.0.0/typelib/types/bidirectional/Handshake/EVENT_HS.adp`, plus
  datentragende Variante `EVENT_HS_WSTRING`
- Beispielbausteine `HandshakeRequester(WSTRING).fbt` (Plug/Client-Rolle)
  und `HandshakeResponder(WSTRING).fbt` (Socket/Server-Rolle)
- Demo-Subapplications `HandshakePatternDemo(WSTRING).sub`, die beide
  über die Adapterverbindung koppeln, sowie `HandshakePatternDemoIO.sub`
  (physisches I/O: Taster löst aus, LED zeigt abgeschlossenen Handshake)

Details, Theorie und Bezug zur Kursfolie: siehe
[`HandshakePattern/HandshakePattern.md`](HandshakePattern/HandshakePattern.md).

### TokenRing / Mutual Exclusion pattern

Ordner: [`TokenRingPattern/`](TokenRingPattern/TokenRingPattern.md)

- Adapter-Typ `TokenRing` (dataless, RCV-Eingang, GIVE-Ausgang) in
  `.lib/adapter-3.0.0/typelib/types/bidirectional/TokenRing/TokenRing.adp`
- Beispielbaustein `TokenRingNode.fbt` (ein Controller im Ring, mit
  `MTXIN`-Socket und `MTXOUT`-Plug)
- Demo-Subapplication `TokenRingPatternDemo.sub` (5-Knoten-Ring)

GIVE/RCV-Rollenzuordnung (Socket=`MTXIN`, Plug=`MTXOUT`) gegen die
Originalquelle bestätigt (Dai/Vyatkin/Christensen/Dubinin, IEEE INDIN
2014 – siehe `TokenRingPattern.md`). Noch nicht in 4diac getestet.

### Chain of Actions (inkl. Generic Actuation)

Ordner: [`ChainOfActionsPattern/`](ChainOfActionsPattern/ChainOfActionsPattern.md)

- Baustein `TrueUntil.fbt` (Folie 65 "Generic Actuation"): generischer
  Aktions-Baustein, kein Adapter nötig – `TRIGGER`/`REQ` → `TO_POSITION`,
  wartet auf `inPosition`, feuert `STOP`+`DONE`
- Demo-Subapplication `ChainOfActionsDemo.sub` (Folie 66): vier
  `TrueUntil`-Instanzen verkettet über `DONE`→`TRIGGER`, statt eines
  großen "Spaghetti"-ECC

Offener Punkt: genaue Rolle von `REQ` neben `TRIGGER` aus der Folie
nicht zweifelsfrei ablesbar (vorerst wie `TRIGGER` behandelt) – siehe
`ChainOfActionsPattern.md`. Noch nicht in 4diac getestet.

### Decorator

Ordner: [`DecoratorPattern/`](DecoratorPattern/DecoratorPattern.md)

- Baustein `E_PERMIT` (Folie 68) – **Standardbaustein**
  `iec61499::events::E_PERMIT` aus der 4diac-Standardbibliothek
  (`EI[PERMIT]` → `EO`), kein eigener; bereits an anderer Stelle im
  Repo genutzt (z. B. `test_B/Uebungen/Uebung_009.SUB`). Gegen die
  echte Datei im 4diac-Install (`typelibrary/events-3.0.0/typelib/
  E_PERMIT.fbt`) verifiziert. Kein eigener Baustein nötig.
- Demo-Subapplication `DecoratorDemo.sub`: `E_PERMIT` gatet
  `TrueUntil.TRIGGER` von außen, ohne `TrueUntil` selbst zu verändern
  (die "echte" Decorator-Variante der Folie, nicht die interne
  ECC-Erweiterung mit einem zweiten `TE`-Eingang)

`E_PERMIT` ist generisch und wiederverwendbar über Decorator hinaus –
genutzt vom Start/Stop-Pattern (siehe unten).

### Start/Stop pattern

Ordner: [`StartStopPattern/`](StartStopPattern/StartStopPattern.md)

- **Keine neuen Bausteine** – nur Standardbausteine
  `iec61499::events::E_SR` (Start/Stop-Zustand) und
  `iec61499::events::E_PERMIT` (Freigabe-Gate, wie beim Decorator).
  Dieselbe Kombination (`E_SR.Q` → `E_PERMIT.PERMIT`) existiert schon
  real im Repo für einen anderen Zweck: `test_B/Uebungen/Uebung_009.SUB`.
- Demo-Subapplication `StartStopDemo.sub`: `START`/`STOP` setzen ein
  `E_SR`; dessen `Q` gibt ein `E_PERMIT` frei, das ein `TRIGGER` zur
  (aus dem Chain-of-Actions-Pattern wiederverwendeten) `TrueUntil`-
  Instanz durchlässt – strukturell fast identisch zur Decorator-Demo,
  nur mit persistentem Start/Stop-Zustand statt einer beliebigen
  externen Bedingung.

Noch nicht in 4diac getestet.

### Reset pattern

Ordner: [`ResetPattern/`](ResetPattern/ResetPattern.md)

- **Keine neuen Bausteine** – Wiederverwendung von `TrueUntil.fbt` für
  den Reset-Baustein selbst, kein Gate davor.
- Demo-Subapplication `ResetDemo.sub`: kombiniert das Start/Stop-Muster
  (`START`/`STOP` → `E_SR` → `E_PERMIT` → `Worker.TRIGGER`) mit einem
  **separaten, ungegateten** `RESET` → `ResetWorker.TRIGGER`-Pfad, um
  den architektonischen Kernpunkt zu zeigen: Reset funktioniert auch,
  wenn die Anlage gestoppt ist (`E_SR.Q=FALSE`), der normale `TRIGGER`
  dagegen nicht.

Noch nicht in 4diac getestet.

### Purely Event-Driven function blocks

Ordner: [`PurelyEventDrivenPattern/`](PurelyEventDrivenPattern/PurelyEventDrivenPattern.md)

- Baustein `EventDrivenCylinder.fbt` (Folie 64): vollständig
  event-getriebene Fassung des Folienbeispiels `DoubleActingCylinder`
  – **null BOOL-Datenpins**, Sensoren (`AT_HOME`/`AT_END`) und
  Aktuatorbefehle (`EXTEND`/`RETRACT`) laufen komplett über Events,
  keine Algorithmen nötig.
- Kein separates Demo-Subapp – der Baustein ist wegen der fehlenden
  Datenpins direkt im FORTE-Monitoring testbar.

Offener Punkt: Interface-Namen sind von der Folie ablesbar, die genaue
ECC-Verdrahtung ist eine eigene, in sich schlüssige Rekonstruktion
(nicht pixelgenau von der Folie verifizierbar) – siehe
`PurelyEventDrivenPattern.md`. Noch nicht in 4diac getestet.

## Offen / geplant

Das letzte noch offene Pattern aus Modul 6 (IO abstraction layer,
Folie 63) wird bei Bedarf noch ergänzt.
