# Dialog-Lib `isobus_UT_dialog`

VT-Dialoge nach dem Vorbild der Windows-`MessageBox`: Titelzeile, Icon, Text, Tasten, Default-Button, Ergebnis, Timeout, modal oder nicht modal. Der Dialog erscheint **auf der aktuellen DataMask**, es wird keine Maske gewechselt.

## Aufbau

| Teil | Ort |
|---|---|
| Lib | `4diacIDE-workspace/.lib/isobus_UT_dialog-3.0.0` |
| Pool-Vorlage | `ISO-DesignerProjects/Workspace_Dialog` |
| Übungen | `test_AX/Uebungen/Uebung_269_AX` … `Uebung_272_AX` |

Bausteine:

- `DLG_MessageBox` (Composite FB): Dialog mit Tasten. Ereignisse `SHOW`/`CLOSE` führen zu `CNF` mit `RESULT`.
- `DLG_Toast` (Composite FB): Hinweis ohne Tasten, verschwindet nach `TIMEOUT` (Standard 3 s).
- `DLG_CTRL`: Ablaufsteuerung (Basic FB).
- Alle drei sind FBs (Instanz mit `<FB>`, nicht `<SubApp>`) und kommen mit dem ELF-Build der Lib.
- `DialogConst.gcf`: `DLG_BTN_*`, `DLG_ICON_*`, `DLG_RES_*`.
- `DialogIDs.gcf`: feste Objekt-IDs der Vorlage.

## Werte

| BUTTONS | Tasten | RESULT | Bedeutung |
|---|---|---|---|
| 0 | keine (Toast) | 0 | geschlossen oder ersetzt |
| 1 | OK | 1 | OK |
| 2 | OK, Abbrechen | 2 | Abbrechen |
| 3 | Abbrechen, Wiederholen, Ignorieren | 3 | Abbruch |
| 4 | Ja, Nein, Abbrechen | 4 | Wiederholen |
| 5 | Ja, Nein | 5 | Ignorieren |
| 6 | Wiederholen, Abbrechen | 6 / 7 | Ja / Nein |
| | | 8 | Zeit abgelaufen |

`ICON`: 0 keins, 1 Information (Titelzeile grün), 2 Frage (navy), 3 Warnung (oliv), 4 Fehler (rot).

- `DEFAULT_BUTTON` setzt den Fokus auf Taste 1 bis 3 (`Select Input Object`, VT ≥ 4).
- `MODAL = TRUE` legt eine weiße Fläche über die ganze Maske. Damit sind die Buttons darunter nicht mehr erreichbar.
- `TITLE_ID = ID_NULL` nimmt den Standardtitel passend zum Icon.

## Pool-Vorlage

Damit der Dialog auf jeder Maske erscheinen kann, muss jede DataMask `Container_Dialog` (3400) als **letztes** Objekt enthalten. Was in der Liste zuletzt steht, wird oben gezeichnet (ISO 11783-6, 4.6.13). Ein Container darf in mehreren Masken stecken (4.6.11.1).

Alle Dialog-Objekte liegen in festen ID-Blöcken im DataMask-Bereich:

- Container 3400–3415
- Buttons 6900–6906 (KeyCode = RESULT)
- Texte 11400–11423
- Rechtecke 14400ff
- Ellipsen 15400ff
- Schriften 23400ff
- Linien 24400ff
- Füllungen 25400ff
- ObjectPointer 27900–27904

Die Ziele der Pointer (Icons, Titel, Button-Reihen, Abdeckung) liegen zusätzlich auf `DataMask_Dlg_Vorlagen_invisible` (1002). Diese Maske dient nur als Ablage und wird nie angezeigt.

Ein Projekt übernimmt die Objekte **mit denselben IDs**, weil die Lib sie als Konstanten kennt.

Beim Kopieren eines Pools als Vorlage `DefaultPool.jops` weglassen. Sonst hängt `ISODesigner /Compile`, sobald der Objektbaum gewachsen ist.

## Generatoren

Pool-Objekte, Lib und Übungen werden per Skript erzeugt (`scripts_central`):

| Skript | Aufruf | Erzeugt |
|---|---|---|
| `gen_dialog_pool.py` | `<pool_dir>` | Dialog-Objekte und Testmasken in einem frischen Pool aus `Workspace_Empty` (ohne `.jops`) |
| `gen_dialog_lib.py` | `<training1_root>` | `isobus_UT_dialog-3.0.0`, IDs aus dem gebauten `DefaultPool.iop.h` |
| `gen_dialog_uebungen.py` | `<training1_root>` | `Uebung_269_AX` … `Uebung_272_AX` |

Reihenfolge: Pool erzeugen, `RunSkript_BuildDialog_AX.bat` laufen lassen, dann Lib und Übungen.

## Grenzen (Stand 1.0)

- **Eine** `DLG_MessageBox`/`DLG_Toast` je Anwendung: Jede Instanz wertet dieselben 7 Buttons aus. Für mehrere Meldungsquellen kommt `DLG_Manager`.
- Ein neues `SHOW` ersetzt einen offenen Dialog, der alte endet mit `RESULT = 0`.
- Noch am Gerät zu prüfen: Lassen sich verdeckte Eingabefelder unter `MODAL` weiter mit dem Drehknopf anwählen? Laut Norm gelten verdeckte Objekte als sichtbar (4.6.17).
