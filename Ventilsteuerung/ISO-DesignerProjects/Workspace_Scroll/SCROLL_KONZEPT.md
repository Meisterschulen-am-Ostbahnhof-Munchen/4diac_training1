# Scroll-Baustein — Konzept (ISO-Designer-Variante)

Dieses Dokument beschreibt, wie die scrollbare Liste im ISO-Designer-Pool
`Workspace_Scroll/DefaultPool/DefaultPool.jop` aufgebaut ist, warum sie so
aufgebaut ist, und wie man sie erweitert (mehr Zeilen, andere Spalten). Für
allgemeines `.jop`/`.jvi`-Hintergrundwissen (CProxy-Mechanismus, ID-Blöcke,
Text-Encoding) siehe den Skill `.claude/skills/iso-designer-jop/SKILL.md` —
hier geht es nur um das konkrete Scroll-Konzept selbst.

## Ziel

Eine Liste mit mehr Einträgen, als auf eine Maske passen, soll auf dem VT
scrollbar dargestellt werden — pro Eintrag eine Zeile mit Label, Name,
Zahlenwert, Einheit und einem Status-Icon.

## Architektur

Auf `MainMask.jvi` liegen **zwei parallele Parent-Container** nebeneinander,
beide mit fester Höhe 288 px (= Höhe des sichtbaren Listenbereichs) und
`ClipsChildren=1`. Der eine trägt die eigentliche Zeilenliste, der andere
nur den schmalen Scrollbalken daneben:

```
MainMask.jvi (480×480)
├─ Containerr_Scrolling_Parent (JVS-ID 3006, CGroup, 480×288, ClipsChildren=1)  ← "Sichtfenster" Liste
│  └─ Container_Scrolling_Content (JVS-ID 3031, CGroup, 432×850)               ← eigentliche Liste
│     ├─ Container_Row_01 (Top=0)     ← Zeile 1
│     ├─ Container_Row_02 (Top=42)    ← Zeile 2
│     ├─ Container_Row_03 (Top=84)    ← Zeile 3
│     ├─ …
│     └─ Container_Row_20 (Top=798)   ← Zeile 20
│
└─ Container_Scrollbar_Parent (JVS-ID 3000, CGroup, 12×288, ClipsChildren=1)    ← schmaler Scrollbalken (Sichtfenster)
   ├─ Rectangle_Scrollbar (14000, 12×288, Top=0 fix)                           ← Balken-Hintergrund/Track, volle Höhe
   └─ Container_Scrollbar_Content (JVS-ID 3010, CGroup, 12×288, Top=−252)      ← bewegter Inhalt (analog Scrolling_Content)
      └─ Rectangle_Scroll_Indicator (14001, 12×36, Top=252 fix innerhalb)      ← "Thumb", Nettoposition = −252+252 = 0
```

- **`Containerr_Scrolling_Parent`** ist das sichtbare Fenster für die Liste:
  fix 288 px hoch. Bei 288 px / 42 px Zeilenhöhe sind gleichzeitig
  **~6–7 Zeilen** sichtbar. (Tippfehler im Namen — siehe Offene Punkte.)
- **`Container_Scrolling_Content`** ist die eigentliche Liste, 850 px hoch
  (20 × 42 px + Rand) — deutlich größer als das Sichtfenster.
- **`Container_Scrollbar_Parent`** ist das Sichtfenster für den Scrollbalken
  neben der Liste, exakt so hoch wie das Listen-Sichtfenster (288 px). Er
  enthält `Rectangle_Scrollbar` als unbeweglichen Track über die volle Höhe,
  sowie — seit der jüngsten GUI-Überarbeitung — einen eigenen bewegten
  Inhalts-Container `Container_Scrollbar_Content` (12×288, genau wie sein
  Parent), der wiederum `Rectangle_Scroll_Indicator` (36 px hoch, eine
  Zeilenhöhe) an einer festen internen Position (Top=252) enthält. Diese
  zusätzliche Verschachtelung spiegelt bewusst das Muster von
  `Containerr_Scrolling_Parent`/`Container_Scrolling_Content` — vermutlich
  damit dieselbe Art von Objekt (ein `Container`) sowohl für die Liste als
  auch für den Indikator per `Q_ChildPosition` bewegt werden kann, statt für
  den Indikator eine Ausnahme (direktes Bewegen eines `Rectangle`) zu
  brauchen. Da `Container_Scrollbar_Content` genauso hoch wie sein Parent
  ist, verschiebt sein `Top` effektiv nur die Position des Indikators
  innerhalb des Balkens — es gibt (anders als bei der Liste) keinen
  zusätzlichen, sonst verdeckten Inhalt, der dadurch sichtbar würde.
- **Scrollen** heißt: die `Top`-Eigenschaft von `Container_Scrolling_Content`
  innerhalb des Sichtfensters negativ verschieben (z. B. −42, −84, …), damit
  andere Zeilen in den sichtbaren Bereich rutschen — **und gleichzeitig**
  die `Top`-Eigenschaft von `Container_Scrollbar_Content` innerhalb seines
  Sichtfensters passend mitverschieben, damit der Scrollbalken die Position
  widerspiegelt. Jede Zeile selbst bleibt dabei unverändert an ihrer festen
  Position (`Top = 42 × (Zeilennummer−1)`) innerhalb der Content-Liste; das
  Rechteck `Rectangle_Scroll_Indicator` bleibt ebenso unverändert an seiner
  festen Position (Top=252) innerhalb von `Container_Scrollbar_Content`.
- **Konvention: X-Koordinate immer 0.** `Container_Scrolling_Content` und
  `Container_Scrollbar_Content` — die beiden per `Q_ChildPosition` bewegten
  Inhalts-Container — werden **nur in Y** verschoben (kein horizontales
  Scrollen vorgesehen); ihre X-Koordinate (`Left`) muss deshalb **immer 0**
  sein. Das war zunächst nicht der Fall (`Container_Scrolling_Content` hatte
  einen von 0 abweichenden X-Wert — ein Fehler), wurde aber direkt im
  ISO-Designer korrigiert und gilt ab jetzt als feste Regel für jeden
  Scroll-Content-Container. Praktischer Nebeneffekt: X=0 ist ein zusätzliches,
  robustes Merkmal, an dem sich ein Scroll-Content-Container erkennen lässt
  (ergänzend zur Namenskonvention `*_Scrolling_Content`/`*_Scrollbar_Content`,
  siehe `GcfScript.py`-Erkennung weiter unten) — ein Container mit
  abweichendem X ist entweder kein Scroll-Content-Container oder falsch
  konfiguriert.
- **Bedienung über 4 Softkeys**: `UP`, `UP_UP`, `DOWN`, `DOWN_DOWN` — je ein
  Softkey für "eine Zeile" und "mehrere Zeilen auf einmal" pro Richtung
  (analog "kurz drücken = 1 Schritt, lang/UP_UP drücken = großer Schritt").
  Aktuell existieren dafür 6 `CPointer`-Objekte auf `MainSoftKeyMask.jvi`
  (JVS-ID 27024–27029, davon einer schon als
  `ObjectPointer_SoftKey_Back` benannt) — die Zuordnung der übrigen auf
  UP/UP_UP/DOWN/DOWN_DOWN ist noch nicht als `ObjectName` im Pool
  eingetragen, siehe BEISPIEL unten.

> ⚠️ **Offen / noch nicht verdrahtet:** `EnableScrolling` ist auf allen
> Masken `0` — das native VT-Scrollen wird also nicht genutzt. Die
> eigentliche Logik, die bei Softkey-Tastendruck den `Top`-Wert von 3031
> (und passend dazu den `Top`-Wert von `Container_Scrollbar_Content`)
> verändert, ist noch nicht umgesetzt — siehe BEISPIEL/Verallgemeinerung
> für einen konkreten Vorschlag, wie das auf FORTE-Seite aussehen könnte.

## Zeilen-Aufbau (eine Zeile im Detail)

Jede Zeile ist ein `CGroup`-Container (432×36) mit zwei Arten von Kindern,
über `CProxy`-Wrapper eingehängt:

**Geteilt (nicht dupliziert — dieselben realen Objekte in jeder Zeile):**
- 4× Hintergrund-/Rahmen-`Rectangle` (Objekte 14003, 14004, 14005, 14013)
- 1× Status-`PictureGraphic` (Objekt 20001) — als Standard-Ziel des
  Object-Pointers, siehe unten

**Individuell (pro Zeile ein eigenes reales Objekt):**
- 1× `OutputString` — Label (z. B. „Label_03")
- 1× `OutputString` — Name/Freitext (Platzhalter „langer Name was weiß ich")
- 1× `OutputString` — Einheit („kg")
- 1× `OutputNumber` — Zahlenwert
- 1× `ObjectPointer` — zeigt per Default auf das geteilte Status-Icon
  (20001), kann aber pro Zeile individuell umgehängt werden (z. B. auf ein
  anderes Icon für „Fehler"/„OK"/„leer")
- 1× verschachtelter Sub-`Container` (180×18) mit eigenem
  `OutputNumber` + `OutputString` (an eine eigene `StringVariable`
  gebunden) — Zweck/Datenquelle dieses Subfelds ist noch nicht geklärt,
  wurde nur strukturell mitkopiert, weil jede bestehende Zeile ihn hatte

## BEISPIEL

Zwei konkrete Beispiele, aus denen unten die allgemeinen Regeln abgeleitet
werden: (A) der Inhalt einer einzelnen Zeile, (B) die Scroll-Steuerung
selbst (Balken + Softkeys + mögliche FORTE-Logik).

### Beispiel A: Zeileninhalt

Um das Zeilen-Muster greifbar zu machen, an dieser Stelle **eine konkrete
Zeile** durchgespielt — Zeile 3, wie sie tatsächlich im Pool steht. Der
Kontext (Krauternter) legt nahe, dass hier später mal eine Kraut-Charge
angezeigt wird; die Werte unten sind aktuell noch Platzhalter, keine echte
Datenbindung.

**Angenommen, Zeile 3 soll zeigen:** Position 3, Kraut „Petersilie",
Erntegewicht 12,47 kg, Status OK.

| Feld | Objekt (Klasse, JVS-ID) | ObjectName | Inhalt aktuell | Wäre inhaltlich |
|---|---|---|---|---|
| Label | `COutputText` 11031 | `OutputString_Row_03_Label` | „Label_03" | Positions-Nr. „3" |
| Name | `COutputText` 11049 | `OutputString_Row_03_Name` | „langer Name was weiß ich" (Platzhalter) | „Petersilie" |
| Wert | `COutputNumber` 12009 | `OutputNumber_Row_03_Value` | Platzhalterzahl | 12.47 (kg) |
| Einheit | `COutputText` 11067 | `OutputString_Row_03_Unit` | „kg" | „kg" (bleibt gleich) |
| Status-Icon | `CPointer` 27006 | `ObjectPointer_Row_03_Status` | zeigt auf geteiltes Icon 20001 | zeigt auf „OK"-Icon |
| Container (Zeile) | `CGroup` 3032 | `Container_Row_03` | Top=84 in der Liste | unverändert |
| Sub-Container | `CGroup` 3050 | `Container_Row_03_Sub` | leeres Textfeld, `StringVariable` 22009 | ungeklärt, s. o. |

Damit diese Zeile wirklich „Petersilie / 12.47 kg / OK" anzeigt, fehlen noch
zwei Dinge, die **nicht** Teil dieses ISO-Designer-Konzepts sind, sondern in
der Steuerungslogik (SPS-Seite / FORTE) passieren müssen:
1. `OutputNumber_Row_03_Value` (12009) an eine echte Prozessvariable binden
   (aktuell nur ein statischer Platzhalterwert in der `.jop`).
2. `ObjectPointer_Row_03_Status` (27006) je nach Zustand zur Laufzeit auf
   unterschiedliche `PictureGraphic`-Objekte umschalten (aktuell fest auf
   das geteilte Icon 20001 verdrahtet).
`OutputString_Row_03_Name` (11049) und `OutputString_Row_03_Label` (11031)
sind reine Text-Properties in der `.jop` — die kann man direkt umschreiben
(Base64/UTF-16LE, siehe Skill), ohne Laufzeitbindung, falls die Namen fix
sind und sich nicht pro Ernte ändern.

### Beispiel B: Scroll-Steuerung (Balken + Softkeys)

Die Anzeige-Seite (Rectangles, Softkey-Pointer) steht schon im Pool, die
Steuerungslogik dafür noch nicht. Konkret vorgeschlagen:

| Bauteil | Objekt | Rolle |
|---|---|---|
| `Container_Scrollbar_Parent` | `CGroup` 3000 | Sichtfenster für den Scrollbalken, 12×288, fix (Top=0 auf der Maske) |
| `Rectangle_Scrollbar` | `CRectangle` 14000 | Balken-Hintergrund, 12×288, unbeweglich |
| `Container_Scrollbar_Content` | `CGroup` 3010 | bewegter Inhalt, 12×288 — `Top` soll sich mit der Scrollposition mitbewegen (Startwert −252) |
| `Rectangle_Scroll_Indicator` | `CRectangle` 14001 | "Thumb", 12×36 — feste Position Top=252 *innerhalb* von `Container_Scrollbar_Content` |
| Softkey `UP` | `CPointer` (einer von 27025–27029, noch nicht benannt) | 1 Zeile nach oben |
| Softkey `UP_UP` | `CPointer` (dto.) | mehrere Zeilen auf einmal nach oben (schnell) |
| Softkey `DOWN` | `CPointer` (dto.) | 1 Zeile nach unten |
| Softkey `DOWN_DOWN` | `CPointer` (dto.) | mehrere Zeilen auf einmal nach unten (schnell) |

**Vorbild für die FORTE-Logik dahinter:**
[`RampLimitFS.fbt`](C:\4diac\4diac-ide_3.2.0-win32.win32.x86_64_nightly_2026-04-17_2003_sp7\4diac-ide\typelibrary\signalprocessing-3.0.0\typelib\RampLimitFS.fbt)
aus der 4diac-Typelibrary `signalprocessing`. Dieser FB macht eigentlich
eine Sollwerteingabe (Tempomat-Prinzip: kurz drücken = ±1, lang drücken =
±10), passt aber strukturell fast 1:1 auf das Scroll-Problem — **nicht als
fertige Lösung**, sondern als Bauplan, nach dem ein eigener `ScrollFS`-FB
gebaut werden könnte:

| `RampLimitFS` | Bedeutung dort | Übertragen auf Scroll |
|---|---|---|
| Event `ZERO` | Sollwert := VAL_ZERO | Event `TOP` |
| Event `UP_SLOW` / `UP_FAST` | Sollwert +1 / +SLOW\|FAST | Event `UP` / `UP_UP` |
| Event `DOWN_SLOW` / `DOWN_FAST` | Sollwert −1 / −SLOW\|FAST | Event `DOWN` / `DOWN_DOWN` |
| Event `FULL` | Sollwert := VAL_FULL | Event `BOTTOM` |
| Event `LOAD` (mit Input `PV`) | Sollwert := PV | Event `POS` (mit Input `SET_POS`) |
| Input `SLOW`, `FAST` | Schrittweite langsam/schnell | Schrittweite 1 Zeile / `STEP` Zeilen |
| Input `VAL_ZERO`, `VAL_FULL` | Wertebereich-Grenzen | Scroll-Anschlag oben (0) / unten (`POS_MAX` = `floor((ContentHöhe − FensterHöhe) / Zeilenhöhe)` = `floor((850−288)/42)` = 13) |
| Output `OUT` (via `CNF`) | aktueller Sollwert | aktuelle Scroll-Position `OUT` (in Zeilen, 0…`POS_MAX`) |

**`ScrollFS` hat also — mit den 7 vorgeschlagenen Events — exakt dieselbe
Zahl und Struktur von Event-Eingängen wie `RampLimitFS`**, 1:1 übersetzt:

| Event | Wirkung auf `OUT` | Schönerer Name (Vorschlag) |
|---|---|---|
| `TOP` | `OUT := 0` — Listenanfang | `FIRST` |
| `UP_UP` | `OUT -= STEP` (geklemmt bei 0) | `PAGE_UP` |
| `UP` | `OUT -= 1` (geklemmt bei 0) | `LINE_UP` |
| `DOWN` | `OUT += 1` (geklemmt bei `POS_MAX`) | `LINE_DOWN` |
| `DOWN_DOWN` | `OUT += STEP` (geklemmt bei `POS_MAX`) | `PAGE_DOWN` |
| `BOTTOM` | `OUT := POS_MAX` — Listenende | `LAST` |
| `POS` (mit Input `SET_POS`) | `OUT := SET_POS`, geklemmt auf `0…POS_MAX` | `GOTO` |

Zusätzliche Inputs (analog `SLOW`/`FAST`/`VAL_ZERO`/`VAL_FULL`/`PV` bei
`RampLimitFS`): `STEP` (Schrittweite für `UP_UP`/`DOWN_DOWN` — vom Skript
automatisch abgeleitet als `floor(Fensterhöhe / Zeilenhöhe)` = `floor(288/42)`
= **6** vollständig sichtbare Zeilen, also "eine Bildschirmseite"), `POS_MAX`
(hier 13), `SET_POS` (Zielwert für `POS`/`GOTO`). Output: `OUT` (aktuelle
Position, 0…13), ausgegeben über `CNF` wie bei `RampLimitFS`.

**Konkret in unserem Fall (20 Zeilen, 42 px Zeilenhöhe):** ein einzelnes
`UP`- oder `DOWN`-Event ändert `OUT` um genau 1, und da
`Container_Scrolling_Content.Top = -42 × OUT` ist, bedeutet das: **ein
`UP`/`DOWN`-Tastendruck scrollt die Liste um exakt 42 Pixel — eine ganze
Zeile.** Das ist kein Zufall, sondern folgt direkt daraus, dass `OUT` in
Zeilen-Einheiten geführt wird und erst beim Schreiben auf den VT (über
`Q_ChildPosition`, siehe unten) mit der Zeilenhöhe skaliert wird — dieselbe
`OUT`-Zahl treibt gleichzeitig beide VT-Ziele (Liste *und* Scroll-Indikator)
mit jeweils eigener Skalierung, ohne dass `ScrollFS` selbst irgendetwas von
Pixeln wissen muss.

Diese `OUT`-Zahl (0…13) müsste dann auf zwei VT-Werte umgerechnet und
geschrieben werden: `Container_Scrolling_Content.Top = -42 × OUT` und
`Container_Scrollbar_Content.Top = -252 + OUT × (288-36)/13`. Die zweite
Formel ergibt sich aus der neuen Verschachtelung (siehe Architektur):
`Rectangle_Scroll_Indicator` sitzt fest bei Top=252 *innerhalb* von
`Container_Scrollbar_Content` — bei `OUT=0` muss `Container_Scrollbar_Content.Top`
also bei −252 stehen, damit der Indikator netto auf Y=0 landet (Balken-Anfang);
bei `OUT=13` (Anschlag unten) ergibt sich `Top = -252 + 252 = 0`, der
Indikator landet netto auf Y=252 (Balken-Ende minus Indikatorhöhe, korrekt).

**Wie `OUT` tatsächlich beim VT ankommt:** über den ISOBUS-Baustein
[`Q_ChildPosition`](C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\Q_ChildPosition.fbt)
(ISO 11783-6 Annex F.16, „Change Child Position") — setzt die **absolute**
Position eines Kind-Objekts relativ zu einem Parent-Objekt. Zwei Instanzen
nötig, eine pro bewegtem Objekt — bei beiden ist das bewegte Kind jetzt ein
`Container`, nicht mehr direkt ein `Rectangle`:

| `Q_ChildPosition`-Instanz | `u16ObjIdParent` | `u16ObjId` (Kind, wird bewegt) | `s16Xposition`/`s16Yposition` |
|---|---|---|---|
| Liste scrollen | `Containerr_Scrolling_Parent` (3006) | `Container_Scrolling_Content` (3031) | `0` / `-42 × OUT` |
| Scroll-Indikator | `Container_Scrollbar_Parent` (3000) | `Container_Scrollbar_Content` (3010) | `0` / `-252 + OUT × (288-36)/13` |

Wichtig — und das war ein Fehler in unserer ersten Beschreibung dieser
Bausteine: `u16ObjId` (Kind) und `u16ObjIdParent` (Parent) haben **getrennte
Gültigkeitsregeln**, keine gemeinsame. ISO 11783-6 Annex F.16 listet nur,
welche Objekttypen als **Kind** bewegt werden dürfen (u. a. Container,
Rectangle — beides bei uns der Fall). Welche Objekttypen als **Parent**
zulässig sind, steht separat in Annex B, jeweils unter „Allowed commands"
des Objekttyps: **Container ist dort explizit erlaubt (Annex B.4)** — SoftKeyMask
dagegen **nicht**. `Containerr_Scrolling_Parent` und `Container_Scrollbar_Parent`
sind beide vom Typ Container, also als Parent für beide `Q_ChildPosition`-Aufrufe
zulässig. Die reale C++-Implementierung
(`C:\git\hr\LOGIBUS_integration_datapanel\Application\components\VTClientHelper\VTClientHelper.cpp`,
Funktionen `iso_is_child_location_id`/`iso_is_parent_valid_id`) prüft beide
Seiten bereits korrekt getrennt und wurde nicht verändert — nur die
Dokumentation der beiden `.fbt`-Bausteine und der zugehörigen
`visual-programming-languages-docs`-Seiten war unpräzise und wurde
korrigiert.

### Beispiel B (Fortsetzung): Struct-basierter Wrapper `ScrollFS_PHYS`

Statt `ScrollFS` mit lauter einzelnen Skalar-Eingängen (zwei Parent-IDs,
zwei Kind-IDs, Zeilenhöhe, Anschläge, …) zu bauen, folgt der Baustein dem
Muster von
[`Q_NumericValue_PHYS.fbt`](C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\Q_NumericValue_PHYS.fbt):
eine Composite-FB (FBNetwork), die alle Objektpool-Eigenschaften einer
konkreten Scroll-Liste in **einer Struct** bündelt und intern verdrahtet.
Bei `Q_NumericValue_PHYS` heißt diese Struct `NumericObjectPool_S`
(`u16ObjId`, `r32Scale`, `i32Offset`, `u8Decimals`) und wird von
`GcfScript.py` (`Ventilsteuerung\scripts_central\GcfScript.py`,
Funktion `writeNumericGCFfile`) automatisch aus der `.jop` erzeugt — pro
`OutputNumber`/`InputNumber` eine `.gcf`-Konstante wie
`(u16ObjId := 12009, r32Scale := 0.01, i32Offset := 0, u8Decimals := 2)`.

**Analog für Scroll-Listen — neue Struct `ScrollObjectPool_S`:**

```
ScrollObjectPool_S:
  u16ListParentId   : UINT  -- Containerr_Scrolling_Parent
  u16ListContentId  : UINT  -- Container_Scrolling_Content
  i32RowHeight      : DINT  -- Zeilenhöhe in px
  u16BarParentId    : UINT  -- Container_Scrollbar_Parent
  u16BarContentId   : UINT  -- Container_Scrollbar_Content
  i32BarBaseOffset  : DINT  -- Bar-Content.Top bei OUT=0
  i32BarTravel      : DINT  -- Fensterhöhe − Indikatorhöhe
  i32PosMax         : DINT  -- Zeilenanzahl − sichtbare Zeilen
  i32Step           : DINT  -- Schrittweite für UP_UP/DOWN_DOWN
```

Für unsere konkrete Liste (20 Zeilen, 6 vollständig sichtbar, 42 px
Zeilenhöhe, Bar 288/36 px) — tatsächlich von `GcfScript.py` gegen die echte
`.jop` erzeugte Konstante (siehe unten):

```
(u16ListParentId := 3006, u16ListContentId := 3031, i32RowHeight := 42,
 u16BarParentId := 3000, u16BarContentId := 3010, i32BarBaseOffset := -252,
 i32BarTravel := 252, i32PosMax := 13, i32Step := 6)
```

**Interner Aufbau von `ScrollFS_PHYS` (FBNetwork, umgesetzt):**

- `stObj` wird bei `INIT` einmalig über einen `F_MOVE`-Baustein („Snap",
  `DataType`-Attribut auf `ScrollObjectPool_S` gebunden) geschnappt — danach
  bleiben alle neun Felder als `Snap.OUT.<Feldname>` dauerhaft verfügbar.
  Das ist keine Kür, sondern nötig: `F_MOVE.IN`/`.OUT` sind generisch `ANY`
  typisiert, und eine `ANY`-Verbindung (hier: der konkret typisierte `stObj`
  auf den generischen `Snap.IN`) läuft in 4diac grundsätzlich nur über genau
  so einen `MOVE`-Baustein, nie direkt. Alle *anderen* Verbindungen im
  Netzwerk sind beidseitig bereits konkret typisiert (`DINT`→`DINT`,
  `UINT`→`UINT`) oder laufen über die zahlenspezifische Baustein-Familie
  `ANY_NUM` (Multiplikation/Division/Addition), die 4diac ohne `MOVE`
  generisch auflöst — nur der Struct-Durchgriff brauchte die Sonderbehandlung.
- **`RampLimitFS` wird direkt als interner Sub-FB wiederverwendet** (kein
  neuer Zustandsautomat nötig) — Events 1:1 gemappt (`TOP→ZERO`,
  `UP→UP_SLOW`, `UP_UP→UP_FAST`, `DOWN→DOWN_SLOW`, `DOWN_DOWN→DOWN_FAST`,
  `BOTTOM→FULL`, `POS→LOAD` mit `PV:=SET_POS`), `VAL_ZERO:=0`,
  `VAL_FULL:=Snap.OUT.i32PosMax`, `SLOW:=1`, `FAST:=Snap.OUT.i32Step`.
- Bei jedem `RampLimitFS.CNF` (liefert `OUT`) werden **parallel** zwei
  Rechenketten angestoßen, die je in einer `Q_ChildPosition`-Instanz enden:
  - Liste: `F_MUL(OUT, Snap.OUT.i32RowHeight)` → `F_SUB(0, …)` (Vorzeichen
    drehen) → `F_DINT_TO_INT` (Q_ChildPosition erwartet `INT`, nicht
    `DINT`) → `MoveList.REQ` mit `s16Yposition`. Parent-/Kind-ID
    (`u16ObjIdParent`/`u16ObjId`) kommen als Dauerverbindung von
    `Snap.OUT.u16ListParentId`/`u16ListContentId`.
  - Balken: `F_MUL(OUT, Snap.OUT.i32BarTravel)` → `F_DIV(…, Snap.OUT.i32PosMax)`
    → `F_ADD(Snap.OUT.i32BarBaseOffset, …)` → `F_DINT_TO_INT` →
    `MoveBar.REQ` mit `s16Yposition`.
- `INIT` (extern, mit `stObj`) löst `Snap.REQ` aus; `Snap.CNF` initialisiert
  `MoveList` (Parent-/Kind-ID aus der Struct), danach `MoveList.INITO` →
  `MoveBar.INIT`, danach `MoveBar.INITO` → externes `INITO` — serielle
  Kette, kein zusätzlicher „Join"-Baustein nötig.
- Datei: `Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\ScrollFS_PHYS.fbt`,
  Package `isobus::UT::Q`. XSD-validiert (`iec61499-creator`-Skill,
  `fbtype.xsd`).

**Umgesetzte Erweiterung von `GcfScript.py`:** `readScrollJOP()` erkennt
eine Scroll-Liste an den Namenskonventionen `*_Scrolling_Parent`/
`*_Scrolling_Content`/`*_Scrollbar_Parent`/`*_Scrollbar_Content` (nur
eine Liste pro Pool unterstützt — bei mehreren Treffern pro Suffix wird die
Generierung mit einer Warnung übersprungen, da eine präfixbasierte Zuordnung
angesichts inkonsistenter Namen wie `Containerr_Scrolling_Parent` vs.
`Container_Scrolling_Content` nicht robust wäre). `RowHeight` wird als
Top-Abstand zwischen `*_Row_01` und `*_Row_02` berechnet (nicht als eigene
`Height`-Property der Zeile — die ist mit 36 px kleiner als der tatsächliche
Zeilenabstand von 42 px, da zwischen den Zeilen eine sichtbare Lücke
liegt). `PosMax = floor((ContentHeight − ParentHeight) / RowHeight)`,
`Step = floor(ParentHeight / RowHeight)`, `BarBaseOffset` wird als aktuell
im Pool gesetzter `Top`-Wert der Bar-Content-Proxy übernommen (nicht neu
berechnet), `BarTravel = BarParentHeight − Indikatorhöhe` (Indikatorhöhe
über den Bar-Content-Kind-Proxy aufgelöst). `writeScrollGCFfile()` schreibt
eine `<Name>_Scroll.gcf` mit `ScrollObjectPool_S`-Konstanten, Namensschema
`<abgeleiteter Name>_Scroll` (Suffix analog `_N` bei den Numeric-Konstanten).
Gegen die echte `Workspace_Scroll/DefaultPool.jop` getestet, Ergebnis siehe
Konstante oben. Prüft aktuell nur die Namenskonvention, nicht die X=0-Regel
(siehe Architektur oben) — als zusätzliche Plausibilitätsprüfung (Warnung bei
X≠0 statt hartem Fehler) noch nicht umgesetzt, aber ein naheliegender
nächster Schritt, sobald mehr als eine Scroll-Liste pro Pool unterstützt
werden soll und die Namenskonvention allein nicht mehr robust genug ist.

**Status:** Implementiert (alle drei Teile: `.dtp`, `GcfScript.py`,
`.fbt`), noch nicht in der eigentlichen Steuerungsanwendung verdrahtet
(kein FB-Netzwerk-Beispiel mit den 4 Softkeys, das ist der nächste Schritt).

## Verallgemeinerung

Aus dem Beispiel oben lässt sich das Muster für **jede** Zeile i
(1-basiert) ableiten:

- `Top` der Zeile in der Liste = `42 × (i − 1)`
- Label-Text = `f"Label_{i:02d}"` (oder fachlich sinnvoller Text)
- Alle "geteilten" Objekte (Rectangles 14003/14004/14005/14013, Icon 20001)
  werden **nie** dupliziert — jede neue Zeile bekommt nur einen frischen
  `CProxy`, der auf dieselbe reale ID zeigt.
- Alle "individuellen" Objekte (2× OutputString + 1× OutputString + 1×
  OutputNumber + 1× ObjectPointer + 1× Sub-Container mit eigenem
  OutputNumber/OutputString/StringVariable) bekommen pro Zeile **frische,
  fortlaufende reale IDs**, jeweils oberhalb des aktuellen Maximums der
  jeweiligen Klasse.
- Pro Zeile fallen **15 neue `CProxy`-Wrapper** an: 10 für die Kinder des
  äußeren Zeilen-Containers, 3 für die Kinder des Sub-Containers, 1 für den
  Sub-Container selbst (als Kind des äußeren Containers) und 1 dafür, den
  Zeilen-Container in `Container_Scrolling_Content` einzuhängen.

Diese Regeln stecken bereits vollständig im Generierungs-Skript, mit dem
Zeile 3–20 erzeugt wurden (siehe Commit-Historie ab
„Add 18 scroll rows (3-20) to Scrolling Content container"). Für weitere
Zeilen reicht es, dasselbe Muster mit dem jeweils aktuellen ID-Maximum
fortzusetzen.

Für die Scroll-Steuerung (Beispiel B) verallgemeinert sich das Muster so:

- Scroll-Position wird als **eine ganze Zahl `pos`** geführt, Bereich
  `0 … floor((ContentHöhe − FensterHöhe) / Zeilenhöhe)` = `0…13` in unserem
  Fall. Bei anderer Zeilenanzahl/-höhe oder Fenstergröße ändert sich nur
  diese Obergrenze und die Umrechnungsfaktoren unten — die Struktur bleibt
  gleich; `GcfScript.py` berechnet das automatisch aus der `.jop`.
- `Container_Scrolling_Content.Top = -H × pos` (H = Zeilenhöhe, hier 42).
- `Container_Scrollbar_Content.Top = -Offset + pos × (Fensterhöhe − Indikatorhöhe) / pos_max`
  (hier: `-252 + pos × (288−36)/13`). `Offset` (hier 252) ist die feste
  interne `Top`-Position von `Rectangle_Scroll_Indicator` innerhalb von
  `Container_Scrollbar_Content` und muss vom Vorzeichen her immer genau
  gegenläufig zum Startwert von `Container_Scrollbar_Content.Top` gewählt
  sein, damit der Indikator bei `pos=0` netto auf Y=0 steht.
- Die 4 Softkeys ändern `pos` um ±1 (`UP`/`DOWN`) bzw. ±N (`UP_UP`/
  `DOWN_DOWN`, z. B. N=3 für "eine Bildschirmseite"), jeweils geklemmt auf
  `0…pos_max` — exakt das `ZERO`/`UP_SLOW`/`UP_FAST`/`DOWN_SLOW`/
  `DOWN_FAST`/`FULL`-Muster von `RampLimitFS`, nur mit `SLOW=1` und
  `FAST=N` sowie `VAL_ZERO=0`, `VAL_FULL=pos_max`.

## Aktueller ID-Stand (Stand: nach GUI-Re-Save)

| Klasse | Anzahl | höchste ID |
|---|---|---|
| `CGroup` (Container) | 52 | 3067 |
| `COutputText` (OutputString) | 83 | 11102 |
| `COutputNumber` | 41 | 12044 |
| `CPointer` (ObjectPointer) | 30 | 27029 |
| `CStringVariable` | 21 | 22026 |
| `CProxy` | 443 | 4194859 |
| `CRectangle` | 13 | 14107 |
| `CImage` (PictureGraphic) | 13 | 20329 |

## Offene Punkte

- **Scroll-Logik nicht verdrahtet**: die 6 SoftKey-Pointer auf
  `MainSoftKeyMask.jvi` (27024–27029) haben noch keine Makro-/
  Programmlogik, die beim Drücken `Container_Scrolling_Content.Top` und
  `Container_Scrollbar_Content.Top` ändert. Kandidat für das Muster:
  ein `ScrollFS`-FB nach Vorbild von `RampLimitFS.fbt`, dessen `OUT` über
  zwei `Q_ChildPosition`-Instanzen (ISO 11783-6 F.16) an den VT geschrieben
  wird — siehe Beispiel B. Noch nicht als FB-Netzwerk umgesetzt, nur als
  Konzept dokumentiert.
- **Softkey-ObjectNames noch generisch**: nur 27024 heißt bereits
  `ObjectPointer_SoftKey_Back`; welche der übrigen fünf (27025–27029) zu
  `UP`/`UP_UP`/`DOWN`/`DOWN_DOWN` werden sollen, ist mündlich festgelegt
  (siehe Beispiel B), aber noch nicht als `ObjectName` im Pool benannt.
- **Zeile 2 heißt strukturell noch `Container_Row_02`, ObjectName der
  Objekte ist aber älteren Datums** (z. B. `OutputString_11003` statt dem
  neueren `OutputString_Row_02_Label`-Schema) — Zeile 1 und 2 stammen aus
  der ursprünglichen, von Hand/GUI gebauten Vorlage, Zeile 3–20 aus dem
  generierten Nachfolge-Schema. Funktional kein Unterschied, nur kosmetisch
  inkonsistent.
- **Sub-Container-Zweck ungeklärt**: warum jede Zeile einen eigenen
  Sub-Container mit leerem, an eine `StringVariable` gebundenem Textfeld
  hat, ist strukturell übernommen, aber inhaltlich nicht verstanden.
- **3 der 7 zuletzt hinzugekommenen Icon-Bitmaps** (`Image_20070.bmp`,
  `Image_55040.bmp`, `Image_55041.bmp`) sind aktuell in keinem Objekt
  referenziert — vermutlich Nebenprodukt der Icon-Auswahl im Designer.
- **Reihentitel „Containerr_Scrolling_Parent“** (JVS-ID 3006) hat einen
  Tippfehler (doppeltes „r“) aus der ursprünglichen GUI-Benennung — bewusst
  nicht angefasst, da nicht Teil des aktuellen Auftrags.
