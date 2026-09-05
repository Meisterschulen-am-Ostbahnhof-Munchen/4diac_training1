# Übung 228: Kombinierte Übung mit Fenster-Farbrückmeldung

## Thema: Change Fill Attributes (ISO 11783-6 F.32) als Statusanzeige

Ableitung von [Übung 227](Uebung_227_AXA_Beschreibung.md): identischer Aufbau (Dreieck +
Split-Bargraph + Istwert, alles über AR-Adapter), zusätzlich wird das Dreieck **rot**, sobald der
Sollwert das Fenster **-2…+2** verlässt, und **grün**, solange er darin liegt.

### Situationsbeschreibung
Der Sollwert bewegt weiterhin das Dreieck und den Split-Bargraph und wird als Istwert
zurückgeschrieben (siehe Übung 227). Zusätzlich färbt sich das Dreieck selbst je nach Sollwert:
grün in der Nähe von 0 (Fenster -2…+2), rot außerhalb.

### Funktionsbeschreibung
- **Warum ein neuer Baustein nötig war:** Das Dreieck (`Polygon_Bargraph_Mittelmarker`) bezieht
  seine Füllfarbe von einem eigenen, nur für dieses Objekt genutzten `FillStyle`-Objekt
  (`FillStyle_Bargraph_Mittelmarker_Gruen`, VT-Objekt 25000, `FillType=2` = feste Farbe, kein
  Muster). Die Farbe eines FillAttributes-Objekts wird per **Change Fill Attributes** (ISO
  11783-6 F.32, `Q_FillAttributes`) gesetzt. Da dieses FillAttributes-Objekt exklusiv vom Dreieck
  verwendet wird, ändert das Umfärben keine anderen Objekte.
- Der neue Baustein `FillWindowFS_AR` (`isobus::UT::Q`) kapselt das — als `SubAppType`, nach dem
  Vorbild von `MyLib_AX-1.0.0\typelib\sys\GreenRedBackground1_AX.SUB`, statt als eigener `FBType`
  mit einer ST-Hilfsfunktion: er nimmt den Sollwert über einen AR-Socket entgegen, verteilt ihn mit
  `AR_SPLIT_2` auf `AR_GE` (`>= rWindowMin`) und `AR_LE` (`<= rWindowMax`), UND-verknüpft beide
  Ergebnisse mit `AX_AND_2` und wählt darüber mit `AX_SEL` (`G` = "im Fenster?") zwischen
  `COLOR_RED`/`COLOR_GREEN` — ausschließlich vorhandene generische Adapter-Bausteine, keine
  eigene ST-Logik. `FillType`/`FillPatternId` bleiben dabei fest auf "feste Farbe, kein Muster",
  genau wie im Pool konfiguriert. Ein sauberer, generischer `Q_FillAttributes`-Adapter-Wrapper
  (als `FBType`) ist als spätere Verfeinerung sinnvoll, aber für den Moment bewusst zurückgestellt.
- **Verteilen:** `Split` (`AR_SPLIT_4`, eine Stelle mehr als in Übung 227) verteilt den einen
  AR-Sollwert jetzt auf vier Verbraucher: Dreieck-Position, Split-Bargraph, Istwert-Rückschreibung
  und die neue Farblogik.

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_228_AXA` an (bereits als Referenzlösung vorhanden).
2. Verteilen Sie den gelesenen Sollwert mit `AR_SPLIT_4` auf vier Ziele (wie Übung 227, plus eins).
3. Färben Sie das Dreieck mit `MarkerColor` (`FillWindowFS_AR`,
   `u16ObjId := FillStyle_Bargraph_Mittelmarker_Gruen`, `rWindowMin := -2.0`,
   `rWindowMax := 2.0`).
4. Am echten Terminal testen: Sollwert zwischen -2 und +2 → Dreieck grün; außerhalb → Dreieck rot.

### Referenzlösung
`Uebung_228_AXA.SUB` — validiert gegen `subapptype.xsd`. Neuer Baustein:
`Ventilsteuerung\4diacIDE-workspace\.lib\isobus-3.0.0\typelib\UT\Q\FillWindowFS_AR.SUB`.
