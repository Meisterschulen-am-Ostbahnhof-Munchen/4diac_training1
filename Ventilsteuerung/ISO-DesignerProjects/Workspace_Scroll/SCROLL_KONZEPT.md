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
└─ Container_Scrollbar_Parent (JVS-ID 3000, CGroup, 12×288, ClipsChildren=1)    ← schmaler Scrollbalken
   ├─ Rectangle_Scrollbar (14000, 12×288)         ← Balken-Hintergrund/Track, füllt die volle Höhe
   └─ Rectangle_Scroll_Indicator (14001, 12×36)   ← "Thumb"/Positionsanzeige, aktuell Top=0
```

- **`Containerr_Scrolling_Parent`** ist das sichtbare Fenster für die Liste:
  fix 288 px hoch. Bei 288 px / 42 px Zeilenhöhe sind gleichzeitig
  **~6–7 Zeilen** sichtbar. (Tippfehler im Namen — siehe Offene Punkte.)
- **`Container_Scrolling_Content`** ist die eigentliche Liste, 850 px hoch
  (20 × 42 px + Rand) — deutlich größer als das Sichtfenster.
- **`Container_Scrollbar_Parent`** ist der optische Scrollbalken neben der
  Liste, exakt so hoch wie das Sichtfenster (288 px). Er enthält zwei
  Rectangles: `Rectangle_Scrollbar` als Track über die volle Höhe, und
  `Rectangle_Scroll_Indicator` (36 px hoch, also eine Zeilenhöhe) als
  bewegliche Positionsanzeige — dessen `Top` soll proportional zur
  Scrollposition der Liste mitwandern.
- **Scrollen** heißt: die `Top`-Eigenschaft von `Container_Scrolling_Content`
  innerhalb des Sichtfensters negativ verschieben (z. B. −42, −84, …), damit
  andere Zeilen in den sichtbaren Bereich rutschen — **und gleichzeitig**
  `Rectangle_Scroll_Indicator.Top` proportional mitverschieben, damit der
  Scrollbalken die Position widerspiegelt. Jede Zeile selbst bleibt dabei
  unverändert an ihrer festen Position (`Top = 42 × (Zeilennummer−1)`)
  innerhalb der Content-Liste.
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
> (und passend dazu den `Top`-Wert von `Rectangle_Scroll_Indicator`)
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
| `Container_Scrollbar_Parent` | `CGroup` 3000 | Sichtfenster für den Scrollbalken, 12×288, fix |
| `Rectangle_Scrollbar` | `CRectangle` 14000 | Balken-Hintergrund, 12×288, unbeweglich |
| `Rectangle_Scroll_Indicator` | `CRectangle` 14001 | "Thumb", 12×36 — `Top` soll sich mit der Scrollposition mitbewegen |
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
| Event `UP_SLOW` / `UP_FAST` | Sollwert +1 / +SLOW\|FAST | Softkey `UP` / `UP_UP` |
| Event `DOWN_SLOW` / `DOWN_FAST` | Sollwert −1 / −SLOW\|FAST | Softkey `DOWN` / `DOWN_DOWN` |
| Input `SLOW`, `FAST` | Schrittweite langsam/schnell | Schrittweite 1 Zeile / N Zeilen |
| Input `VAL_ZERO`, `VAL_FULL` | Wertebereich-Grenzen | Scroll-Anschlag oben (0) / unten (Zeilenanzahl − sichtbare Zeilen = 20 − 7 = 13) |
| Output `OUT` (via `CNF`) | aktueller Sollwert | aktuelle Scroll-Position (in Zeilen) |

Ein `ScrollFS`-FB nach diesem Muster hätte als `OUT` die aktuelle
Zeilen-Offset-Zahl; diese müsste dann auf zwei VT-Werte umgerechnet und
geschrieben werden: `Container_Scrolling_Content.Top = -42 × OUT` und
`Rectangle_Scroll_Indicator.Top = OUT × (288-36)/13` (linear zwischen 0 und
`288-36`, je nachdem wie weit `OUT` zwischen 0 und 13 steht).

**Wie `OUT` tatsächlich beim VT ankommt:** über den ISOBUS-Baustein
[`Q_ChildPosition`](C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\Q_ChildPosition.fbt)
(ISO 11783-6 Annex F.16, „Change Child Position") — setzt die **absolute**
Position eines Kind-Objekts relativ zu einem Parent-Objekt. Zwei Instanzen
nötig, eine pro bewegtem Objekt:

| `Q_ChildPosition`-Instanz | `u16ObjIdParent` | `u16ObjId` (Kind, wird bewegt) | `s16Xposition`/`s16Yposition` |
|---|---|---|---|
| Liste scrollen | `Containerr_Scrolling_Parent` (3006) | `Container_Scrolling_Content` (3031) | `0` / `-42 × OUT` |
| Scroll-Indikator | `Container_Scrollbar_Parent` (3000) | `Rectangle_Scroll_Indicator` (14001) | `0` / `OUT × (288-36)/13` |

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
  `0 … (Zeilenanzahl − sichtbare Zeilen)` = `0…13` bei 20 Zeilen / 7
  sichtbaren Zeilen. Bei einer anderen Zeilenanzahl N oder Zeilenhöhe H
  ändert sich nur diese Obergrenze (`N − sichtbare_Zeilen`) und die
  Umrechnungsfaktoren unten — die Struktur bleibt gleich.
- `Container_Scrolling_Content.Top = -H × pos` (H = Zeilenhöhe, hier 42).
- `Rectangle_Scroll_Indicator.Top = pos × (Fensterhöhe − Indikatorhöhe) / pos_max`
  (hier: `pos × (288−36)/13`).
- Die 4 Softkeys ändern `pos` um ±1 (`UP`/`DOWN`) bzw. ±N (`UP_UP`/
  `DOWN_DOWN`, z. B. N=3 für "eine Bildschirmseite"), jeweils geklemmt auf
  `0…pos_max` — exakt das `ZERO`/`UP_SLOW`/`UP_FAST`/`DOWN_SLOW`/
  `DOWN_FAST`/`FULL`-Muster von `RampLimitFS`, nur mit `SLOW=1` und
  `FAST=N` sowie `VAL_ZERO=0`, `VAL_FULL=pos_max`.

## Aktueller ID-Stand (Stand: nach GUI-Re-Save)

| Klasse | Anzahl | höchste ID |
|---|---|---|
| `CGroup` (Container) | 51 | 3067 |
| `COutputText` (OutputString) | 83 | 11102 |
| `COutputNumber` | 41 | 12044 |
| `CPointer` (ObjectPointer) | 30 | 27029 |
| `CStringVariable` | 21 | 22026 |
| `CProxy` | 441 | 4194859 |
| `CRectangle` | 13 | 14107 |
| `CImage` (PictureGraphic) | 13 | 20329 |

## Offene Punkte

- **Scroll-Logik nicht verdrahtet**: die 6 SoftKey-Pointer auf
  `MainSoftKeyMask.jvi` (27024–27029) haben noch keine Makro-/
  Programmlogik, die beim Drücken `Container_Scrolling_Content.Top` und
  `Rectangle_Scroll_Indicator.Top` ändert. Kandidat für das Muster:
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
