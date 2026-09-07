# Übung 230: Zwei Taster, ein SR-Latch (Last-Wins) — Umbau mit ASR-Adapter

## Thema: Dieselbe Funktion wie Übung 229, aber mit gebündelten Set/Reset-Adaptern statt loser Events

### Situationsbeschreibung

Exakt dieselbe Funktion wie `Uebung_229_AX` (zwei Taster `I1`/`I2` schalten gemeinsam `Q1` über ein
Last-Wins-SR-Latch), aber mit den neueren Adapter-Bausteinen umgesetzt: statt jede Flanke als
losen Event zu verkabeln, trägt ein `ASR`-Adapter Set UND Reset gebündelt in einem Stecker.

### Funktionsbeschreibung

- **`AX_ASR_RF_TRIG`** ersetzt `AX_RF_TRIG`: intern derselbe `E_RF_TRIG`-Kern (steigende/fallende
  Flanke), aber die beiden Events werden direkt in einen `ASR`-Adapter-Ausgang geschrieben
  (`Q.SET`/`Q.RESET`) statt als zwei lose EventOutputs (`ER`/`EF`) exportiert zu werden.
- **`ASR_MERGE_2`** ersetzt die 4 losen EventConnections aus Übung 229: er nimmt die beiden
  `ASR`-Adapter der beiden Taster entgegen und führt SET mit SET, RESET mit RESET zusammen -
  dieselbe ODER-Verknüpfung wie zuvor, jetzt aber als eigener, wiederverwendbarer,
  typsicherer Baustein statt Ad-hoc-Verkabelung.
- **`ASR_AX_SR`** ersetzt `AX_SR`: identischer ECC (Set-dominant, START→SET→RESET→SET), aber Set
  und Reset kommen gebündelt über einen `ASR`-Socket (`S_R`) statt als zwei lose EventInputs.
- Ergebnis: exakt dasselbe Verhalten wie Übung 229, aber komplett ohne rohe EventConnections -
  alle Verbindungen laufen über AdapterConnections.

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_230_AX` an (bereits als Referenzlösung vorhanden).
2. Verbinden Sie `Input_I1`/`Input_I2` über je einen `AX_ASR_RF_TRIG` mit `ASR_MERGE_2`, dessen
   Ausgang mit `ASR_AX_SR.S_R`, und `ASR_AX_SR.Q` mit `Output_Q1`.
3. Testen Sie identisch zu Übung 229 - das Verhalten muss ununterscheidbar sein, nur die
   Bausteine dahinter sind andere.
4. Vergleichen Sie die beiden SubApps im 4diac-Editor: Übung 229 hat ein `EventConnections`-Element
   mit 4 Verbindungen, Übung 230 hat gar keins - alles ist über Adapter typisiert.

### Referenzlösung

`Uebung_230_AX.SUB`. Die verwendeten Bausteine liegen in
`Ventilsteuerung\4diacIDE-workspace\.lib\adapter-3.0.0\typelib\events\unidirectional\BOOL\AX_ASR_RF_TRIG.fbt`,
`...\BOOL\ASR_AX_SR.fbt` und `...\EVENT\ASR_MERGE_2.fbt`.
