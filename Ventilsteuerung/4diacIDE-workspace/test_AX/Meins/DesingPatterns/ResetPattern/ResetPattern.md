# Design Pattern: Reset (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folie:

- **Folie 71 – "The reset pattern"** (Kategorie: *Compositional /
  Architectural*)

Zeigt dieselbe Cylinder-Beispielgrafik wie Handshake-/Start-Stop-Pattern
(Folien 69–72), diesmal mit hervorgehobenem `Reset`-Zweig: ein eigener
`TrueUntil`-artiger Baustein (`CylinderReset`), der direkt von einem
externen `RESET`-Event getriggert wird, **nicht** über das
`E_PERMIT`-Gate aus dem Start/Stop-Pattern.

Kein eigener Adapter, kein neuer Basis-Baustein nötig – reine
Wiederverwendung von `TrueUntil` (Chain-of-Actions-Pattern), diesmal
für einen isolierten Reset-Pfad.

## Einordnung

| Feld | Wert |
|---|---|
| Name | reset pattern |
| Kategorie | Compositional / Architectural |

## Das Grundproblem

Eine Anlage braucht neben der normalen, ggf. per Start/Stop gegateten
Betriebslogik einen **Reset-/Homing-Pfad**, der die Anlage in einen
sicheren/definierten Ausgangszustand zurückfährt. Würde dieser
Reset-Pfad genau wie die normale Betriebslogik durch dasselbe
Start/Stop-`E_PERMIT`-Gate laufen (siehe
[Start/Stop-Pattern](../StartStopPattern/StartStopPattern.md)), könnte
man die Anlage nicht zurücksetzen, während sie gestoppt ist – gerade
dann ist Reset aber oft am wichtigsten (z. B. nach einem Not-Stopp,
vor dem nächsten Start).

Die Lösung: Der Reset-Pfad wird **architektonisch getrennt** von der
normalen Betriebslogik geführt – eigener, direkter Trigger-Eingang
(`RESET`), der **nicht** durch das `E_PERMIT`-Gate läuft, sondern die
zuständige Aktion (hier wieder eine `TrueUntil`-Instanz) unmittelbar
und bedingungslos auslöst.

## Aufbau auf der Folie

Im gemeinsamen Cylinder-Beispiel sitzt der Reset-Zweig parallel zur
Extend/Retract-Kette: `RESET` (extern) → `TRIGGER` einer eigenen
`CylinderReset`-Instanz (`TrueUntil`-artig: `TRIGGER`/`REQ` →
`TO_POSITION`(hier `RETRACT`)/`STOP`/`DONE`, `inPosition`(hier
`atHome`)) – unabhängig vom `StartStopHandle`/`Started`-Gate, das nur
die Extend/Retract-Kette schützt.

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

- **Keine neuen Bausteine** – Wiederverwendung von `TrueUntil.fbt`
  (Chain-of-Actions-Pattern) für den Reset-Baustein selbst; kein Gate
  davor.
- **Demo:** `ResetDemo.sub` in diesem Ordner – kombiniert das
  Start/Stop-Pattern (`START`/`STOP` → `E_SR` → `E_PERMIT` →
  `Worker.TRIGGER`, wie in `StartStopDemo.sub`) mit einem **separaten,
  ungegateten** `RESET` → `ResetWorker.TRIGGER`-Pfad, um den
  architektonischen Unterschied explizit zu zeigen: `RESET` funktioniert
  auch dann, wenn `E_SR.Q` (Start/Stop-Zustand) `FALSE` ist –
  `TRIGGER` dagegen nicht.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Siehe `../DesignPatterns.md` für die Gesamtübersicht.
