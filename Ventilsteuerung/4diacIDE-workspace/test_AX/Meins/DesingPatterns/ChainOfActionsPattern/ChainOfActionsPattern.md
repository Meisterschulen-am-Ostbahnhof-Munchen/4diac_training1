# Design Pattern: Chain of Actions (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folien:

- Folie 65 – "Generic Actuation" (Category: *Structural*, Problem: *Code
  reusability*) – führt den generischen Baustein `TrueUntil` ein
- **Folie 66 – "Chain of Actions"** (Category: *Behavioural,
  Compositional*, Problem: *"Spaghetti code"*, *Code reusability in
  IEC 61499*) – einfaches Beispiel (Vakuumgreifer mit zwei Zylindern
  `LC`/`RC`)
- Folie 67 – "Chain of Actions: more complex example" (Problem: *Zu
  viele Transitions, wenn State-Logik als ECC implementiert wird*) –
  reales Werkstück-Handling mit 5 verketteten Aktionsbausteinen
- Folie 68 – "Decorator" – Erweiterung von `TrueUntil` um eine zweite
  BOOL-Eingangsvariable `TE` für bedingte Ausführung (eigenes,
  separates Pattern, hier nicht Teil der Umsetzung)

Im Gegensatz zu TokenRing ist dieses Pattern Teil der offiziellen
"Design Patterns for IEC 61499"-Übersicht (Folie 62) und auf den
Folien selbst mit Interface- und ECC-Diagramm dokumentiert – kein
externes Paper nötig (im Vyatkin-Demoprojekt-Korpus wurde trotzdem
nach `TrueUntil`/`TO_POSITION`/"Chain of Action" gesucht: keine
Treffer, siehe Memory `vyatkin-demo-corpus`).

## Einordnung

| Feld | Wert |
|---|---|
| Name | Chain of actions |
| Kategorie | Behavioural, Compositional |
| Problem laut Folie | "Spaghetti code"; Code-Wiederverwendbarkeit in IEC 61499; zu viele Transitions, wenn State-Logik als ein einziges ECC implementiert wird |

## Das Grundproblem

Eine mehrstufige Bewegungssequenz (z. B. "fahre Zylinder A aus, dann
Zylinder B aus, dann Zylinder B ein, dann Zylinder A ein") lässt sich
als EIN großes ECC mit vielen Zuständen/Transitionen implementieren –
das wird schnell unübersichtlich ("Spaghetti-Code", vgl. das
Problem, das schon beim Handshake-Pattern über
"Spaghetti connections" beschrieben wurde, hier aber auf ECC-Ebene
statt auf Verbindungsebene).

Die Lösung: Man zerlegt die Sequenz in gleichartige, wiederverwendbare
**Aktions-Bausteine** (`TrueUntil`, s. u.) und verkettet sie über
`DONE`→`TRIGGER`-Verbindungen zu einer linearen Kette – jeder Baustein
kennt nur seinen eigenen Schritt, die Reihenfolge ergibt sich rein aus
der Verdrahtung, nicht aus einem zentralen ECC.

## Der generische Baustein: `TrueUntil` (Folie 65, "Generic Actuation")

```
TrueUntil
  Event-Eingänge:  TRIGGER, REQ
  Event-Ausgänge:  TO_POSITION, STOP, DONE
  BOOL-Eingang:    inPosition
```

Idee: "Fahre in eine Position (`TO_POSITION`) und warte, bis `inPosition`
wahr wird (`DONE`)." Generisch, weil derselbe Baustein für JEDE
Bewegungsart (Zylinder ausfahren, Zylinder einfahren, Schieber
bewegen, Greifer öffnen/schließen …) wiederverwendet wird – nur über
`TRIGGER`/`inPosition` extern angebunden, ohne eigene
Zylinder-spezifische Logik.

ECC (aus der Folien-Grafik abgeleitet):

- **START** (initial)
- `START` → `OPERATE` bei `TRIGGER`
- `OPERATE` → `MOVING` (unbedingt) – feuert `TO_POSITION`
  (`MOVE` ist ein reserviertes ST-Schlüsselwort, daher `MOVING` im
  Baustein)
- `MOVING` → `STOP` bei `inPosition` – feuert `STOP` und `DONE`
- `STOP` → `START` (zurück in den Idle-Zustand, bereit für den nächsten
  `TRIGGER`/`REQ`) – **nicht** zurück nach `OPERATE`, sonst würde sich
  wegen `OPERATE`s unbedingter Transition nach `MOVING` eine
  Endlosschleife ergeben

**Offener Punkt:** Die genaue Rolle von `REQ` neben `TRIGGER` ist aus
der komprimierten Folien-Grafik nicht zweifelsfrei ablesbar (evtl. ein
Abbruch-/Wiederholungs-Event, das ebenfalls nach `STOP` führt). Für die
Umsetzung hier wird `REQ` vorerst wie `TRIGGER` behandelt (erneutes
Anstoßen der Bewegung), das kann bei Bedarf noch präzisiert werden.

## Beispiel aus der Folie: Vakuumgreifer (Folie 66)

Zwei Zylinder `LC` (links, `LChome`/`LCend`) und `RC` (rechts,
`RChome`/`RCend`) tragen gemeinsam eine Vakuum-Saugvorrichtung `VC`
(`vcu`/`vcd`) über vier Werkstückpositionen `pp0`–`pp3`. Die Kette
lautet: `LCExtend` → `RCExtend` → … (weitere Aktionen, "other actions",
gestrichelt angedeutet) … → `RCRetract` → `LCRetract`, jeweils über
`DONE`(Vorgänger) → `TRIGGER`(Nachfolger) verbunden. Jeder Kettenglied-
Baustein ist eine `TrueUntil`-Instanz mit eigenem `inPosition`-Signal
(z. B. `LCend`, `RCend`, …).

## Komplexeres Beispiel (Folie 67)

Werkstück-Handling mit 5 verketteten Aktionsbausteinen
(`RaiseLift`/`SimpleMove`, `Eject`, `SlideWorkpiece`/`SimpleMove`,
`LowerLift`/`SimpleMove`, `RejectWorkpiece`/`RejectBlock`), zusätzlich
mit `E_SWITCH`/`E_MERGE`-Bausteinen für Verzweigungen (z. B.
"Werkstück zurückweisen" als Alternativpfad) und mehrere `DONE`-Ausgänge,
die über `E_MERGE` zu gemeinsamen Ausgangs-Events (`WP_REJECTED`,
`DONE`, `EJECTOR_EXTEND`, `LOWER_LIFT`, …) zusammengeführt werden. Das
ist die Erweiterung des Grundmusters um Verzweigung/Zusammenführung –
für die Erstumsetzung hier zunächst nicht nachgebaut (siehe
"Umsetzung", Abgrenzung).

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

- **Baustein:** `TrueUntil.fbt` – generischer Aktions-Baustein wie auf
  Folie 65/66, kein Adapter nötig (reine Events/BOOL), kein
  INIT/INITO (wie auf der Folie – bewusst weggelassen, kein Zustand,
  der initialisiert werden müsste).
  Ablageort: `test_AX/Meins/DesingPatterns/ChainOfActionsPattern/`.
- **Demo:** `ChainOfActionsDemo.sub` – Kette aus 4 `TrueUntil`-Instanzen
  (`Step1`…`Step4`, analog zum LCExtend/RCExtend/RCRetract/LCRetract-
  Beispiel von Folie 66, aber generisch benannt statt
  zylinderspezifisch, wie schon beim Handshake-Pattern von der
  konkreten Zylinder-Domäne losgelöst), verkettet über
  `DONE`→`TRIGGER`. Jede Stufe hat ein eigenes, an der Subapp-
  Schnittstelle exponiertes `StepN_InPosition`-BOOL, mit dem sich das
  "Erreichen der Position" beim Testen manuell simulieren lässt.
- **Abgrenzung:** Das komplexere Beispiel mit Verzweigung/`E_MERGE`
  (Folie 67) ist eine spätere Erweiterung, kein Teil dieser Umsetzung.
- **Decorator** (Folie 68, `TrueUntil` + `TE`-Bedingung) ist ein
  eigenes Pattern und hier nicht enthalten – siehe
  `../DesignPatterns.md`.

Noch offen: reale 4diac-Validierung (XSD ist grün, das prüft aber wie
bei den anderen Patterns weder Socket/Plug-Richtung noch ECC-Logik).

## Ground-truth-Referenz: `RequestQueueManager.fbt`

Kein Vyatkin-Folien-Pattern, sondern ein echter, funktionierender
Baustein aus dem UAO-Curriculum-Download (`Elevator_DumbButtons_EAE_
Final.sln`, `IEC61499/RequestQueueManager.fbt`, EAE/nxtControl-Format),
1:1 nach 4diac portiert (gleiche Interface/ECC/Algorithmen, nur
Format-Übersetzung). Gefunden bei der Suche nach zusätzlichem
Referenzmaterial im Downloads-Curriculum-Ordner.

Ein Aufzug-Anfragen-Arbitrierer: klassischer SCAN-Sweep über 3 Etagen,
kombiniert Chain-of-Actions-artige Sequenzierung (eine Handvoll
Zustände, ein linearer Ablaufkreis) mit REQ/CNF-Service-Vokabular
(dasselbe Vokabular wie beim Handshake-Pattern). `CNF` feuert zweimal
pro bedienter Anfrage (Ankunft, dann Fertigstellung) mit
unterschiedlicher Payload statt zwei separater Event-Namen – ein
reales, nicht selbst erdachtes Beispiel für diesen Stil. **Löst nicht**
die oben offene Frage zu `TrueUntil`s `REQ` vs. `TRIGGER` (anderer
Baustein, andere REQ-Semantik) – nur ein thematisch verwandter,
unabhängiger Präzedenzfall.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Siehe `../DesignPatterns.md` für die Gesamtübersicht.
