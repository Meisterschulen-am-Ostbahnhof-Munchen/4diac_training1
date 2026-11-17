# NmGetCfInfo: IND/RSP-Muster in den Übungen

Stand: 2026-11-17. Die Übungen sind umgebaut, aber **noch nicht auf Hardware getestet**.

## Warum der Umbau

Der FB `isobus::pgn::NmGetCfInfo` sendet ein Ereignis aus dem Netzwerkmanagement mit IND.
Danach wartet er auf RSP (`bwaitingForRSP = TRUE`). Erst nach RSP kommt das nächste Ereignis aus seiner internen Queue.
Bis auf 122 und 122b hatten die Übungen kein RSP verbunden. Nach dem ersten IND kam deshalb nichts mehr, auch keine Abmeldung.
Außerdem wurde jedes IND als „Teilnehmer da“ behandelt, egal welches `eNetEvent` es war.

Der FB bleibt unverändert, denn viele Bausteine arbeiten mit diesem IND/RSP-Muster.
Die Übungen zeigen jetzt das richtige Muster (Entscheidung Franz).

## Das Muster

Reine Anzeige (120, 121, 123):

- `STRUCT_DEMUX(sNetEv).CNF` → `RSP`

Übungen mit `install` (124–128b, 130–135 und in #390 auch 129, 136–139c):

| Schritt | Bausteine |
|---|---|
| `eNetEvent` holen | `IND` → `STRUCT_DEMUX(sNetEv)`. Danach `CNF` → `NetEv_Install.REQ` und `eNetEvent` → `NetEv_Install.eNetEvent` |
| Filtern | SubApp `NetEv_Install` (Typ `MyLib::sys::NetEv_Install_Filter`): `INSTALL` → install, `RSP` → `NmGetCfInfo.RSP` |
| Install quittieren | `installO` → `NetEv_Install.SET` und `RSP`, `pgnERR` → `RSP` |
| Replay beim Start | bei `member = network`: `E_RESTART.COLD/WARM` → `INIT` |

Alle Verbindungen auf `RSP` sind ausgeblendet (`Visible = false`).

Inhalt von `MyLib_B/sys/NetEv_Install_Filter.SUB`:

- `F_USINT_TO_UINT` → `E_DEMUX_8 NetEv_Verteiler`. Die Ausgänge sind beschriftet: **EO1 = K 0 Active**, **EO4 = K 3 NewAddress**. Alle anderen EO gehen auf `RSP`.
- EO1 und EO4 gehen auf die SubApp `Nur_einmal` (Typ `NetEv_Einmal`, darin `E_SWITCH` + `E_SR Installiert`):
  - beim ersten Mal → `INSTALL`
  - danach → `RSP`
- `SET` (installO) setzt den Merker, `RESET` löscht ihn. `RESET` ist in den Übungen noch nicht verbunden, siehe offener Punkt 1.

## Offene Punkte: muss jemand testen

1. **Partner meldet sich ab und wieder an.**
   - Durch den Merker `Installiert` wird die PGN pro Deploy nur einmal installiert.
   - Meldet sich der Partner ab und wieder an (VT, PEAK oder TECU, z. B. Terminal aus und wieder ein), wird nichts neu installiert.
   - Das geht nur gut, wenn der ISOBUS-Treiber für den Partner **denselben Handle** behält. Geprüft ist das nicht.
   - **Test:** Übung deployen, Nachrichten prüfen. Partner abstecken, wieder anstecken. Kommen die Nachrichten noch an?
   - Wenn nicht: Bei Inactive die PGN entfernen und `NetEv_Install.RESET` auslösen.
2. **Partner schon vor dem Deploy am Netz.**
   - Erst mit `INIT` kommt der Replay.
   - **Test:** Partner anstecken, dann deployen. Wird die PGN installiert?
3. **`thisMember`-Übungen ohne INIT** (121, 128, 128b, 129, 134, 136–139c).
   - Ist die eigene CF beim Deploy schon aktiv, kommt kein IND.
   - **Test:** Wird in diesen Übungen installiert? Wenn nicht, auch dort `E_RESTART` → `INIT` setzen. Wegen `Nur_einmal` schadet das nicht.
4. **`E_DEMUX_8` kennt nur K 0–7.**
   - Die Werte 8 und 9 (HSI) gibt es nur mit `CCI_HSI`. Kämen sie doch, käme kein RSP und der FB bliebe hängen.
5. **IDE-Check und Headless-Export** der umgebauten Übungen fehlen noch.
   - Geprüft sind bisher nur XSD, reservierte Wörter und ob alle verbundenen Pins existieren.
   - Die neuen Bausteine liegen unterhalb des bestehenden Netzes. Das Layout muss in der IDE noch zurechtgeschoben werden.

## Quelle

forte: `logiBUS-modules/isobus_PGN/src/isobus/pgn/NmGetCfInfo_fbt.cpp`, dort `executeEvent` (RSP, INIT → `ReplayAllNetworkEvents`) und `recCfInfo` (Filter, Queue).
