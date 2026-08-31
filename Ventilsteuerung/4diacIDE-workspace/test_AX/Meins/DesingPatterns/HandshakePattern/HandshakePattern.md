# Design Pattern: Handshake (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folien:

- Folie 62 – Übersicht "Design Patterns for IEC 61499" (Structural, Architectural, Compositional, Behavioural)
- Folie 69 – "Miscellaneous design patterns": Start/Stop-Pattern, Reset-Pattern, **Handshake-Pattern**
- Folie 70 – The Start/Stop pattern
- Folie 71 – The reset pattern
- **Folie 72 – The handshake pattern** (Kategorie: *Behavioural*)

Das Handshake-Pattern ist Teil einer Dreiergruppe von Patterns, die zusammen
in einem einzigen Beispiel (Cylinder ↔ NextSystem) vorgeführt werden:
Start/Stop-Pattern (Freigabe der Ausführung über `E_PERMIT`), Reset-Pattern
(separater Reset-Pfad) und Handshake-Pattern (die Kommunikation zwischen dem
Cylinder-Baustein und dem nachgelagerten System). Für die Implementierung
hier interessiert uns ausschließlich der Handshake-Mechanismus selbst – er
ist unabhängig von Cylinder/Start-Stop/Reset einsetzbar.

## Einordnung

| Feld | Wert |
|---|---|
| Name | Handshake pattern |
| Kategorie | Behavioural |
| Problem laut Folie | "Handshake implementation via IEC 61499 adapters" |

## Das Grundproblem

Wenn zwei Function Blocks (oder Subapplications, oder Geräte) eine
Anfrage/Antwort-Beziehung haben – A fragt bei B etwas an, B bestätigt oder
meldet unaufgefordert etwas zurück, A quittiert das wiederum – braucht man
dafür im einfachsten Fall vier einzelne Event-Verbindungen (REQ, CNF, IND,
RSP) plus ggf. Datenverbindungen dazu. Bei mehreren solchen Beziehungen
zwischen vielen Bausteinen entsteht schnell die auf Folie 11 gezeigte
"Spaghetti connections"-Problematik.

Die Lösung: Man bündelt die vier Events (und optionale Nutzdaten) in einem
**Adapter-Typ**. Die Verbindung zwischen den beiden Kommunikationspartnern
wird dann durch eine einzige Adapterverbindung (Socket ↔ Plug) hergestellt
statt durch vier einzelne Event-Linien.

## Das REQ/CNF/IND/RSP-Vokabular

Das Handshake-Pattern verwendet exakt das klassische
Request/Indication/Response/Confirm-Servicemodell, das auch allen
IEC 61499 Service-Interface-Function-Blocks (SIFBs) zugrunde liegt
(z. B. `SUBSCRIBE`, `SERVER`/`CLIENT`, `PUBLISH`) – hier aber als
eigenständiger, wiederverwendbarer Adaptertyp statt fest in einem SIFB
verdrahtet:

- **REQ** – Anfrage vom Requester ("Client") an den Responder ("Server"): *"Bitte tu X."*
- **CNF** – Bestätigung vom Responder zurück an den Requester: *"X erledigt / X quittiert."* (synchron zur REQ)
- **IND** – unaufgeforderte Meldung vom Responder an den Requester: *"Es ist etwas passiert."*
- **RSP** – Antwort des Requesters auf eine IND: *"Meldung erhalten / verarbeitet."*

Diese vier Events bilden zusammen den Adapter-Interface-Typ. Auf der Folie
heißt dieser Typ **`EVENT_HS`**:

```
EVENT_HS
  Event-Eingänge:  CNF, IND
  Event-Ausgänge:  REQ, RSP
```

(In der Grunddeklaration – d. h. aus Sicht der **Plug**-Seite – sind CNF
und IND Eingänge, REQ und RSP Ausgänge; siehe Abschnitt "Socket vs. Plug"
unten für die Begründung dieser Zuordnung. Keine Datenanschlüsse in der
minimalen Fassung der Folie; in der Praxis kann man dem Adapter bei Bedarf
zusätzlich Datenpins mitgeben, siehe Abschnitt "Erweiterungen" unten.)

## Socket vs. Plug

Wie jeder IEC 61499-Adapter hat auch `EVENT_HS` zwei Sichten auf dieselbe
Schnittstelle (siehe Folien 12/13/48 zum generellen Adapter-Mechanismus).

**Wichtig, per echtem 4diac-Compiler-Verhalten verifiziert** (die XSD/ECC-
Validierung prüft nur, ob `HS.<Name>` irgendein am Adapter deklariertes
Event ist – nicht, ob die Richtung an dieser Seite überhaupt Sinn ergibt;
das muss man selbst sicherstellen):

- **Plug** (`Name>>` – Adaptername mit angehängten `>>`):
  behält die in der Adapterdeklaration festgelegte Richtung bei.
  REQ/RSP sind hier als ECAction-**Output** feuerbar, CNF/IND sind als
  ECTransition-**Condition** auswertbar.
  → Das ist die **Requester-Rolle** ("Client"): stellt Anfragen (REQ),
  empfängt Bestätigungen (CNF), empfängt unaufgeforderte Meldungen (IND)
  und quittiert sie mit RSP.

- **Socket** (`>>Name` – Adaptername mit führenden `>>` am Baustein):
  spiegelt die Richtung. CNF/IND sind hier als ECAction-**Output**
  feuerbar, REQ/RSP sind als ECTransition-**Condition** auswertbar.
  → Das ist die **Responder-Rolle** ("Server"): nimmt Anfragen (REQ)
  entgegen, quittiert sie (CNF), meldet unaufgefordert Ereignisse (IND)
  und nimmt die Quittierung (RSP) entgegen.

Damit ist im FBNetwork-Editor der Requester der Plug (der sich "in den"
Responder-Socket einsteckt) – die üblichere, natürlichere Leserichtung
(Requester links/initiierend, Responder rechts/antwortend). Der
mitgelieferte Standardadapter `templates/Adapter.adp` benennt es zwar
andersherum (Socket dort als anfragende Seite), aber welche Seite Plug
und welche Socket ist, ist pro Adaptertyp frei wählbar – hier wurde
bewusst so entschieden.

```
        Requester (Plug)               Responder (Socket)
        ┌───────────────┐             ┌───────────────┐
   ...  │   HS   >>      │◄──Adapter──►│      >>   HS   │  ...
        │  REQ ─────────►│             │────────► REQ   │
        │  RSP ─────────►│             │────────► RSP   │
        │◄───────── CNF  │             │  CNF ◄─────────│
        │◄───────── IND  │             │  IND ◄─────────│
        └───────────────┘             └───────────────┘
```

Eine einzige Adapterverbindung (in den Folien als dicke orange Linie
dargestellt) ersetzt damit die vier einzelnen Event-Verbindungen zwischen
Requester und Responder. In `AdapterConnections` steht die Plug-Instanz
als `Source`, die Socket-Instanz als `Destination` (vgl. bestehende
Beispiele im Repo, z. B. `ErsteAutomatisierung.SUB`).

## Beispiel aus der Folie (Cylinder ↔ NextSystem)

Auf Folie 69/72 wird das Pattern am Beispiel eines `Cylinder`-Bausteins
gezeigt, der über seinen Adapter `HS>>` (Plug) mit einem
`NextSystem`-Baustein verbunden ist, der den Adapter als `>>HS` (Socket)
anbietet – das deckt sich direkt mit der hier gewählten Zuordnung:
`Cylinder` (Plug) spielt die Requester-Rolle, `NextSystem` (Socket) die
Responder-Rolle. Im Composite-Innenleben von `Cylinder` ist die
`HS`-Adapterinstanz an die Extend/Retract-"Chain of Actions"-Kette und an
`E_SR`-Latches (Extender/Retractor) angebunden, zusätzlich zum
Start/Stop-Pattern (`StartStopHandle` + `E_PERMIT`) und zum Reset-Pattern
(separater `CylinderReset`-Zweig). Dieses konkrete Zylinder-Beispiel ist
aber nur die Vorführung im Kurs – der Handshake-Mechanismus selbst
(`EVENT_HS`, Socket/Plug, REQ/CNF/IND/RSP) ist unabhängig von Zylindern
und in diesem Repo generisch implementiert.

## Umsetzung in diesem Repository (fertig)

### 1. Adapter-Typ

- **Ablageort:** `Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/events/Handshake/EVENT_HS.adp`
  (parallel zu den bestehenden `events/TimeOut/`, `events/bidirectional/`,
  `events/unidirectional/`).
- **Name:** `EVENT_HS` (1:1 wie in der Kursfolie).
- **Interface:** EventInputs `CNF`, `IND`; EventOutputs `REQ`, `RSP`
  (aus Sicht der Plug-Seite – Plug=Requester, Socket=Responder, siehe
  "Socket vs. Plug" oben). Inhaltlich exakt wie auf Folie 72, ohne
  Datenanschlüsse (minimale/kanonische Form des Patterns).

### 2. Beispiel-Bausteine

- **Ablageort:** dieser Ordner
  (`test_AX/Meins/DesingPatterns/HandshakePattern/`).
- Zwei generische, vom Zylinder-Beispiel losgelöste Demo-Bausteine
  (Basic FBs, nicht Composite – die ganze Logik steckt in der ECC):
  - `HandshakeRequester.fbt` – nutzt `EVENT_HS` als **Plug**. Sendet auf
    `START` ein `REQ`, meldet `DONE` bei `CNF`, reagiert auf `IND` mit
    `RSP` und meldet `NOTIFIED`.
  - `HandshakeResponder.fbt` – nutzt `EVENT_HS` als **Socket**. Beantwortet
    ein eingehendes `REQ` mit `CNF`, sendet auf `TRIGGER` ein
    unaufgefordertes `IND`, nimmt die passende `RSP` entgegen.
  - `HandshakePatternDemo.sub` – koppelt beide über eine einzige
    `AdapterConnections`-Verbindung (`Source="Requester.HS"`,
    `Destination="Responder.HS"`, da Requester=Plug, Responder=Socket),
    mit Init-Kette und an die Subapp-Schnittstelle durchgereichten
    Test-Triggern/Zählern.

**Wichtiger Stolperstein bei der Umsetzung:** Die 4diac-XSD-/ECC-Validierung
prüft bei `HS.<Name>` in einer `ECTransition`-`Condition` oder einem
`ECAction`-`Output` nur, ob `<Name>` überhaupt am Adapter deklariert ist –
**nicht**, ob die Richtung an dieser Socket-/Plug-Seite Sinn ergibt. Ein
Baustein, bei dem REQ/CNF/IND/RSP an der falschen Seite oder in der
falschen Rolle (Condition statt Output oder umgekehrt) verwendet werden,
kompiliert trotzdem fehlerfrei – die Logik muss man selbst korrekt
zusammenbauen, siehe Abschnitt "Socket vs. Plug" oben.

### 3. Validierung

Jede `.adp`/`.fbt`/`.sub`-Datei wird gegen die zugehörige XSD-Schema
geprüft:

```bash
python .agents/skills/iec61499-creator/scripts/validate.py <Pfad_zur_Datei>
```

XSD-grün heißt dabei **nicht** semantisch korrekt (siehe Stolperstein
oben) – die eigentliche Verhaltensprüfung passiert nur beim Test in der
4diac IDE / FORTE-Monitoring.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Aus derselben Foliensammlung, für spätere Iterationen in
`DesingPatterns/`:

- Structural: *Purely Event-Driven function blocks*, *Generic Actuation*, *Decorator*
- Architectural: *IO abstraction layer*
- Compositional/Behavioural: *Chain of actions*
- Compositional/Architectural: *Start/Stop pattern*, *reset pattern*
