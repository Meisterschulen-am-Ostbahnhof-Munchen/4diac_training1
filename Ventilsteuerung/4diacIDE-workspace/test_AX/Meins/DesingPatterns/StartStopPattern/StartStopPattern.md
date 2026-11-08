# Design Pattern: Start/Stop (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folie:

- **Folie 70 – "The Start/Stop pattern"** (Kategorie: *Compositional /
  Architectural*, Problem: *"Separate start-stop logic implied by HMI
  console from the main control logic"*)

Kein eigener Adapter, keine neuen Bausteine nötig – nur Standard-4diac-
Bausteine (`E_SR`, `E_PERMIT`), siehe Abschnitt "Bausteine" unten.

## Einordnung

| Feld | Wert |
|---|---|
| Name | Start/Stop pattern |
| Kategorie | Compositional / Architectural |
| Problem laut Folie | Start/Stop-Logik von einer HMI-Konsole von der eigentlichen Steuerlogik trennen |

## Das Grundproblem

Eine Anlage soll über ein separates HMI-Bedienfeld (Start-/Stopp-Taste)
insgesamt ein- und ausgeschaltet werden können, unabhängig davon, was
die eigentliche Steuerlogik gerade tut. Verdrahtet man diese
Start/Stop-Freigabe direkt in die Kernlogik hinein, vermischen sich
zwei Zuständigkeiten (Bedien-Zustand vs. fachliche Ablaufsteuerung),
die eigentlich unabhängig voneinander änderbar sein sollten.

Die Lösung: Der Start/Stop-Zustand wird als eigener, persistenter
Zustand (`E_SR`-Latch: `S`=Start, `R`=Stop, `Q`=aktuell läuft/steht)
modelliert und über ein Freigabe-Gate (`E_PERMIT`, siehe
[Decorator-Pattern](../DecoratorPattern/DecoratorPattern.md)) vor die
eigentliche Trigger-Logik geschaltet – exakt derselbe
`E_PERMIT`-Mechanismus wie beim Decorator-Pattern, nur dass die
Freigabebedingung hier nicht eine beliebige externe Bedingung ist,
sondern speziell ein persistenter Start/Stop-Zustand.

## Bausteine (beide Standard, real gegen 4diac verifiziert)

```
E_SR (iec61499::events::E_SR)
  Event-Eingänge:  S (Set), R (Reset)
  Event-Ausgang:   EO
  BOOL-Ausgang:    Q

E_PERMIT (iec61499::events::E_PERMIT)
  Event-Eingang:   EI (mit Qualifier PERMIT)
  Event-Ausgang:   EO
  BOOL-Eingang:    PERMIT
```

Verdrahtung: `START` → `E_SR.S`, `STOP` → `E_SR.R`; `E_SR.Q` →
`E_PERMIT.PERMIT` (das Gate ist offen, solange die Anlage gestartet
ist); das eigentliche Auslöse-Event läuft durch `E_PERMIT.EI` → `EO`
und erreicht die Steuerlogik nur, solange `Q=TRUE` ist.

Diese exakte Kombination (`E_SR.Q` → `E_PERMIT.PERMIT`) existiert
bereits real und getestet im Repo, wenn auch für einen anderen
Anwendungsfall: `test_B/Uebungen/Uebung_009.SUB` (ein Ticker, der nur
zählt, während `E_SR.Q` – dort per Taster hin- und hergeschaltet –
`TRUE` ist).

## Aufbau auf der Folie

Im (mit Handshake/Reset gemeinsam gezeigten) Cylinder-Beispiel sitzt
`StartStopHandle` (`E_SR`) mit `Started` (`E_PERMIT`) direkt vor der
Extend/Retract-Kette: `S`/`R` kommen von `START`/`STOP`-Events (z. B.
von einer HMI), `Q` geht als `PERMIT` in `Started`; das ankommende
Service-Request-Event (`REQ` des Handshake-Adapters `HS`) läuft durch
`Started.EI`→`EO`, bevor es die Extend/Retract-Bausteine überhaupt
erreicht – die Anlage reagiert also nur auf Anfragen, solange sie
"gestartet" ist.

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

- **Keine neuen Bausteine** – nur `iec61499::events::E_SR` und
  `iec61499::events::E_PERMIT` (Standardbibliothek).
- **Demo:** `StartStopDemo.sub` in diesem Ordner – `START`/`STOP`
  setzen/löschen ein `E_SR`; dessen `Q` gibt ein `E_PERMIT` frei, das
  ein `TRIGGER`-Event zur (aus dem Chain-of-Actions-Pattern
  wiederverwendeten, unveränderten) `TrueUntil`-Instanz durchlässt –
  nur während die Anlage "gestartet" ist, kommt der `TRIGGER` überhaupt
  an. Strukturell fast identisch zur Decorator-Demo, nur mit `E_SR`
  als Quelle der Freigabebedingung statt einer beliebigen externen
  `TE`-Variable.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Siehe `../DesignPatterns.md` für die Gesamtübersicht.
