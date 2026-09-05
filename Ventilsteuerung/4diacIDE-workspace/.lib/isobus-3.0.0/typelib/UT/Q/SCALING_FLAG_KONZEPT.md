# `xScale`-Flag für Pixel-Bausteine — Konzept

Dieses Dokument beschreibt das neue `xScale`/`rScaleFactorDM`/`rScaleFactorSKM`-Feld-Trio,
das auf den folgenden acht ISO 11783-6-Kommando-Bausteinen (`isobus::UT::Q`) ergänzt wurde:

| Baustein | Pixel-Feld(er) | Entscheidungs-ID (welches Feld die DM/SKM-Wahl trifft) |
|---|---|---|
| `Q_ChildPosition.fbt` | `s16Xposition`/`s16Yposition` | `u16ObjIdParent` |
| `Q_ChildPosition_AI.fbt` | `s16Xposition`/`s16Yposition` (über AI-Sockets) | `u16ObjIdParent` |
| `Q_ChildLocation.fbt` | `u8Xchange`/`u8Ychange` | `u16ObjIdParent` |
| `Q_Size.fbt` | `u16Width`/`u16Height` | `u16ObjId` |
| `Q_EndPoint.fbt` | `u16Width`/`u16Height` (Linien-Endpunkt) | `u16ObjId` |
| `Q_ChangePolygonScale.fbt` | `u16NewWidth`/`u16NewHeight` | `u16ObjId` |
| `Q_ChangePolygonPoint.fbt` | `u16NewXValue`/`u16NewYValue` | `u16ObjId` |
| `Q_LineAttributes.fbt` | `u8LineWidth` | `u16ObjId` |

## Warum `u16ObjIdParent` bei `Q_ChildPosition`/`Q_ChildPosition_AI`/`Q_ChildLocation`?

Diese drei Bausteine positionieren ein Kind-Objekt **relativ zur oberen linken Ecke des
Parent-Objekts** (`u16ObjIdParent`). Der Pixel-Offset lebt also im Koordinatenraum des
*Parents*, nicht des Kindes — ein Container mit ID 3200 (DataMask-Bereich) enthält seine
Kinder in DM-skalierten Pixeln, ein Container mit ID 3700 (SoftKeyMask-Bereich) in
SKM-skalierten Pixeln, unabhängig davon, welcher Objekttyp/ID-Bereich das Kind selbst hat.
Bei allen anderen fünf Bausteinen bezieht sich die Pixelangabe auf das **Objekt selbst**
(eigene Größe, eigener Polygon-Punkt, eigene Linienbreite) — dort entscheidet `u16ObjId`.

## Die Entscheidungstabelle

Quelle: `visual-programming-languages-docs/docs/en/runtime/isobus/Scaling.md`
(`C:\git\ms-docs\visual-programming-languages-docs`, auch als readthedocs-Seite verlinkt).
Jeder der acht Bausteine wählt anhand der o.g. Entscheidungs-ID zwischen drei Fällen:

1. **Centering (Faktor immer `1.0`, nie skaliert)**: `WorkingSet` (ID `0`), Softkeys
   (`5000`–`5999`), Auxiliary Function (`31000`–`31999`).
2. **SoftKeyMask/Aux-Hälfte eines geteilten Bereichs** (`rScaleFactorSKM`): Container
   (`3500`–`3999`), OutputString (`11500`–`11999`), OutputNumber (`12500`–`12999`), Line
   (`13500`–`13999`), Rectangle (`14500`–`14999`), Ellipse (`15500`–`15999`), Polygon
   (`16500`–`16999`), PictureGraphic/Working-Set-Bitmap (`20500`–`20999`), FontAttributes
   (`23500`–`23999`), LineAttributes (`24500`–`24900`), FillAttributes (`25500`–`25999`).
3. **Alles andere** (`rScaleFactorDM`): die DataMask-Hälfte eines geteilten Bereichs, sowie
   jede Objektklasse, die laut Tabelle gar keine SKM-Gegenstück-ID hat (z. B. InputNumber,
   Button, Meter, LinearBarGraph) — per Kernprinzip der Quelle ("DataMask-Objekte sind immer
   skaliert") als Standardfall.

Diese Logik ist bereits als eigenständiger, wiederverwendbarer Baustein gebaut:
**`isobus::UT::Q::helpers::F_VTScaleFactor`** (`REQ(u16ObjId, rScaleFactorDM, rScaleFactorSKM)
→ CNF(<Faktor>)`) — reine Entscheidungsfunktion, keine Pixel-Arithmetik.
**`isobus::UT::Q::helpers::F_ScalePixel`** baut direkt darauf auf: `REQ(xScale, u16ObjId,
iValue, rScaleFactorDM, rScaleFactorSKM) → CNF(<Ergebnis>)` — bei `xScale=FALSE` reicht sie
`iValue` unverändert durch (Bypass), bei `TRUE` multipliziert sie mit dem per
`F_VTScaleFactor` ermittelten Faktor. `iValue`/Rückgabe sind `DINT` (generischer Träger);
ein Aufrufer mit `INT`/`UINT`/`USINT`-Feldern konvertiert an den Rändern über die
Standard-IEC-61131-3-Konvertierungsbausteine (`iec61131::conversion::F_*_TO_DINT`/
`F_DINT_TO_*`).

## Wichtige Einschränkung: reine Interface-Erweiterung, keine Verhaltensänderung

Alle acht oben genannten Bausteine (außer `Q_ChildPosition_AI`) sind **Service-Interface-
Bausteine ohne `<FBNetwork>`/`<BasicFB>`/`<Algorithm>`** in diesem Repository — ihre
`.fbt`-Datei besteht nur aus `InterfaceList` + `Documentation`-Attribut. Die tatsächliche
Umsetzung des ISO-11783-6-Kommandos läuft zur Laufzeit über eine native, in FORTE
kompilierte C++-Implementierung, die **außerhalb dieses Repos** liegt.

**Das bedeutet konkret:** Das Hinzufügen von `xScale`/`rScaleFactorDM`/`rScaleFactorSKM` zur
`InterfaceList` erweitert den **deklarierten Vertrag** (der Baustein hat jetzt diese Inputs,
mit sinnvollen Defaults `FALSE`/`1.0`/`1.0`, sodass alle **bestehenden** SubApp-Instanzen in
diesem Repo unverändert weiterlaufen, siehe Defaultwerte). Es bewirkt **noch keine tatsächliche
Skalierung**, solange die dahinterliegende native Implementierung die neuen Felder nicht
auswertet — das ist ein Folgeschritt außerhalb dieses Repos (oder, alternativ, ein zukünftiger
composite Wrapper-Baustein nach dem Muster von `Q_ChildPosition_AI`/`PositionMarkerFSA`, der
`F_ScalePixel` vor eine interne Instanz des jeweiligen nativen Bausteins schaltet — die beiden
o.g. Helper-Bausteine sind dafür bereits einsatzbereit vorbereitet).

`Q_ChildPosition_AI.fbt` ist die einzige Ausnahme mit echtem `<FBNetwork>` in diesem Set — dort
sind `xScale`/`rScaleFactorDM`/`rScaleFactorSKM` bereits real bis zur inneren
`Q_ChildPosition`-Instanz durchverdrahtet (siehe `DataConnections`), landen dort aber ebenfalls
nur als deklarierte, noch unbenutzte Inputs.
