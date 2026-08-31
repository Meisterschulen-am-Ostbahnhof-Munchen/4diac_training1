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
| Structural (creational) | Purely Event-Driven function blocks | – | offen |
| Structural (creational) | Generic Actuation | – | offen |
| Structural (creational) | Decorator | – | offen |
| Architectural | IO abstraction layer | – | offen |
| Compositional | Chain of actions | – | offen |
| Behavioural | Chain of actions | – | offen |

## Weitere Patterns laut Folie 69 ("Miscellaneous design patterns")

| Kategorie | Pattern | Ordner | Status |
|---|---|---|---|
| Compositional / Architectural | Start/Stop pattern | – | offen |
| Compositional / Architectural | reset pattern | – | offen |
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

## Offen / geplant

Die übrigen Patterns aus Modul 6 (Purely Event-Driven function blocks,
Generic Actuation, Decorator, IO abstraction layer, Chain of actions,
Start/Stop pattern, reset pattern) werden nach und nach in eigenen
Unterordnern nach demselben Schema ergänzt.
