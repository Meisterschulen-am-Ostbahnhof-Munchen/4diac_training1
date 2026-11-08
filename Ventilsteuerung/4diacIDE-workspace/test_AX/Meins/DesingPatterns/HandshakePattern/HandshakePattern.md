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

- **Ablageort:** `Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/types/bidirectional/Handshake/EVENT_HS.adp`
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

**Zweiter Stolperstein (INIT-Sequenz):** Die INIT-Behandlung darf nicht als
Entry-Action des Idle-Zustands eingebaut werden (`ECState "Idle"` mit
`Algorithm="OnInit" Output="INITO"` direkt dran) – sonst feuert `OnInit`
(und damit `INITO`, und ein Reset der Zähler) bei jedem Rücksprung in den
Idle-Zustand erneut, nicht nur beim echten Initialisieren. Richtig ist das
Muster aus `TemplateBasic.fbt`: ein eigener `Init`-Zustand, nur erreichbar
über eine mit dem Qualifier bewachte Transition `Condition="INIT[TRUE = QI]"`,
danach eine unbedingte Transition in einen separaten `Initialized`-Idle-
Zustand (von dem aus die eigentliche Handshake-Logik abzweigt); dazu
symmetrisch ein `DeInit`-Zustand über `Condition="INIT[FALSE = QI]"`
zurück nach `START`. Beide Demo-Bausteine sind entsprechend aufgebaut.

### 3. Validierung

Jede `.adp`/`.fbt`/`.sub`-Datei wird gegen die zugehörige XSD-Schema
geprüft:

```bash
python .agents/skills/iec61499-creator/scripts/validate.py <Pfad_zur_Datei>
```

XSD-grün heißt dabei **nicht** semantisch korrekt (siehe Stolperstein
oben) – die eigentliche Verhaltensprüfung passiert nur beim Test in der
4diac IDE / FORTE-Monitoring.

## Erweiterungen

### Die Quelle der `"push,100"`-Notation: Message Exchange zwischen Services (Folie 41–48)

Bisher stand in diesem Dokument nur ein beiläufiger Verweis auf
`"push,100"`. Das eigentliche Diagramm dazu – **"Message exchange
between services"** – war bisher nirgends beschrieben, obwohl es in
der PDF sehr ausführlich behandelt wird. Nachgetragen (Korrektur
2026-09-02: exakt nachgezählt, es sind fünf Folien, nicht drei):

- **Folie 41** – Titelfolie mit den beiden Struktur-/Rollen-Diagrammen
  (`MES`→`WP Sensor`/`Cylinder`/`Drop`, sowie `Cylinder`→
  `Start Sens`/`End Sens`/`Push Valve`/`Pop Valve`) und der `CylH`-
  Mechanik-Skizze – **noch ohne** das eigentliche Message-Sequence-
  Chart (MSC).
- **Folien 42–46** – dieselbe MSC-Grafik fünfmal wiederholt (Build-
  Animation): Inhalt (alle Lifelines, alle Nachrichten) ist auf allen
  fünf Folien **identisch**, nur der gelb hinterlegte
  Hervorhebungsbereich wandert von Folie zu Folie weiter nach unten
  (Folie 42: keine Hervorhebung; Folie 43: INIT-Sequenz +
  "Workpiece arrived"; Folien 44–46: weitere Ausschnitte bis
  "Service completed"). Jede der 18 unten aufgelisteten Konstanten
  ist bereits auf Folie 42 vollständig sichtbar.

**Das Beispiel:** Ein Zylinder `CylH` transportiert ein Werkstück
zwischen Startposition (`WPS`-Sensor) und Endposition. Er besteht aus
vier unabhängigen, jeweils eigenständig service-fähigen Teilen:
`CYL.start` (Startpositions-Sensor), `CYL.end` (Endpositions-Sensor),
`CYL.push` (Push-Ventil) und `CYL.pop` (Pop-/Rückhol-Ventil). Ein
übergeordneter Controller `CYL` bündelt diese vier zu einem einzigen
Service für den Orchestrator `MES` ("Manufacturing Execution System");
`DS` ist der Ziel-Sink, an den das Werkstück am Ende übergeben wird.
Jeder dieser Teilnehmer (`MES`, `WPS`, `CYL`, `CYL.start`, `CYL.end`,
`CYL.push`, `CYL.pop`, `DS`) ist eine eigene Lifeline im Message-
Sequence-Chart (MSC) auf Folie 42 (identisch auch auf 43–46, siehe
oben).

**Die Nachrichten-Konvention:** Jede Anfrage/Antwort ist ein einzelner
String (WSTRING), nach einem einfachen, selbstbeschreibenden Schema:

- `REQ,"<value>"` – Anfrage, trägt nur den rohen Parameter (z. B.
  `REQ,"100"` an `CYL.push`: "fahre auf 100").
- `RSP,"<name>,<value>"` – Antwort, trägt zusätzlich den Namen des
  gemeldeten Zustands/Service (z. B. `RSP,"push,100"`: "push-Ventil
  steht jetzt auf 100"; `RSP,"start,1"`: "Startsensor meldet 1").

Diese `"name,value"`-Formatierung in der Antwort ist genau die
Notation, die in `EVENT_HS_WSTRING`s Default-Payloads (`"push,100"`,
weiter unten in diesem Dokument) zitiert, aber bisher nie referenziert
wurde.

**Der Ablauf (verkürzt, aus dem MSC auf Folie 42–46):**

1. Alle Teilnehmer initialisieren (`INIT` → `RSP,"start,1"` /
   `RSP,"end,0"` / `RSP,"WPS,0"` usw.).
2. *Workpiece arrived:* `WPS` meldet `RSP,"WPS,1"` an `MES`; `MES`
   schickt `REQ,"trip"` an `CYL` ("mach die Rundfahrt"); `CYL` schickt
   `REQ,"100"` an `CYL.push`, bekommt `RSP,"push,100"` zurück, meldet
   `RSP,"CYL,STARTED"` an `MES`.
3. *Pusher reached end position:* `CYL.end` meldet `RSP,"end,1"`; `CYL`
   meldet `RSP,"CYL, END POS"` an `MES`, schickt `REQ,"drop"` an `DS`
   (bekommt `RSP,"ack"`), fährt dann `CYL.push` zurück auf `0`
   (`REQ,"0"` → `RSP,"push,0"`) und `CYL.pop` auf `100`
   (`REQ,"100"` → `RSP,"pop,100"`); `CYL.end` fällt zurück auf
   `RSP,"end,0"`.
4. *Pusher reached start position:* `CYL.start` meldet `RSP,"start,1"`;
   `CYL` meldet `RSP,"CYL, START POS"`; `CYL.pop` wird auf `0`
   zurückgefahren (`REQ,"0"` → `RSP,"pop,0"`).
5. *Service completed:* `CYL` meldet `RSP,"CYL, Trip Complete"` an
   `MES`.

**Verbindung zur SoA-Implementierung (Folie 47/48):** Dieselbe
`CylH`-Anwendung zeigt Folie 47 ("SoA implementation in function
blocks") als konkrete Function-Block-Schaltung: Der Orchestrator-
Baustein `CylMES` (Typ `CControlTRAS`) hat einen `TokenRing`-Adapter
(`>>MTXIN`/`MTXOUT>>`) **und** zwei generische Service-Adapter
(`SREQ1>>`/`SREQ2>>`) – der Beleg dafür, dass `TokenRing` in diesem
Beispiel nicht für gegenseitigen Ausschluss zwischen zwei Zylindern
verwendet wird (wie im `CylH`/`CylV`-Mutual-Exclusion-Beispiel, siehe
[`TokenRingPattern.md`](../TokenRingPattern/TokenRingPattern.md)),
sondern zum reihum-Ansprechen mehrerer Service-Teilnehmer (`SREQ1`,
`SREQ2`) – derselbe Adaptertyp, zweite, andersartige Anwendung.

Folie 48 ("Implementation of Adapters") zeigt daneben die generische
**Adapter-Typ-Deklaration** des `"service"`-Adapters selbst: EventInputs
`REQ`/`RSP`, EventOutputs `CNF`/`IND`, dazu `REQD`/`RSPD` (WSTRING-Inputs)
und `CNFD`/`INDD` (WSTRING-Outputs) – exakt die vier Events und vier
Datenpins, die `EVENT_HS_WSTRING` (unten) 1:1 übernimmt.

**Diskrepanz gelöst (2026-09-04, per Video-Transkript):** Die
Bildunterschrift auf Folie 48 lautet *"When used as Plug the adapter's
instance is mirrored"* – wörtlich genommen schien das der in Abschnitt
"Socket vs. Plug" oben **live gegen den echten 4diac-Compiler
verifizierten** Regel dieses Repos zu widersprechen ("Plug behält die
deklarierte Richtung bei, Socket spiegelt"). Aufgelöst durch Vyatkins
eigenes Auto-Transkript zu genau dieser Folie
(`G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\Videos\Module 6.2 Adapters.transcript.txt`,
Quelle: https://www.youtube.com/watch?v=zDQRY5efevQ), wörtlich:

> "the adapter interface in the composite block on the left hand side
> is declared as [...] output [...] which is called plug but on the
> right hand side it's declared as a socket so plug is plugged into
> the socket **and it is mirrored** [...] we can see that [...] the
> left hand side composite block has three inputs and four data
> outputs while here [rechts, Socket] it's mirrored so it has three
> data output and four inputs"

Das bestätigt **exakt** die in diesem Repo verifizierte Regel: Plug
behält seine deklarierte Richtung (links, 3 in/4 out), Socket ist die
gespiegelte Seite (rechts, 4 in/3 out) – "it is mirrored" bezieht sich
im Video eindeutig auf die **Socket**-Seite, nicht wörtlich auf "when
used as Plug" wie die Folienunterschrift knapp/missverständlich
formuliert. Die Folie 48 selbst bleibt also leicht irreführend
formuliert, aber Vyatkins gesprochene Erklärung UND die live gegen
4diac verifizierte Regel stimmen überein – kein echter Widerspruch
mehr.

### Das konkrete Beispiel: `MessageExchangeDemo` (Folie 47, fertig, ungetestet in 4diac)

Vollständige Umsetzung des `CylH`-Beispiels aus "SoA implementation in
function blocks" (Folie 47) als vier zusammenspielende Bausteine, alle
in diesem Ordner:

- **`const/MessageExchangeConst.gcf`** – alle 18 auf Folie 42–46
  vorkommenden Nachrichtenwerte als benannte `WSTRING`-Konstanten
  (`REQ_TRIP`, `REQ_EXTEND`="100", `REQ_RETRACT`="0", `REQ_DROP`,
  `RSP_WPS_ABSENT`/`ARRIVED`, `RSP_START_TRIGGERED`,
  `RSP_END_IDLE`/`TRIGGERED`, `RSP_PUSH_EXTENDED`/`RETRACTED`,
  `RSP_POP_EXTENDED`/`RETRACTED`,
  `RSP_CYL_STARTED`/`END_POS`/`START_POS`/`TRIP_COMPLETE`, `RSP_ACK`).
- **`WorkpieceSensor.fbt`** (`WPSensor`/`a1WPS1`) – Plug `ACTIVATE`
  (`EVENT_HS_ACK_WSTRING`). Auf `DETECT` (manuell in FORTE feuerbar)
  sendet es `REQ` mit `REQ_TRIP`; meldet `DONE`, sobald das `CNF`
  zurückkommt. Vereint bewusst die beiden MSC-Lifelines `WPS` und
  `MES` in einem Baustein, genau wie auf der Folie.
- **`CylinderOrchestrator.fbt`** (`CylMES`/`CControlTRAS`) – Socket
  `SRSP` (`EVENT_HS_ACK_WSTRING`, von `WorkpieceSensor`), Plug `SREQ1`
  (volles `EVENT_HS_WSTRING`, zu `CylinderService` – braucht die
  Zwischenmeldung), Plug `SREQ2` (`EVENT_HS_ACK_WSTRING`, zu
  `DropSinkService`). Reagiert auf `SREQ1.IND` ("Endposition erreicht")
  mit einer `SREQ2.REQ` (Drop anfordern) und erst nach deren `CNF` mit
  einer `SREQ1.RSP` ("darfst jetzt einfahren").
- **`CylinderService.fbt`** (`SCylH`/`CylHServ`) – Socket `SRSP`
  (volles `EVENT_HS_WSTRING`). Simulierte Sensor-Events `AT_END`/
  `AT_START` (manuell feuerbar) statt echter Hardware, analog zu
  `EventDrivenCylinder.fbt`. Feuert `IND` bei `RSP_CYL_STARTED` und bei
  `RSP_CYL_END_POS` – **wartet dort auf `RSP` vom Orchestrator**, bevor
  es einfährt (der einzige echte Synchronisationspunkt im Beispiel:
  der Zylinder darf erst zurückfahren, wenn der Drop bestätigt ist).
  Schließt mit `CNF`=`RSP_CYL_TRIP_COMPLETE` ab.
- **`DropSinkService.fbt`** (`DSServ`) – Socket `SRSP`
  (`EVENT_HS_ACK_WSTRING`). Jede `REQ` wird unbedingt mit
  `CNF`=`RSP_ACK` bestätigt.
- **`MessageExchangeDemo.sub`** – koppelt alle vier über drei
  `AdapterConnections` (`WorkpieceSensor.ACTIVATE→Orchestrator.SRSP`,
  `Orchestrator.SREQ1→Cylinder.SRSP`, `Orchestrator.SREQ2→Sink.SRSP`),
  reicht `DETECT`/`AT_END`/`AT_START` zum manuellen Durchsteppen des
  Ablaufs sowie `WPS_TripResult`/`WPS_TripCount`/`DS_LastReqPayload`/
  `DS_ReqCount` zur Beobachtung nach außen durch.

**Bewusst weggelassen gegenüber der Folie:** Der `TokenRing`-Adapter
(`MTXIN`/`MTXOUT`) für die Mehr-Controller-Verriegelung und der
konstant-`TRUE`-`Enable`/`Permit`-Adapter (`CONST1`). Diese Demo hat
nur einen `CylinderOrchestrator`, also nichts, wogegen zu
verriegeln wäre, und keinen Grund, einen immer-`TRUE`-Permit extra zu
verdrahten. `TokenRing` selbst ist bereits separat umgesetzt, siehe
[`TokenRingPattern.md`](../TokenRingPattern/TokenRingPattern.md).

**Zeigt alle drei Adapter-Reduktionsstufen der `EVENT_HS`-Familie in
einem realistischen Zusammenhang:** volles `EVENT_HS_WSTRING` dort, wo
eine echte Zwischenmeldung nötig ist (`SREQ1`), reduziertes
`EVENT_HS_ACK_WSTRING` dort, wo nur Anfrage+Bestätigung gebraucht
werden (`SRSP`, `SREQ2`) – genau die Motivation hinter den vier
reduzierten Varianten unten in "Weitere Handshake-Varianten".

### Datentragende Variante: `EVENT_HS_WSTRING`

Ablageort: `.lib/adapter-3.0.0/typelib/types/bidirectional/Handshake/EVENT_HS_WSTRING.adp`
(gleicher Ordner, gleiches Socket/Plug-Rollenschema wie `EVENT_HS`).

Entspricht 1:1 Vyatkins eigenem generischen **"service"-Adapter**
(Folie 48, genutzt auf Folien 15/47 für SoA-Service-Interfaces und
Prozessdaten-Interfaces): dieselben vier Events `REQ`/`CNF`/`IND`/`RSP`,
jedes zusätzlich mit einer `WSTRING`-Nutzlast gekoppelt
(`REQD`/`CNFD`/`INDD`/`RSPD`, jeweils über `<With Var="...">` an das
zugehörige Event gebunden – wie im offiziellen 4diac-Standardadapter
`templates/Adapter.adp`). Passt zum textbasierten Nachrichtenstil aus
den Message-Sequence-Beispielen der Folie (z. B. `"push,100"`).

Bewusst (noch) kein eigener, engerer Datentyp (z. B. `LREAL` für eine
Zylinderposition) – lässt sich bei konkretem Bedarf jederzeit als
weitere, enger typisierte Variante ergänzen, analog zur bestehenden
`typelib/types/`-Familie (`AX`/`ADI`/`AR`/`AL`/`ALR`/`AS`/`AB`, je
unidirektional und bidirektional).

Beispielbausteine (analog zu `EVENT_HS`, gleiches Init/Initialized/DeInit-
Muster, gleiche Zustandsnamen):

- `HandshakeRequesterWSTRING.fbt` – Plug/Requester. `START` trägt
  `ReqPayload` (Default `"push,100"`), lädt es vor dem Senden in
  `HS.REQD`; `DONE`/`NOTIFIED` liefern `CnfPayload`/`IndPayload` aus
  `HS.CNFD`/`HS.INDD`.
- `HandshakeResponderWSTRING.fbt` – Socket/Responder. Liest `HS.REQD`
  nach `LastReqPayload`, antwortet mit fixem `HS.CNFD := "ack"`; `TRIGGER`
  lädt `IndPayload` (Default `"status,ok"`) in `HS.INDD`; liest
  `HS.RSPD` nach `LastRspPayload`.
- `HandshakePatternDemoWSTRING.sub` – koppelt beide, analog zu
  `HandshakePatternDemo.sub`.

**Verifiziert:** Adaptereigene Datenvariablen (`REQD`/`CNFD`/`INDD`/
`RSPD`) werden in ST-Algorithmen genauso mit `HS.`-Präfix angesprochen
wie die Events (`HS.REQD`, `HS.CNFD` usw.) – in 4diac gegengetestet,
keine Fehlermeldung.

Die feste Bestätigungs-Payload `"ack"` (Responder-CNF, Requester-RSP)
steht nicht als Literal im Code, sondern als globale Konstante:
`const/HandshakeConst.gcf` (Package
`Meins::DesingPatterns::HandshakePattern::const`, Konstante
`ACK_PAYLOAD`), per `<Import>` in beide `...WSTRING.fbt`-Bausteine
eingebunden und dort als `HandshakeConst::ACK_PAYLOAD` referenziert –
gleiches Muster wie `logiBUS::utils::quarter::const::quarter` im
`quarter`-Paket.

`HandshakePatternDemoWSTRING.sub` exponiert `ReqPayload`/`IndPayload`
zusätzlich als eigene `InputVars` (Defaults `"push,100"`/`"status,ok"`),
sodass sie beim Instanziieren per `Parameter` überschrieben werden
können, statt nur an den internen Requester/Responder-Defaults zu
hängen.

### Weitere Handshake-Varianten: reduzierte Event-Sets

Vier zusätzliche Adaptertypen, alle im selben Ordner wie `EVENT_HS`/
`EVENT_HS_WSTRING`, die das volle REQ/CNF/IND/RSP-Vokabular gezielt
reduzieren – nützlich, wenn eine Beziehung nachweislich nie die volle
Vier-Event-Choreografie braucht (siehe `MessageExchangeDemo` oben für
ein Beispiel, das drei dieser Varianten nebeneinander einsetzt):

- **`EVENT_HS_UNI`** – nur `REQ` (datenlos), keinerlei Antwort. Reines
  Fire-and-Forget, **kein echter Handshake** (der Socket kann weder
  bestätigen noch ablehnen, der Plug erfährt nie, ob die Anfrage
  überhaupt ankam) – bewusst so dokumentiert, nicht versehentlich als
  Ersatz für `EVENT_HS` gedacht.
- **`EVENT_HS_UNI_WSTRING`** – wie `EVENT_HS_UNI`, plus `REQD`-Payload
  (`WSTRING`).
- **`EVENT_HS_ACK`** – nur `REQ`/`CNF` (datenlos), kein `IND`/`RSP`.
  Anders als `EVENT_HS_UNI` ein **echter** (wenn auch einseitiger)
  Handshake: jede `REQ` bekommt eine `CNF`. Passend, wenn der Socket
  nie unaufgefordert etwas melden muss.
- **`EVENT_HS_ACK_WSTRING`** – wie `EVENT_HS_ACK`, plus `REQD`/`CNFD`-
  Payload (`WSTRING`). Wird in `MessageExchangeDemo` für `SRSP` und
  `SREQ2` verwendet (reine Anfrage/Bestätigung, keine
  Zwischenmeldung nötig).

Alle vier folgen demselben Socket/Plug-Rollenschema wie `EVENT_HS`
(Plug behält die deklarierte Richtung, Socket spiegelt) und sind
gegen die XSD validiert.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Aus derselben Foliensammlung, für spätere Iterationen in
`DesingPatterns/`:

- Structural: *Purely Event-Driven function blocks*, *Generic Actuation*, *Decorator*
- Architectural: *IO abstraction layer*
- Compositional/Behavioural: *Chain of actions*
- Compositional/Architectural: *Start/Stop pattern*, *reset pattern*
