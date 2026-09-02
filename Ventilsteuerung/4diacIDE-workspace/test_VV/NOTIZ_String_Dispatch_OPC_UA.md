# NOTIZ: String-Dispatch-Variante der verteilten SR/Toggle-Flipflop-Übung (OPC-UA)

Kontext: in `C:\git\ms\4diac_training1` (Branch `feature/test_VV`) wurde
`test_VV/sys/03_OPC_UA/Training_04_OPC_UA_RES` gebaut — die verteilte
SR/Toggle-Flipflop-Übung (3 SoftKeys: Set/Reset/Toggle, `AX_T_FF_SR`) über
zwei Geräte (Station 11/12) per OPC-UA Method Call, **"Option A"**: 3
eigene, typisierte Methoden (`CLIENT_0`/`SERVER_0`, je ein Paar pro
Set/Reset/Toggle), keine Wert-Übertragung, reiner RPC-Trigger.

Diskutiert wurde auch **"Option B"** (Dr. Valeriy Vyatkin, generischer
Dispatch): EINE Methode mit einem WSTRING-Parameter ("SET"/"RESET"/
"TOGGLE"), auf der Empfängerseite per String-Vergleich auf S/R/CLK
geroutet. Funktional gleichwertig, aber bewusst als **eigene, separate
Übung** zurückgestellt (Konvention in diesem Projekt: eine Variante = eine
neue Nummer, nicht in dieselbe Übung mischen). Falls du das jetzt baust,
hier die wichtigsten Erkenntnisse aus der Option-A-Arbeit, die 1:1 gelten:

## Wichtigste Falle: native CLIENT_x_y/SERVER_x_y-FBs feuern NICHT automatisch

`net-3.0.0/typelib/CLIENT_0.fbt` und `SERVER_0.fbt` hatten im Original
(4diac IDE 3.4.0) `INIT`/`INITO` als PLAIN `Type="Event"`, nicht `EInit`.
Das bedeutet: sie feuern NICHT automatisch, wenn sie unverdrahtet in einem
SUB-Style-Composite stecken (kein Zugriff auf `START.COLD`) — anders als
z.B. `AX_CLIENT_1_0`/`AX_SUBSCRIBE_1`, die als eigene FBType-Wrapper ihr
eigenes `INIT` bewusst als `EInit` deklarieren und intern an die native
(plain-Event) `INIT` durchreichen.

Für `Training_04_OPC_UA_RES` wurde das gelöst, indem die INIT/INITO-Events
von `CLIENT_0.fbt`/`SERVER_0.fbt` DIREKT in der lokalen 4diac-IDE-Installation
gepatcht wurden (`C:\4diac\4diac-ide_3.4.0-win32.win32.x86_64\4diac-ide\
typelibrary\net-3.0.0\typelib\{CLIENT_0,SERVER_0}.fbt`, `Type="Event"` →
`Type="EInit"`). Kein eigener Adapter-Wrapper mehr nötig, da die native
FBs seitdem selbst auto-initen.

**Falls deine Option-B-Methode `CLIENT_1_0`/`SERVER_1_0` (1 WSTRING-Argument,
kein Rückgabewert) statt `CLIENT_0`/`SERVER_0` braucht**: dieselbe Prüfung
machen! Vermutlich hat auch `CLIENT_1_0.fbt`/`SERVER_1_0.fbt` (und alle
anderen `CLIENT_<n>`/`SERVER_<n>`-Varianten) noch `INIT`/`INITO` als plain
`Event` im Auslieferungszustand — dann entweder denselben Patch anwenden,
ODER (sauberer, falls "RES style" statt "SUB style" gewählt wird) explizit
`START.COLD`/`WARM` auf Resource-Ebene an `INIT` verdrahten (siehe
`opcua.adoc`: "Do not forget to connect the COLD/WARM events ... to the
INIT event ports").

## myOpcUaAddresses.gcf-Konvention (VV::const::OPC_UA)

Namensschema für neue Konstanten (siehe `VV/const/OPC_UA/myOpcUaAddresses.gcf`
im test_VV-Workspace der anderen Clone):
- Zustandswerte: `<Prefix>_LOCAL_READ` (ACTION=READ, AX_SUBSCRIBE_1) +
  `<Prefix>_REMOTE_WRITE` (ACTION=WRITE, AX_CLIENT_1_0) — Pfad/Name-Suffix
  MUSS in beiden identisch sein.
- RPC-Trigger: `<Prefix>_LOCAL_METHOD` (ACTION=CREATE_METHOD, SERVER_0) +
  `<Prefix>_REMOTE_CALL` (ACTION=CALL_METHOD, CLIENT_0) — dito, identischer
  Pfad/Name-Suffix.
- Node-Pfade unter `/Objects/<Kategorie>/<Name>`, z.B.
  `/Objects/SRFlipflop/SR1_Set`.

## Referenz-Implementierung

Fertige, validierte Option-A-Umsetzung zum Vergleich/Wiederverwenden:
`C:\git\ms\4diac_training1` (Branch `feature/test_VV`),
`Ventilsteuerung/4diacIDE-workspace/test_VV/sys/03_OPC_UA/Training_04_OPC_UA_RES/`
(+ `Type Library/MyLib/sys/Uebung_010e_PC_A_OPC.SUB` /
`Uebung_010e_PC_B_OPC.SUB`). Für Option B: gleiche Struktur, nur die 3
`CLIENT_0`/`SERVER_0`-Paare durch 1 `CLIENT_1_0`/`SERVER_1_0`-Paar +
String-Vergleichslogik (z.B. `F_STRING_EQUAL`/`E_SWITCH`) auf Geraet B
ersetzen, die dann auf `AX_T_FF_SR.S`/`.R`/`.CLK` routet.
