# Design Pattern: TokenRing / Mutual Exclusion (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folie:

- **Folie 15 – "Mutual Exclusion"** (im Kapitel "Modelling PLC systems",
  *nicht* Teil der formalen Pattern-Tabelle auf Folie 62/69 – siehe
  Abschnitt "Einordnung" unten)

**Primärquelle gefunden (2026-08-31):** Die Folie basiert auf

> W. Dai, V. Vyatkin, J. H. Christensen, V. Dubinin, *"Function Block
> Implementation of Service Oriented Architecture: Case Study,"*
> IEEE INDIN 2014 (lokal: `INDIN14_DVCD.pdf`).

Abschnitt III.B/IV.A und Fig. 7/10 dort zeigen exakt das `CControlTRAS`-
Beispiel mit `MTXIN`/`MTXOUT` vom Typ `TokenRing`, das Folie 15/16
übernimmt. Zusätzlich bestätigt

> R. Sinha, V. Vyatkin, Z. Salcic, H. J. Park, *"Competitors or
> Cousins? Studying the Parallels between Distributed Programming
> Languages SystemJ and IEC61499"* (lokal:
> `Competitors_or_Cousins_Studying_the_para.pdf`)

dieselbe CylH/CylV-Konstellation in Worten: *"a cylinder fires only
when a work-piece has arrived and it holds the token. A cylinder
passes the token to the other cylinder after moving a work-piece and
retracting the pusher or when no work-piece is present."*

Kein Adaptertyp in den ~30 herunterladbaren EAE-Demoprojekten von
Vyatkin selbst (siehe Memory `vyatkin-demo-corpus`) – dieses Pattern
existiert nur in den beiden o. g. Papers, nicht als lauffähiges
Beispielprojekt.

## Einordnung

| Feld | Wert |
|---|---|
| Name (im Repo) | TokenRing pattern |
| Kategorie laut Folienbeschriftung | "(adapter) interfaces to mutual exclusion protocol (Ring Token protocol)" |
| Taxonomie Folie 62/69 | **nicht gelistet** – anders als Handshake taucht dieses Pattern nicht in der offiziellen "Design Patterns for IEC 61499"-Tabelle auf, sondern nur als Beispiel im Kapitel "Modelling PLC systems" |

**Wichtiger Unterschied zum Handshake-Pattern:** Für Handshake gab es auf
der Folie selbst eine eigene, ausführlich beschriftete Nahaufnahme
(Folie 72) mit Adapter-Interface-Deklaration. Für TokenRing zeigt die
Folie nur die beiden Adapterinstanzen (`MTXIN`, `MTXOUT`) mit den
Portnamen `GIVE`/`RCV`, ohne eigene Deklarations-Nahaufnahme oder
Fließtext daneben – die Protokollbeschreibung dazu steht im Fließtext
des INDIN14-Papers (s. o.), nicht auf der Folie selbst.

## Das Grundproblem

Zwei (oder mehr) Controller teilen sich eine physische Ressource, auf die
immer nur einer zugreifen darf (im Beispiel: zwei Zylinder `CylH`/`CylV`,
die sich einen gemeinsamen Werkstückträger/eine gemeinsame Achse teilen –
siehe `wpsv`/`wpsh` in der Skizze auf Folie 15). Statt die Interlocking-
Logik hart zwischen den Controllern zu verdrahten, wird ein
**Token-Ring-Protokoll** verwendet: Ein "Token" (eine Berechtigungsmarke)
zirkuliert reihum zwischen den Controllern; nur wer gerade das Token hält,
darf die geteilte Ressource benutzen; ist er fertig, reicht er das Token
an den nächsten Controller im Ring weiter.

Wie beim Handshake-Pattern wird dieser Mechanismus als eigener,
wiederverwendbarer **Adapter-Typ** (`TokenRing`) gekapselt, statt die
Interlocking-Events einzeln zu verdrahten.

## Aufbau auf der Folie

Auf Folie 15 hat jeder der beiden `CControlTRAP`-Controller (`CTLH`,
`CTLV`) zwei Adapterinstanzen vom Typ `TokenRing`:

- `MTXIN` – Portbeschriftung `RCV`/`GIVE`
- `MTXOUT` – Portbeschriftung `GIVE`/`RCV`

Die orange Linie zwischen `CTLH.MTXOUT`/`MTXIN` und `CTLV.MTXOUT`/`MTXIN`
ist als "Mutex based interlocking (Ring Token protocol) implemented via
adapter connections" beschriftet. Mit nur zwei Controllern bilden `MTXOUT`
von `CTLH` und `MTXIN` von `CTLV` (und umgekehrt) einen geschlossenen
Zwei-Knoten-Ring; bei mehr Controllern würde sich das reihum fortsetzen
(`MTXOUT` von A → `MTXIN` von B, `MTXOUT` von B → `MTXIN` von C, …, bis
zurück zu A).

Zusätzlich zeigt Folie 15 noch einen zweiten Adapter (`SREQ`, Typ
"service" – der generische Request/Confirm/Indication/Response-Adapter
aus Folie 48/`EVENT_HS_WSTRING`), der dort für die *Freigabebedingung*
("Interlocking condition (permits to operate if Q=TRUE)") zuständig ist,
nicht für das Token-Passing selbst. Das ist ein separates Thema und hier
nicht Teil des TokenRing-Patterns.

## GIVE/RCV-Semantik (durch INDIN14-Paper bestätigt)

Aus Abschnitt III.B des INDIN14-Papers: *"an adapter **input** MTXIN
and **output** MTXOUT are reserved"* – das bestätigt direkt (und
unabhängig von jeder Pixel-Interpretation der Folien-Grafik):
`MTXIN` = **Input-Adapter = Socket**, `MTXOUT` = **Output-Adapter =
Plug**. Genau das deckt sich mit dem am Handshake-Pattern real gegen
4diac verifizierten Socket/Plug-Verhalten (Plug übernimmt die
deklarierte Richtung unverändert, Socket spiegelt sie – siehe
`HandshakePattern.md`, Abschnitt "Socket vs. Plug"):

```
TokenRing
  Event-Eingänge:  RCV   – Bestätigung vom Empfänger, dass das Token angekommen ist
  Event-Ausgänge:  GIVE  – Token an den Nachbarn weiterreichen
```

- **Plug** (`MTXOUT`, "Geber"): feuert `GIVE` (reicht das Token weiter),
  reagiert auf `RCV` (Empfangsbestätigung vom Nachbarn – danach ist
  sicher, dass das Token wirklich übergeben wurde).
- **Socket** (`MTXIN`, "Empfänger"): reagiert auf `GIVE` (Token
  angekommen → darf jetzt in den kritischen Abschnitt), feuert `RCV`
  (Empfangsbestätigung zurück an den Geber).

Damit hat jeder Controller **zwei** Adapterinstanzen: `MTXOUT` (Plug,
Richtung zum nächsten Controller im Ring) und `MTXIN` (Socket, Richtung
vom vorherigen Controller im Ring) – exakt wie auf der Folie und in
Fig. 10 des Papers gezeichnet (dort für den 2-Zylinder-Fall: `CylH.MTXOUT`
→ `CylV.MTXIN`, `CylV.MTXOUT` → `CylH.MTXIN`). Aus dem Sinha/Vyatkin-
Paper zusätzlich bestätigt: der Token-Halter arbeitet (falls ein
Werkstück wartet) und reicht das Token danach weiter – oder reicht es
sofort weiter, falls kein Werkstück wartet (kein Warten auf Arbeit
nötig). Genau dieses Verzweigungsverhalten (`CHECK_WANT` →
`DO_CS`/direkt `PASS_ON`) implementiert `TokenRingNode.fbt`.

## Wo wird das Token tatsächlich übergeben?

Kurze Antwort: **Es werden gar keine Daten übergeben — das Token IST das
Event.**

`TokenRing.adp` ist bewusst datenlos:

```
EventInputs:  RCV   (Event, keine Nutzlast)
EventOutputs: GIVE  (Event, keine Nutzlast)
```

Es gibt keine `VarDeclaration`, kein `WSTRING`/`BOOL`-Feld, nichts, das
man als "das Token" tragende Nutzdaten bezeichnen könnte. Die Semantik ist: **das
Feuern von `GIVE` selbst ist die Übergabe.** Wer gerade zwischen "hat
`MTXIN.GIVE` empfangen" und "hat `MTXOUT.GIVE` weitergereicht" steht
(in `TokenRingNode.fbt` zwischen den ECC-Zuständen `HANDLE_GIVE` und
`PASS_ON`), "hat" das Token – nicht weil irgendwo eine Variable das
sagt, sondern weil in diesem Moment genau dieser Baustein gerade in
dieser Phase seiner Zustandsmaschine steckt. Keine Daten tragen den
Zustand, der Kontrollfluss tut es.

Das ist kein Bug, sondern die klassische Umsetzung eines
Token-Ring-Protokolls in einem Event-System – analog zu echten
Token-Ring-Netzwerken, wo das "Token" auch nur ein bestimmtes
Bitmuster/Frame ist, dessen bloßes Eintreffen die Sendeberechtigung
überträgt, ohne dass eine fachliche Nutzlast nötig wäre. Auch Vyatkins
Original (INDIN14-Paper) spezifiziert keine Nutzlast für GIVE/RCV.

**Wo das aber tatsächlich eine Schwäche ist:** Es gibt keine
Möglichkeit, ein dupliziertes oder verlorenes Token zu erkennen (z. B.
wenn `SEED` versehentlich zweimal gefeuert wird, zirkulieren zwei
Token gleichzeitig, und nichts im System bemerkt das). Ein Token mit
Nutzlast (z. B. laufende Sequenznummer oder Ersteller-ID) würde das
erkennbar machen – genau das haben wir beim Handshake-Pattern mit
`EVENT_HS_WSTRING` als datentragende Zusatzvariante gemacht, hier
(bewusst, siehe "Datenlos" unten) bisher nicht.

## Zweite Fundstelle: TokenRing auch in der SoA-Beispielanwendung (Folie 47)

Ergänzung vom 2026-09-02: Beim Nachtragen der bisher fehlenden
"Message exchange between services"-Dokumentation (siehe
[`HandshakePattern.md`](../HandshakePattern/HandshakePattern.md),
Abschnitt "Die Quelle der `push,100`-Notation") zeigte sich, dass
`TokenRing` auch auf **Folie 47 ("SoA implementation in function
blocks")** derselben Foliensammlung auftaucht: Der Orchestrator-
Baustein `CylMES` (Typ `CControlTRAS`) hat dort einen `TokenRing`-
Adapter (`>>MTXIN`/`MTXOUT>>`) **zusätzlich zu** zwei generischen
Service-Adaptern (`SREQ1>>`/`SREQ2>>`). Hier dient `TokenRing` nicht
dem gegenseitigen Ausschluss zweier gleichberechtigter Zylinder (wie
im `CylH`/`CylV`-Beispiel oben), sondern dem reihum-Ansprechen
mehrerer nachgeschalteter Service-Teilnehmer – derselbe Adaptertyp,
zweite, andere Verwendung. Bestätigt zusätzlich unabhängig vom
INDIN14-Paper, dass `TokenRing` ein durchgängig in Vyatkins Material
wiederverwendetes generisches Muster ist, nicht nur eine Einzelfall-
Lösung für das Mutual-Exclusion-Beispiel.

## Dritte Fundstelle: Vyatkins eigene mündliche Erklärung (Video-Transkript)

Ergänzung 2026-09-04: Das Auto-Transkript von Vyatkins eigenem Vortrag
zu Folie 48 (`Module 6.2 Adapters.mp4`,
`G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\Videos\Module 6.2 Adapters.transcript.txt`,
Quelle: https://www.youtube.com/watch?v=zDQRY5efevQ) beschreibt exakt
dieses Pattern in eigenen Worten, unabhängig von den beiden Papers
oben:

> "we can slightly modify the previous design by adding one more
> adapter connection between these two controller blocks that will be
> passing the token and this way implementing Mutual exclusion so that
> only one cylinder can operate the one which has a token and then we
> can Implement simple ring token protocol uh where the token is
> passed all the time from One controller to another until the
> controller receives the [I]n signal that workpiece has arrived and
> in this case it performs pushing operation keeping the token and not
> letting the other cylinder to operate [...] this design helps us to
> build a lot more complex systems like in this case we have four
> interacting cylinders we can easily scale up this design"

Bestätigt unabhängig: (a) das Token zirkuliert kontinuierlich, bis ein
Controller ein Werkstück meldet, (b) der Controller behält das Token
während der Operation (kein Loslassen, während gearbeitet wird),
(c) genau das in `TokenRingNode.fbt` implementierte Verzweigungsverhalten
(`CHECK_WANT`→`DO_CS`/direkt `PASS_ON`), (d) die Skalierbarkeit auf
mehr als zwei Knoten ("four interacting cylinders") – deckt sich mit
der bewussten Entscheidung, `TokenRingPatternDemo.sub` mit 5 statt nur
2 Knoten zu bauen.

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

- **Adapter-Typ:** `TokenRing` (dataless, EventInputs `RCV`,
  EventOutputs `GIVE`) in
  `.lib/adapter-3.0.0/typelib/types/bidirectional/TokenRing/TokenRing.adp`.
- **Beispielbaustein:** `TokenRingNode.fbt` – ein Controller im Ring,
  mit `MTXIN` (Socket) und `MTXOUT` (Plug), Init/Initialized/DeInit-
  Muster wie bei den Handshake-Bausteinen, `REQUEST`-Event zum Anfordern
  des kritischen Abschnitts, `SEED`-Event zum einmaligen Bootstrappen
  des Rings.
- **Demo-Subapplication:** `TokenRingPatternDemo.sub` – 5-Knoten-Ring
  (`NodeA`…`NodeE`, `NodeE.MTXOUT` schließt zurück auf `NodeA.MTXIN`) –
  bewusst mehr als 2 Knoten, damit es ein echter Ring ist und nicht nur
  ein Zwei-Knoten-Hin-und-Her wie im CylH/CylV-Beispiel des Papers.
  Analog zu "Four processes" (Folie 16 / Fig. 11-13 des Papers), nur mit
  fünf statt vier Teilnehmern.
- **Datenlos** wie `EVENT_HS` (nicht wie der datentragende "service"-
  Adapter) – eine Payload-Variante (z. B. Werkstück-/Anforderer-ID)
  könnte analog zu `EVENT_HS_WSTRING` ergänzt werden, falls gebraucht.

Noch offen: reale 4diac-Validierung (XSD ist grün, aber wie beim
Handshake-Pattern prüft das nicht, ob Socket/Plug-Richtung und ECC-Logik
tatsächlich stimmen).

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Siehe `../DesignPatterns.md` für die Gesamtübersicht.
