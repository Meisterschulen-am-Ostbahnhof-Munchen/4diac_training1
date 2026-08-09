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

Zwei ineinander verschachtelte Container plus eine feste Zeilenhöhe:

```
MainMask.jvi (480×480, Top=108 auf der Maske positioniert)
└─ Container_Scrolling_Parent (JVS-ID 3006, CGroup, 480×288, ClipsChildren=1)   ← "Sichtfenster"
   └─ Container_Scrolling_Content (JVS-ID 3031, CGroup, 432×850)               ← eigentliche Liste
      ├─ Container_Row_01 (Top=0)     ← Zeile 1
      ├─ Container_Row_02 (Top=42)    ← Zeile 2
      ├─ Container_Row_03 (Top=84)    ← Zeile 3
      ├─ …
      └─ Container_Row_20 (Top=798)   ← Zeile 20
```

- **`Container_Scrolling_Parent`** ist das sichtbare Fenster: fix 288 px
  hoch, `ClipsChildren=1` schneidet alles ab, was über den Rand hinausragt.
  Bei 288 px / 42 px Zeilenhöhe sind gleichzeitig **~6–7 Zeilen** sichtbar.
- **`Container_Scrolling_Content`** ist die eigentliche Liste, 850 px hoch
  (20 × 42 px + Rand) — deutlich größer als das Sichtfenster.
- **Scrollen** heißt: die `Top`-Eigenschaft von `Container_Scrolling_Content`
  innerhalb des Sichtfensters negativ verschieben (z. B. −42, −84, …), damit
  andere Zeilen in den sichtbaren Bereich rutschen. Jede Zeile selbst bleibt
  dabei unverändert an ihrer festen Position (`Top = 42 × (Zeilennummer−1)`)
  innerhalb der Content-Liste.

> ⚠️ **Offen / noch nicht verdrahtet:** `EnableScrolling` ist auf allen
> Masken `0` — das native VT-Scrollen wird also nicht genutzt. Es gibt
> bereits 6 neue `CPointer`-Komponenten auf `MainSoftKeyMask.jvi`
> (`ObjectPointer_SoftKey_Back` + 5 weitere, JVS-ID 27024–27029), die nach
> Optik für Softkeys (vermutlich hoch/runter/zurück) angelegt wurden — die
> eigentliche Logik, die bei Tastendruck den `Top`-Wert von 3031 verändert
> (Macro oder Steuerungslogik auf ECU-Seite), ist noch nicht umgesetzt.

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

Um das Muster greifbar zu machen, an dieser Stelle **eine konkrete Zeile**
durchgespielt — Zeile 3, wie sie tatsächlich im Pool steht. Der Kontext
(Krauternter) legt nahe, dass hier später mal eine Kraut-Charge angezeigt
wird; die Werte unten sind aktuell noch Platzhalter, keine echte
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

- **Scroll-Logik nicht verdrahtet**: die 6 neuen SoftKey-Pointer auf
  `MainSoftKeyMask.jvi` haben noch keine Makro-/Programmlogik, die beim
  Drücken den `Top`-Wert von `Container_Scrolling_Content` (3031) ändert.
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
