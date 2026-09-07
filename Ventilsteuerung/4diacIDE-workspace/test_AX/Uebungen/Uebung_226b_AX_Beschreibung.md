# Übung 226b: Split-Bargraph mit AR-Adapter

## Thema: Virtual-Terminal-Bargraphen — AR-Adapter-Variante

Adapter-Variante von [Übung 226](Uebung_226_AX_Beschreibung.md): identische Funktion, aber das Lesen
von `InputNumber_Sollwert` läuft über den AR-Adapter-Baustein `NumericValue_PHYSA` statt über ein
plain `REQ`/`IND`-Event. Die Bargraph-Ansteuerung nutzt weiterhin den wiederverwendbaren
`BargraphSplitFS` — inklusive Klammern und `xOverRight`/`xOverLeft` — passend zu 226.

### Warum ein neuer Baustein nötig war
`BargraphSplitFS` hat keine AR-Adapter-Schnittstelle. Genau wie bei `PositionMarkerFSA`, das
`PositionMarkerFS` um einen AR-Socket herum verpackt, gibt es jetzt `BargraphSplitFS_AR`
(`isobus::UT::Q`): ein neuer, kleiner Wrapper, der **intern eine einzige Instanz von
`BargraphSplitFS` aufruft** (keine Duplizierung der Klammer-Logik) und `xOverRight`/`xOverLeft` als
AX-Adapter-Plugs nach außen reicht — exakt dieselbe Baustein-Form wie `PositionMarkerFSA`. Die
bestehenden Bausteine `NumericValue_PHYSA`/`BargraphSplitFS` wurden dafür **nicht** verändert.

### Verdrahtung
- `Sollwert_N` (`NumericValue_PHYSA`) liest `InputNumber_Sollwert`, liefert den Wert als AR-Plug `rPhys`.
- `SplitBar` (`BargraphSplitFS_AR`) steuert beide Bargraphen an, mit Klammerung und
  `xOverRight`/`xOverLeft`.
- Da hier - anders als bei 225b_AXA mit seinem parallelen Istwert-Schreiben - nur **ein** Verbraucher
  den Sollwert braucht, entfällt `AR_SPLIT_2`: `Sollwert_N.rPhys` verbindet sich direkt mit
  `SplitBar.rPhys`.
- Alles ausschließlich über `<AdapterConnections>` verdrahtet - keine einzige plain Event-/
  DataConnection nötig, genau wie bei `Uebung_011b1_PHYSA`.

### Referenzlösung
`Uebung_226b_AX.SUB` — validiert gegen `subapptype.xsd`. Neuer Baustein:
`Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\BargraphSplitFS_AR.fbt`.
