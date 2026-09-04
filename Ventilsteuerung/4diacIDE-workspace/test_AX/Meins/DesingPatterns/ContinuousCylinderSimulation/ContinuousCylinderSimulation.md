# Ground-truth reference: continuous-time cylinder simulation (`CylinderHCore`)

## Quelle

**Kein Vyatkin-Folien-Pattern** – dieser Ordner ist keine Umsetzung
eines der 10 Module-6-Design-Patterns, sondern ein **originalgetreu
portierter Referenzbaustein** aus dem UAO-Curriculum-Download:

`C:\Users\franz\Downloads\UniversalAutomation.org\UAO - IEC 61499 curriculum - Dokumente\General\Version 0\en\Final.sln\IEC61499\CylinderH\CylinderH.fbt`

(identische Kopien auch in `LiftingLuggage_20240201-122924720.sln`,
`LiftingLuggage_final.sln`, `LiftingLuggage_starter.sln`, `Starter.sln`
– fünf Übungsprojekte insgesamt). Gefunden bei der gezielten Suche
nach `*.fbt`-Dateien im gesamten Curriculum-Ordner, mit der Hoffnung,
damit die als "nicht pixel-verifiziert" / "eigene Rekonstruktion"
geflaggte ECC von `EventDrivenCylinder.fbt`
([`PurelyEventDrivenPattern.md`](../PurelyEventDrivenPattern/PurelyEventDrivenPattern.md))
und `CylinderService.fbt`
([`HandshakePattern.md`](../HandshakePattern/HandshakePattern.md))
gegenzuprüfen.

## Wichtige Erkenntnis: andere Modellierungstechnik, keine Verifikation

`CylinderH` bestätigt **nicht** unsere Rekonstruktion – es ist eine
**grundlegend andere Modellierungstechnik**:

| | `EventDrivenCylinder.fbt` / `CylinderService.fbt` | `CylinderHCore.fbt` (dieser Ordner) |
|---|---|---|
| Modell | diskrete Event-Zustandsmaschine | kontinuierliche Zeit-Simulation |
| Datenpins | keine (Purely Event-Driven) bzw. nur WSTRING-Payload | `REAL POSITION`, laufend aktualisiert |
| Antrieb | Events (`EXTEND_REQ`, `AT_END`, …) | `E_CYCLE`-Tick alle 20 ms |
| Positionsberechnung | keine – Position ist reine Kontrollfluss-Semantik | echte Integration (`integEC`) über die Zeit |

Damit ist `CylinderHCore` eher ein Beleg für die Folien **50–52**
("Modelling Event-driven PLCs system" / "Modelling a Scan-based PLCs
System" im Kapitel "Modelling PLC systems") als für das
"Purely Event-Driven function blocks"-Pattern (Folie 63/64) – eine
andere, bisher in diesem Repo nicht umgesetzte Modellierungsart.

## Bestätigung durch Vyatkins Video-Transkript (2026-09-04)

Das Auto-Transkript zu Folie 50-52 (`Module 6.4 Modelling PLC
systems.mp4`,
`G:\Geteilte Ablagen\Classroom\Students\UAO-Curriculum\en\Module 06 – Design Patterns\Videos\Module 6.4 Modelling PLC systems.transcript.txt`,
Quelle: https://www.youtube.com/watch?v=2t0AZtp2WPs) bestätigt genau
den hier verwendeten Mechanismus – zyklische Aktivierung per `E_CYCLE`
mit konfigurierbarem `DT`, um unterschiedliche PLC-Geschwindigkeiten
zu modellieren:

> "using the very same structure we can also Implement even modeling
> of scan based plcs of a classic PLC so we can take the very same
> interface blocks but Implement them as a basic blocks with just one
> additional state where the original control code written in
> structure text is executed [...] to implement different speed of
> each PLC one can activate this function block cyclically using
> e cycle block and the DT constant of each e cycle block can be set
> to the required value to model the particular speed of the PLC like
> [...] 20 milliseconds in one case and 100 milliseconds in the other"

Das bestätigt unabhängig die `E_CYCLE`+`DT`-basierte Grundidee hinter
`CylinderHCore.fbt` (hier `T#20ms`) – allerdings anhand des
Zweizylinder-Beispiels mit geteilter Variable (Shared-Variable-Sync
über Event+Daten), nicht anhand von `CylinderH`s konkreter
Integrator-Mathematik selbst; die genaue ECC/Formel von `integEC`
bleibt weiterhin nur durch den Curriculum-Quellcode belegt, nicht
durch dieses Video.

## Aufbau

- **`integEC.fbt`** – generischer zeitbasierter Integrator (Basic FB,
  originalgetreu portiert). Integriert `pv1`/`pv2` über `cycleTime`,
  optional geclampt auf `[minValue, maxValue]`.
- **`ChangeDetect.fbt`** – einfacher Änderungsfilter (Basic FB,
  originalgetreu portiert). Feuert `CHG` nur, wenn sich der `REAL`-Wert
  tatsächlich geändert hat.
- **`CylinderHCore.fbt`** – Composite FB, verdrahtet `Tick`
  (`iec61499::events::E_CYCLE`, **Standard-4diac-Baustein**, nicht neu
  angelegt), `Model` (`integEC`) und `Filter` (`ChangeDetect`).

## Bewusste Reduktion gegenüber dem Original

Das Original (`CylinderH.fbt`) hat zusätzlich eine `Interface1`-Instanz
vom Typ `CylinderH_HMI` – ein natives EAE "Service Interface Function
Block" **ohne** portierbare ECC/Algorithmen (reines
`QI`/`QO`-Init-Durchreichen plus HMI-Anzeige). Deren einzige
*strukturelle* Rolle – `Model.INITO` weiterzureichen, um den
`E_CYCLE`-Tick zu starten und das eigene `INTO` zu feuern – wird hier
direkt verdrahtet, ohne die HMI-Hülle. `LABEL` (nur für die HMI-Anzeige
gedacht) wurde ebenfalls weggelassen.

**Nicht portiert** (bewusst, siehe Antwort auf Rückfrage "wie
originalgetreu?"): die Sensor-Hülle `CylinderHSens.fbt` (fügt zwei
`Sensor`-Instanzen für Start-/Endschalter hinzu) und die
Ventil-Hülle `CylinderHSensValve.fbt` (fügt `ValveControlSR` hinzu) –
beide liegen unverändert im Original-Curriculum-Ordner, falls später
eine vollständigere Portierung gewünscht ist.

## Weitere Design Patterns aus Modul 6

Siehe [`../DesignPatterns.md`](../DesignPatterns.md) für die
Gesamtübersicht der zehn umgesetzten Patterns – dieser Ordner ist
bewusst kein elftes Pattern, sondern nur Referenzmaterial.
