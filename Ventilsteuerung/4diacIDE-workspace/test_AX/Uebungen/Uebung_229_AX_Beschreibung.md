# Übung 229: Zwei Taster, ein SR-Latch (Last-Wins) — klassisch mit AX_RF_TRIG

## Thema: Flankenerkennung + Set/Reset-Verriegelung, zwei Quellen auf einer Verriegelung

### Situationsbeschreibung
Zwei tastende Taster `I1` und `I2` sollen denselben Ausgang `Q1` schalten: `I1` schaltet EIN,
`I2` schaltet AUS. Da beide Taster tastend sind (kein Dauersignal), braucht es eine Verriegelung
(SR-Latch), die den zuletzt gedrückten Zustand hält, bis der jeweils andere Taster betätigt wird.

### Funktionsbeschreibung
- **Flankenerkennung:** Jeder physische Eingang wird über einen eigenen `AX_RF_TRIG` beobachtet -
  dieser meldet eine steigende Flanke (`ER`, Taster gedrückt) und eine fallende Flanke (`EF`,
  Taster losgelassen) als separate Events.
- **Zusammenführen zweier Quellen auf einer Verriegelung:** Beide `AX_RF_TRIG`-Instanzen speisen
  denselben `AX_SR` (Set-Reset-Latch): `I1`s steigende Flanke UND `I2`s steigende Flanke laufen
  beide auf `AX_SR.S`, beide fallenden Flanken auf `AX_SR.R`. Das ist legal in 4diac, da
  EventConnections (anders als DataConnections) mehrere Quellen auf ein Ziel erlauben - eine reine
  ODER-Verknüpfung ohne zusätzlichen Baustein.
- **Ausgang:** `AX_SR.Q` treibt direkt `Output_Q1`.

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_229_AX` an (bereits als Referenzlösung vorhanden).
2. Verbinden Sie `Input_I1`/`Input_I2` über je einen `AX_RF_TRIG` mit dem gemeinsamen `AX_SR`.
3. Testen Sie: `I1` drücken → `Q1` EIN und bleibt EIN nach Loslassen; `I2` drücken → `Q1` AUS und
   bleibt AUS; beide Taster können beliebig oft in beliebiger Reihenfolge gedrückt werden, der
   Ausgang folgt immer dem zuletzt gedrückten Taster.

### Referenzlösung
`Uebung_229_AX.SUB`. Siehe auch `Uebung_230_AX` für dieselbe Funktion, umgebaut auf die
Adapter-Bausteine `AX_ASR_RF_TRIG`/`ASR_MERGE_2`/`ASR_AX_SR` statt loser Event-Verkabelung.
