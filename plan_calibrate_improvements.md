# Plan: CALIBRATE Verbesserungen

## Ausgangslage

[`CALIBRATE.fbt`](Ventilsteuerung/4diacIDE-workspace/.lib/OSCAT/typelib/Basic/POUs/Engineering/measurements/CALIBRATE.fbt) funktioniert, hat aber zwei Probleme:

1. **Keine Reihenfolge-Erzwingung:** `CO` muss zwingend vor `CS` erfolgen, da `CS` den bereits berechneten `OFFSET` verwendet (`SCALE := Y_Scale / (X + OFFSET)`). Der SimpleFB lässt beide BOOL-Eingänge gleichzeitig oder in beliebiger Reihenfolge zu.
2. **`Y_Offset` ist nicht intuitiv:** Der Name klingt nach "Offset-Betrag" auf der Eingangsseite, ist aber tatsächlich ein **Sollwert auf der Ausgangsseite** ("Welchen Y-Wert soll ich bei diesem X liefern?").
   - **Tieferes Problem (nur E_CALIBRATE_SQ adressiert):** Nach `CO` gilt `Y = Y_Offset * SCALE` – also nur korrekt wenn `SCALE = 1.0`.  
     Die alte Formel `OFFSET := Y_Offset - X` liefert `Y = (X + (Y_Offset - X)) * SCALE = Y_Offset * SCALE`.  
     **Korrekt muss es sein:** `OFFSET := Y_Offset / SCALE - X`, damit `Y = (X + (Y_Offset/SCALE - X)) * SCALE = Y_Offset` **immer** gilt.

## Maßnahmen

### 1. `CALIBRATE.fbt` – Doku-Aufwertung

- **`Y_Offset` beibehalten** (zur Wahrung der Abwärtskompatibilität, aber in der Dokumentation klarstellen, dass es sich um einen Sollwert auf der Ausgangsseite handelt)
- **Dokumentation erweitern (Original-Formel bleibt unverändert):**
  - Formel: `Y = (X + OFFSET) * SCALE`
  - `CO` (Calibrate Offset): `OFFSET := Y_LOW - X` — speichert den Offset. **Achtung:** Nach CO gilt `Y = Y_LOW * SCALE`, also nur korrekt, wenn `SCALE = 1.0`. Für SCALE-unabhängiges CO siehe `E_CALIBRATE_SQ`.
  - `CS` (Calibrate Scale): `SCALE := Y_Scale / (X + OFFSET)` — speichert die Skalierung, damit bei aktuellem X der Sollwert Y_Scale erscheint
  - **Wichtig:** `CO` muss **vor** `CS` ausgeführt werden
- Lizenz-Header vervollständigen

### 2. `E_CALIBRATE_SQ.fbt` – Neuanlage

Event-gesteuerter BasicFB mit **ECC-erzwungener Reihenfolge** CO → CS.

#### Interface
| Typ | Name | Beschreibung |
|-----|------|-------------|
| EI | `REQ` | Normalbetrieb: berechne Y |
| EI | `EICO` | Offset kalibrieren (Punkt 1 setzen) |
| EI | `EICS` | Scale kalibrieren (Punkt 2 setzen) |
| EO | `CNF` | Bestätigung Normalbetrieb |
| EO | `EOCO` | Punkt 1 (Offset) kalibriert |
| EO | `EOCS` | Punkt 2 (Scale) kalibriert |
| Input | `X` | Rohwert |
| Input | `Y_Offset` | Soll-Y bei Punkt 1 (Low) |
| Input | `Y_Scale` | Soll-Y bei Punkt 2 (High) |
| Output | `Y` | Kalibrierter Ausgang |
| InOut | `OFFSET` (0.0) | Gespeicherter Offset |
| InOut | `SCALE` (1.0) | Gespeicherte Skalierung |

#### Interne Variablen
- `X_LOW_INT` (REAL): Speichert X-Wert von EICO
- `Y_LOW_INT` (REAL): Speichert Y_Offset von EICO

#### ECC (Zustandsautomat)

```
START ──REQ──→ REQ ──1──→ START       (Normalbetrieb, Y = (X+OFFSET)*SCALE)
START ──EICO─→ CO  ──1──→ WAIT_CS     (Referenzpunkt 1 speichern)
WAIT_CS ──REQ──→ REQ ──1──→ WAIT_CS  (Betrieb mit aktuellem OFFSET/SCALE)
WAIT_CS ──EICO─→ CO  ──1──→ WAIT_CS  (Referenzpunkt 1 neu setzen)
WAIT_CS ──EICS─→ CS  ──1──→ START     (Referenzpunkt 2 speichern + Berechnung)
```

**Enforcement:** `EICS` ist nur aus `WAIT_CS` erreichbar. Der Anwender muss zwingend zuerst `EICO` triggern.

#### Algorithmen

```
Algorithm REQ:  Y := (X + OFFSET) * SCALE;

Algorithm CO:   
  X_LOW_INT := X;
  Y_LOW_INT := Y_Offset;
  (* Optional: Sofortige Offset-Anpassung für die Anzeige bis EICS erfolgt *)
  IF SCALE <> 0.0 THEN OFFSET := Y_Offset / SCALE - X; ELSE OFFSET := Y_Offset - X; END_IF;

Algorithm CS:   
  (* Mathematisch entkoppelte Zwei-Punkt-Kalibrierung *)
  IF (X - X_LOW_INT) <> 0.0 THEN
    SCALE := (Y_Scale - Y_LOW_INT) / (X - X_LOW_INT);
    IF SCALE <> 0.0 THEN
      OFFSET := Y_LOW_INT / SCALE - X_LOW_INT;
    END_IF;
  END_IF;
```

**Kernunterschied zu CALIBRATE:** Durch Speicherung von `X_LOW_INT` und `Y_LOW_INT` kann `CS` beide Parameter (`SCALE` und `OFFSET`) so berechnen, dass die Gerade exakt durch beide Punkte (Punkt 1 von EICO und Punkt 2 von EICS) geht. Die Reihenfolge-Erzwingung stellt sicher, dass die Basisdaten vorhanden sind.

## Ablauf

1. `CALIBRATE.fbt` editieren: Doku verbessern, Lizenz-Header
2. `E_CALIBRATE_SQ.fbt` neu anlegen im selben Ordner
3. Beide Dateien mit `python script/check_missing_ax.py` und `python script/scan_bad_names.py` validieren
