# Design Pattern: Decorator (IEC 61499)

## Quelle

UAO "IEC 61499: primer course", Modul 6 – *Design methods and patterns*,
Valeriy Vyatkin (Luleå University of Technology / Aalto University).

Datei: `G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\UAO theme slides\Module 6. Design methods and patterns.pdf`

Relevante Folie:

- **Folie 68 – "Decorator"** (Kategorie: *Structural design pattern*,
  Problem: *"Conditional execution of FBs"*)

**Korrektur:** `E_PERMIT` ist ein **Standardbaustein der 4diac-
Standardbibliothek** (`iec61499::events::E_PERMIT`, aus
`Standard Libraries/events` in beiden Projekten – siehe die
existierende Nutzung z. B. in `test_B/Uebungen/Uebung_009.SUB`), kein
eigener, zu portierender Baustein. Der Treffer im Vyatkin-
Demoprojekt-Korpus (`en\Task1_Solution.sln\IEC61499\E_PERMIT.fbt`) war
nur eine lokale Kopie des Standardbausteins innerhalb des
EAE-Projekts (Pin-Name dort `E1`), nicht der Beleg für einen fehlenden
eigenen Baustein. Ich hatte das fälschlich als "noch nicht vorhanden"
interpretiert und eine eigene, überflüssige Kopie angelegt – die ist
wieder entfernt. Verwendet wird ausschließlich der echte
Standardbaustein mit seinen echten Pin-Namen `EI`/`EO`/`PERMIT`.

## Einordnung

| Feld | Wert |
|---|---|
| Name | Decorator |
| Kategorie | Structural design pattern |
| Problem laut Folie | Conditional execution of FBs |

## Das Grundproblem

Ein bestehender Baustein (hier: `TrueUntil` aus dem
[Chain-of-Actions-Pattern](../ChainOfActionsPattern/ChainOfActionsPattern.md))
soll manchmal übersprungen werden können ("führe diesen Schritt nur
aus, wenn Bedingung X gilt"), ohne den Baustein selbst zu verändern –
klassischer Decorator-Gedanke aus der objektorientierten Welt: Verhalten
per Umverdrahtung/Ummantelung hinzufügen statt die Originalklasse
anzufassen.

## Zwei Varianten auf der Folie

Die Folie zeigt zwei Implementierungen desselben Gedankens:

1. **Intern** (linke Bildhälfte): `TrueUntil` bekommt selbst einen
   zweiten BOOL-Eingang `TE` spendiert; die Transition `START` →
   `OPERATE` wird zu zwei Transitionen `TRIGGER AND TE` (ausführen) vs.
   `TRIGGER AND NOT TE` (direkt nach `DONE`, überspringen). Das
   **verändert** den Baustein selbst.
2. **Extern** (rechte Bildhälfte, `FB2`/`FB1`): Der generische
   Standard-Gate-Baustein `E_PERMIT` (`iec61499::events::E_PERMIT`)
   wird **vor** den unveränderten Baustein geschaltet: `TRIGGER` →
   `E_PERMIT.EI`, `TE` (BOOL) → `E_PERMIT.PERMIT`, `E_PERMIT.EO` →
   `TrueUntil.TRIGGER`. Ist `PERMIT` `FALSE`, wird das Event
   verschluckt, `TrueUntil` bekommt gar keinen `TRIGGER` und tut
   nichts.

**Umgesetzt wird hier ausschließlich Variante 2** – das ist der
eigentliche Decorator-Gedanke (Baustein bleibt unangetastet,
Verhalten kommt von außen dazu) und passt zu unserem bereits
bestehenden, unveränderten `TrueUntil.fbt`.

## `E_PERMIT` (Quelle: `Task1_Solution.sln/E_PERMIT.fbt`)

```
E_PERMIT
  Event-Eingang:   E1 (mit Qualifier PERMIT)
  Event-Ausgang:   EO
  BOOL-Eingang:    PERMIT
```

ECC (1:1 aus der Originaldatei übernommen):

- `START` (initial)
- `START` → `FORWARD` bei `E1[PERMIT]` (Event-Eingang mit Qualifier-
  Guard – feuert nur, wenn `PERMIT` zum Zeitpunkt von `E1` `TRUE` ist)
  – feuert `EO`
  (im Original heißt der Zielzustand `EO`, hier `FORWARD` genannt, um
  Verwechslung mit dem gleichnamigen Event zu vermeiden – funktional
  identisch)
- `FORWARD` → `START` (unbedingt)

Ist `PERMIT` `FALSE`, wenn `E1` eintrifft, gibt es keine passende
Transition aus `START` – das Event wird laut Standard-ECC-Semantik
einfach verworfen (kein `EO`, kein Zustandswechsel).

Da `E_PERMIT` generisch ist (kein Bezug zu `TrueUntil` oder irgendeinem
konkreten Baustein), wird es hier als eigenständiger, wiederverwendbarer
Baustein abgelegt – nicht nur für das Decorator-Pattern nützlich,
sondern z. B. auch für das später geplante Start/Stop-Pattern
(Folie 70), das laut Folie denselben Baustein verwendet.

## Umsetzung in diesem Repository (fertig, ungetestet in 4diac)

- **Baustein:** `.lib/adapter-3.0.0/typelib/events/E_PERMIT.fbt` –
  generischer Gate-Baustein, 1:1 aus der Originaldatei portiert (kein
  Adapter, reines Event+BOOL).
- **Demo:** `DecoratorDemo.sub` in diesem Ordner – ein
  `TrueUntil`-Baustein (aus dem Chain-of-Actions-Pattern,
  unverändert wiederverwendet), dessen `TRIGGER` über `E_PERMIT`
  gegatet wird. `TE` (BOOL) an der Subapp-Schnittstelle steuert, ob
  der `TRIGGER` überhaupt durchkommt.

## Weitere Design Patterns aus Modul 6 (zur späteren Umsetzung)

Siehe `../DesignPatterns.md` für die Gesamtübersicht.
