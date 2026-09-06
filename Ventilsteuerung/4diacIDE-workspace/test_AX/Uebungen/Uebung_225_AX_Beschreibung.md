# Übung 225: Dreieck-Sollwertmarker

## Thema: Virtual-Terminal-Objektpositionierung (ISO 11783-6 Annex F.16)

### Situationsbeschreibung
Im ISO-Designer-Pool `Workspace_Dreieck` zeigt ein kleines Dreieck (`Polygon_Bargraph_Mittelmarker`)
innerhalb eines 96×14 px großen Containers (`Container_Sollwertmarker`) eine Sollposition an —
analog zum Mittelmarker, wie er in der echten Krauternter-Anwendung für Achslenkung/Hangausgleich
verwendet wird. Der Bediener gibt über das Eingabefeld `InputNumber_Sollwert` (VT-Objekt 9000) einen
Wert zwischen **-42 und +42** ein (0 = Mitte, ISO-Designer wendet den Offset -42 bereits objektseitig
an). Das Dreieck soll dieser Eingabe sofort folgen, und der eingestellte Wert soll zusätzlich als
Istwert (`NumberVariable_Istwert`, treibt sowohl `InputNumber_Istwert` als auch den Bargraph-Zeiger)
zurückgemeldet werden.

### Funktionsbeschreibung
- **Sollwert lesen:** Ändert der Bediener `InputNumber_Sollwert`, liefert das VT den physikalischen
  Wert (bereits skaliert/versetzt gemäß Offset -42) als `REAL`.
- **Dreieck bewegen:** Der Sollwert (-42…+42) muss auf die tatsächliche Pixel-X-Position
  (0…84) innerhalb des Containers umgerechnet werden (`+42`, dann `REAL`→`INT`) und per
  **Change Child Position** (ISO 11783-6 Annex F.16) auf das Polygon-Objekt geschrieben werden —
  Kind-Objekt ist das Dreieck (`Polygon_Bargraph_Mittelmarker`, ID 16000, gültig als Kind: TypPolygon
  16000–16999), Parent-Objekt ist der Container (`Container_Sollwertmarker`, ID 3000, gültig als
  Parent: Container, Annex B.4). Y bleibt konstant 0.
- **Istwert zurückschreiben:** Derselbe physikalische Sollwert wird unverändert (gleicher Offset,
  keine weitere Umrechnung nötig) auf `NumberVariable_Istwert` geschrieben — dadurch aktualisieren
  sich sowohl `InputNumber_Istwert` als auch der Bargraph-Positionszeiger gleichzeitig.

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_225_AX` an (bereits als Referenzlösung vorhanden).
2. Lesen Sie `InputNumber_Sollwert` (VT-Objekt 9000) mit einer `NumericValue_PHYS`-Instanz
   (`stObj := NumberVariable_Sollwert_N` aus `DefaultPool_Dreieck_Numeric.gcf`) — das VT meldet
   Wertänderungen eines an eine `NumberVariable` gebundenen Eingabefelds unter der Objekt-ID der
   Variable (hier `NumberVariable_Sollwert`, 21000), nicht unter der ID des Eingabefelds selbst
   (9000).
3. Rechnen Sie den physikalischen Wert per `F_ADD` (+42.0) und `F_REAL_TO_INT` auf die
   Pixel-X-Position (0…84) um.
4. Schreiben Sie die neue Position mit `Q_ChildPosition` (`u16ObjId := Polygon_Bargraph_Mittelmarker`,
   `u16ObjIdParent := Container_Sollwertmarker`, `s16Yposition := 0`).
5. Schreiben Sie parallel denselben physikalischen Sollwert mit `Q_NumericValue_PHYS`
   (`stObj := NumberVariable_Istwert_N`) als Istwert zurück.
6. Am echten Terminal testen: Sollwert ändern → Dreieck folgt sofort, Istwert-Feld und
   Bargraph-Zeiger zeigen denselben Wert.

### Referenzlösung
`Uebung_225_AX.SUB` — validiert gegen `fbtype.xsd`/`subapp.xsd` (siehe `iec61499-creator`-Skill).
