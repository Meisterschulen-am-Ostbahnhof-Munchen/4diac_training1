# OPC-UA lokal (Meins/OPC_UA_Lokal)

Die OPC-UA-Beispiele aus `test_VV/sys/03_OPC_UA` (zwei Geräte) laufen hier auf **einem**
Gerät (`test_AX`, FORTE_PC_AX). Jede Übung ist eine SubApp. Zum Ausprobieren wählt man sie
in `test_AX.sys` per „Change Type“ am SubApp `Control` aus.

## Was lokal geht (opcua.adoc)

| Aktion | FB | lokal |
|---|---|---|
| READ | SUBSCRIBE | ja |
| WRITE | PUBLISH | ja |
| CREATE_METHOD | SERVER | ja |
| CREATE/DELETE_OBJECT, CREATE/DELETE_VARIABLE | PUBLISH_0 | ja |
| CALL_METHOD | CLIENT | nein |
| SUBSCRIBE (Client-Subscription) | SUBSCRIBE | nein |

„Lokal“ heißt: ohne Endpunkt. Was lokal nicht erlaubt ist, läuft als Remote-Aufruf mit
Endpunkt an die eigene Station, hier `opc.tcp://localhost:4840#` (`LOCAL_OPC`). Die
eigene IP funktioniert genauso. Getestet am 2026-10-18 auf FORTE_PC (L03).

Die IDs stehen in `const/OpcUaLokal.gcf`, gebaut mit `MyLib_OPC::F_OPC_LOCAL` /
`F_OPC_REMOTE` und je einem `*_NODE`.

## Übungen

| Übung | Inhalt |
|---|---|
| L01 | wie Training_01: Input_I1 → PUBLISH, SUBSCRIBE → Output_Q1 (getestet) |
| L02 | wie Training_02: Protokoll-FBs direkt (AX_PUBLISH_1 / AX_SUBSCRIBE_1) |
| L03 | wie Training_03 ohne VT: Input_I1 ruft die Toggle-Methode per localhost, Q1 Flipflop, Q2 Zustand (getestet) |
| L04–L09 | wie Training_04–09 (SoftKeys, SR/Toggle, Adapter-Varianten), Methoden per localhost |
| L10–L12 | wie Training_10–12 (Hoch/Runter mit ILOCK, Rückmeldung, gebündelt) |
| L13 | Flip-Flop (opcua.adoc): Q1 = NICHT I1 über Flip/Flop-Knoten |
| L14 | Adder (opcua.adoc): Num1 + Num2 = Result, Werte per UaExpert |
| L15 | Methode AddValues: I1 ruft per CLIENT_2_1 mit 43 und 10 auf |
| L16 | Variablen per CLIENT: I1 schreibt 42 auf Increment, liest Incremented = 43 |
| L17 | Client-Subscription: wie L16, plus SUBSCRIBE mit Endpunkt |
| L18 | PUBLISH_0: I1/I2 legen Objekt/Variable an, I3/I4 löschen sie |
| L19 | lokal 2x lesen: zwei SUBSCRIBE auf einen Knoten (Q1 und Q2) |

L19 braucht eine FORTE mit eclipse-4diac/4diac-forte#1082. Ohne diese Änderung meldet
die zweite SUBSCRIBE „Cannot add another one“ (siehe 4diac-documentation#123).

Die Doku-Beispiele L13–L18 gibt es auch auf zwei Geräten als
`test_VV/sys/03_OPC_UA/Training_13` bis `_18`.

## Bausteine

- Lokale Varianten (`_LOC`, PUBLISH statt Remote-WRITE) in `MyLib_AX/typelib/sys`, z. B.
  `Toggle_RPC_FROM_Remote_QXA_OPC_LOC`, `logiBUS_IXA_TO_PUBLISH_OPC`.
- Lokale Net-FBs in `MyLib_AX/typelib/net`: `*_SERVER_0_PUBLISH_1`, `A2X2_PUBLISH_2_SUBSCRIBE_2(_PLUG)`.
- Taster statt VT: `Input_Toggle_RPC_TO_Remote_QXA_OPC`, `Input_Toggle_RPC_TO_Remote_AX_OPC`,
  `Input_CLIENT_Method_IE`.
