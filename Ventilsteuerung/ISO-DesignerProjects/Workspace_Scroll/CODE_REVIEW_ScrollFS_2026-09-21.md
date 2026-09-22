# Code-Review ScrollFS-Bausteine

Datum: 2026-09-21
Autor des Reviews: opencode (deepseek-v4.1-flash)
Status: Nur Dokumentation — es wurden **keine** Bausteine verändert.

## 1. Gegenstand

Geprüft wurden die sechs folgenden Dateien:

| Datei | Typ |
| --- | --- |
| `.lib\isobus-3.0.0\typelib\UT\Q\ScrollFS.fbt` | Composite (FBNetwork) |
| `.lib\isobus-3.0.0\typelib\UT\Q\ScrollFS_PHYS_Button.fbt` | Composite (FBNetwork) |
| `.lib\isobus-3.0.0\typelib\UT\Q\ScrollFS_PHYS_Softkey.fbt` | Composite (FBNetwork) |
| `.lib\isobus-3.0.0\typelib\UT\Q\helpers\F_ScrollBarY.fct` | Function |
| `.lib\isobus-3.0.0\typelib\UT\Q\helpers\F_ScrollListY.fct` | Function |
| `.lib\isobus-3.0.0\typelib\UT\Q\helpers\ReportScrollOffset.fbt` | Service Interface (interface-only) |

Vollständige Pfade (Workspace-Wurzel `C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\`):
`...\.lib\isobus-3.0.0\typelib\UT\Q\` bzw. `...\UT\Q\helpers\`.

## 2. Prüfgrundlage (herangezogene Abhängigkeiten)

Zum Verständnis/Abgleich zusätzlich gelesen (nicht geändert):

- Datenstrukturen: `utils\scroll\ScrollObjectPool_S.dtp`, `ScrollFull_S.dtp`, `ScrollControls_S.dtp`
- `UT\Q\Q_ChildPosition.fbt`, `UT\Q\Q_NumericValue.fbt`, `UT\Q\Q_NumericValue_PHYS.fbt`
- `UT\io\Button\Button_IE.fbt`, `UT\io\Button\ButtonActivationCode.gcf`
- `UT\io\Softkey\Softkey_IE.fbt`, `UT\io\NumericValue\NumericValue_ID.fbt`
- `UT\Q\const\IDs.gcf` (ID_NULL = UINT#16#FFFF)
- Referenz-Implementierung `RampLimitFS.fbt` aus
  `C:\4diac\4diac-ide_3.4.0-win32.win32.x86_64\4diac-ide\typelibrary\signalprocessing-3.0.0\typelib\RampLimitFS.fbt`
- Bestehende, funktionierende Vorlagen: `MyLib_AX-1.0.0\typelib\sys\AX_SwitchPic_2_1.SUB`,
  `MyLib_AX-1.0.0\typelib\sys\RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB`,
  `adapter-3.0.0\typelib\signalprocessing\ramp\AUDI_RampLimitFS.fbt`
- Konzeptdokument `Workspace_Scroll\SCROLL_KONZEPT.md`
- Git-Historie zu diesen Dateien (`5a8d4793e`, `936dfa031`, `00911f112`)

Ergänzende Struktur-Analyse der Bibliothek: In `isobus-3.0.0` gibt es 134 `.fbt`, davon 54 mit
`<FBNetwork>` und **0** mit `<BasicFB>`. Alle Nicht-Composite-FBs sind also interface-only
Service-Interface-Typen, deren Implementierung nativ (C++) außerhalb dieses Repos liegt.

## 3. Befundübersicht

| Nr. | Schwere | Kurztitel |
| --- | --- | --- |
| 1 | Kritisch | `ReportScrollOffset` ist implementierungslos und hängt in der INIT-Kette |
| 2 | Kritisch | `GOTO` klemmt nicht — entgegen eigener Doku und `SCROLL_KONZEPT.md` |
| 3 | Kritisch | Division durch Null / negatives `i32PosMax` in `F_ScrollBarY` |
| 4 | Mittel | Anschlag-Ausblendung greift erst nach dem ersten Scrollen |
| 5 | Mittel | `INT`-Abschneiden ohne Clamp in beiden Helper-Funktionen |
| 6 | Mittel | `BT_PRESSED_LATCHED` bei On-Screen-Buttons möglicherweise falsch |
| 7 | Niedrig | Massive Duplikation `_Softkey` / `_Button` |
| 8 | Niedrig | Veraltete Referenzen und veraltetes Konzeptdokument |
| 9 | Niedrig | Import-Hygiene |
| 10 | Niedrig | Fehlende `Documentation`-CDATA in `ReportScrollOffset` |

---

## 4. Detailbefunde

### Befund 1 (Kritisch): `ReportScrollOffset` ist implementierungslos und hängt in der INIT-Kette

**Beobachtung.**
`helpers\ReportScrollOffset.fbt` endet nach der `InterfaceList` bei Zeile 39/40 mit
`<Attribute Name="eclipse4diac::core::TypeHash" Value="''"/>` — es gibt **kein** `<FBNetwork>`
und **kein** `<SimpleFB>`/ECC. Der Typ hat also keinen Body.

Das ist zunächst konsistent mit der Konvention dieser Bibliothek (alle Nicht-Composite-Typen,
z. B. `Q_ChildPosition`, `Q_NumericValue`, `Button_IE`, sind genauso interface-only und werden
nativ in C++ implementiert). Der Commit-Text zu `5a8d4793e` bestätigt die Lücke aber explizit:

> "New Basic FB (isobus::UT::Q::helpers::ReportScrollOffset), modeled on the existing
> GetVtcStatus "Service Interface Block" pattern (pure InterfaceList, no ECC/BasicFB -
> hand-coded executeEvent())."
> "C++ implementation to follow once the corresponding _fbt.h/.cpp are generated."

**Warum kritisch.** Der Block ist nicht optional, sondern fest in die serielle INIT-Kette von
`ScrollFS` eingebaut (`ScrollFS.fbt:128-134`):

```
Ramp.INITO      -> ScrollReport.INIT
ScrollReport.INITO -> MoveBar.INIT
MoveBar.INITO   -> MoveList.INIT
MoveList.INITO  -> INITO
```

Damit gilt: Fehlt der native Typ, schlägt das Deployment fehl (unbekannter FB-Typ). Existiert er,
liefert aber kein `INITO` (z. B. weil `u16ContainerId` = `ID_NULL` ist oder der FB deaktiviert
bleibt), wird die INIT-Kette nie abgeschlossen — `MoveBar`/`MoveList` werden nie initialisiert
und `ScrollFS.INITO` wird nie gesendet.

**Empfehlung.**
- Vor dem Ausrollen verifizieren, dass die C++-Implementierung inkl. Registrierung
  (`ReportScrollOffset`/`ScrollReport`) und `VtMaskVisibility_OnScroll()` existiert.
- Sicherstellen, dass `INIT` unter allen Umständen (auch `ID_NULL`) `INITO` liefert.
- Alternativ: `ScrollReport` aus der kritischen INIT-Kette herausnehmen (z. B. parallel
  betreiben) und/oder durch die native Implementierung absichern.
- Beschreibungstext korrigieren: es ist ein nativer Service-Interface-Block, kein „Basic FB“
  im Sinne eines `<SimpleFB>` mit ECC.

### Befund 2 (Kritisch): `GOTO` klemmt nicht — entgegen eigener Doku

**Beobachtung.** In `ScrollFS.fbt` steht bei `SET_POS` (Zeile 50):

> "Target position for the GOTO event, clamped to 0..stObj.i32PosMax"

`GOTO` wird direkt auf `Ramp.LOAD` gelegt (`ScrollFS.fbt:116`), `SET_POS` dauerhaft auf
`Ramp.PV` (`ScrollFS.fbt:140`). Der reale Algorithmus von `RampLimitFS.LOAD` (aus der
verwendeten Bibliothek `signalprocessing-3.0.0`) klemmt aber ausdrücklich **nicht**:

> Algorithmus `LOAD` (Zeile 169-174):
> "Load an externally supplied preset directly into OUT: OUT := PV. **Not clamped to
> VAL_ZERO/VAL_FULL** - caller is expected to pass an already-valid value ..."
> `OUT := PV;`

`SCROLL_KONZEPT.md:210` behauptet ebenfalls eine Klemmung („`OUT := SET_POS`, geklemmt auf
`0…POS_MAX`") — das ist falsch.

**Auswirkung.** Da die Zielposition über ein freies Eingabefeld (`NumericValue_ID`) kommt, kann
`OUT > i32PosMax` (oder negativ) werden. Folgen:
- `F_ScrollListY` liefert eine zu große negative Y-Position → die Liste scrollt über das Ende
  hinaus (leere Zeilen).
- `F_ScrollBarY` liefert `i32BarBaseOffset + pos*i32BarTravel/i32PosMax > i32BarBaseOffset +
  i32BarTravel` → Indikator läuft aus der Spur.
- Nachfolgende `LINE_DOWN`/`PAGE_DOWN` erhöhen weiter; erst `FIRST`/`LAST` reparieren den Zustand
  (diese setzen `OUT` per Zuweisung).

**Empfehlung.** Vor `Ramp.LOAD` auf `0..i32PosMax` klemmen (z. B. `F_MAX`/`F_MIN` bzw.
`F_LIMIT`), oder mindestens die Kommentare/Doku korrigieren. Zusätzlich beachten:
`GotoInput.IN` ist `DWORD`, die Umrechnung erfolgt über `F_DWORD_TO_DINT`; Werte > 2^31 werden
dabei negativ.

### Befund 3 (Kritisch): Division durch Null / negatives `i32PosMax` in `F_ScrollBarY`

**Beobachtung.** `helpers\F_ScrollBarY.fct:47`:

```
F_ScrollBarY := DINT_TO_INT(i32BarBaseOffset + (i32Pos * i32BarTravel) / i32PosMax);
```

Es gibt keinerlei Schutz gegen `i32PosMax <= 0`. Laut `SCROLL_KONZEPT.md:355` berechnet
`GcfScript.py` `PosMax = floor((ContentHeight − ParentHeight) / RowHeight)`. Passt die Liste
komplett ins Sichtfenster, ist das 0; ist der Inhalt kleiner als das Fenster, wird der Wert
negativ. In beiden Fällen teilt die Funktion bei **jedem** `Ramp.CNF` (also auch bei
`FIRST`/`LAST`) durch 0 bzw. durch eine negative Zahl — in FORTE ein Laufzeitfehler bzw. eine
unsinnige Position.

**Empfehlung.**
- In `F_ScrollBarY` für `i32PosMax <= 0` einen definierten Ersatzwert liefern
  (z. B. `i32BarBaseOffset`).
- `GcfScript.py` so anpassen, dass `i32PosMax` mindestens 1 ist (Schein-Scrollbalken für
  nicht-scrollbare Listen vermeiden oder Liste als statisch behandeln).

### Befund 4 (Mittel): Anschlag-Ausblendung greift erst nach dem ersten Scrollen

**Beobachtung.** `RampLimitFS` liefert bei `INIT` **nur** `INITO` (ECC: `ECState INIT` →
`Algorithm INIT, Output INITO`, `RampLimitFS.fbt:84-86`), **kein** `CNF`. Der `INIT`-Algorithmus
setzt `OUT := VAL_ZERO`, also 0, und `qAtZero := TRUE`.

Die Pointer-Umleitung (UP/PAGE_UP bzw. DOWN/PAGE_DOWN ausblenden) wird in den Wrappern aber
ausschließlich von `Inner.CNF` getriggert (`ScrollFS_PHYS_Softkey.fbt:159-174`,
`ScrollFS_PHYS_Button.fbt:159-174`). `Inner.CNF` stammt wiederum von `Ramp.CNF`
(`ScrollFS.fbt:117`), das beim Initialisieren nie feuert.

**Auswirkung.** Beim Einschalten steht die Position auf 0 (`qAtFirst = TRUE`), aber UP/PAGE_UP
bleiben sichtbar, bis der Bediener erstmals scrollt. Die Ausblendung „am Anschlag“ startet also
nicht mit dem korrekten Anfangszustand.

**Empfehlung.** `Inner.INITO` zusätzlich auf die vier `*.REQ`-Eingänge der F_SEL-Kette legen
(analog zu `Inner.CNF`). `RampLimitFS.INITO` führt `OUT`, `qAtZero`, `qAtFull` bereits mit
(`RampLimitFS.fbt:59-63`), die Daten sind zu diesem Zeitpunkt gültig.

### Befund 5 (Mittel): `INT`-Abschneiden ohne Clamp in beiden Helper-Funktionen

**Beobachtung.**
- `F_ScrollListY.fct:41`: `F_ScrollListY := DINT_TO_INT(-(i32Pos * i32RowHeight));`
- `F_ScrollBarY.fct:47`: `... := DINT_TO_INT(...)` (siehe Befund 3)

Beide rechnen in `DINT` und wandeln anschließend ohne Begrenzung nach `INT` (16 Bit). Bei langen
Listen oder großen Offsets (|Wert| > 32767) kippt das Ergebnis still ins Negative.

**Einordnung.** Das s16-Limit ist protokollbedingt (`Q_ChildPosition.s16Yposition` ist `INT`,
ISO 11783-6 F.16), also nicht grundsätzlich behebbar. Ein sauberes Clamping auf
`[-32768, 32767]` (statt stillem Wrap) wäre aber robuster und würde das Problem sichtbar machen.

### Befund 6 (Mittel): `BT_PRESSED_LATCHED` bei On-Screen-Buttons möglicherweise falsch

**Beobachtung.** `ScrollFS_PHYS_Button.fbt:88` u. a. konfigurieren alle sechs `Button_IE` mit
`InputEvent = BT_PRESSED_LATCHED` und importieren nur diesen Code (`:15`). In
`ButtonActivationCode.gcf:11,26` ist `BT_PRESSED_LATCHED` Code 1; der zugehörige Release-Code
ist `BT_RELEASED_UNLATCHED` = 0.

**Risiko.** Ist ein Button-Objekt im Pool als *latching* ausgelegt, wechselt es pro Betätigung
zwischen Code 1 (gedrückt/verriegelt) und Code 0 (entriegelt). Lauscht der FB nur auf Code 1,
wird jede zweite Betätigung ignoriert.

**Empfehlung.** Vor dem Einsatz am Terminal prüfen, ob die verwendeten Button-Objekte momentan
oder latching sind. Bei latching ggf. zusätzlich `BT_RELEASED_UNLATCHED` behandeln.
(Die Softkey-Variante mit `SK_PRESSED` ist davon nicht betroffen.)

### Befund 7 (Niedrig): Massive Duplikation `_Softkey` / `_Button`

**Beobachtung.** `ScrollFS_PHYS_Softkey.fbt` und `ScrollFS_PHYS_Button.fbt` sind jeweils ~233
Zeilen und bis auf sechs FB-Typen (`Softkey_IE` vs. `Button_IE`), einen Import und einen
Parameter-String identisch. Zusätzlich ist die komplette Hide-Logik (4× `F_SEL` + 4×
`Q_NumericValue` + Verkabelung von `qAtFirst`/`qAtLast`) in jedem Wrapper erneut enthalten.

**Empfehlung.**
- Die Anschlag-Ausblendung in `ScrollFS` selbst ziehen, damit alle Aufrufer sie erben.
- Die beiden Wrapper aus einer gemeinsamen Vorlage generieren oder den Eingabe-Quelltyp über
  einen Adapter/Subapp entkoppeln.

### Befund 8 (Niedrig): Veraltete Referenzen und veraltetes Konzeptdokument

- `ScrollFS.fbt:3` (Identification): „... see **ScrollFS_PHYS** for that.“ — `ScrollFS_PHYS.fbt`
  existiert nicht mehr (umbenannt in `_Softkey`/`_Button`).
- `ScrollFS_PHYS_Button.fbt:3`: „Same as **ScrollFS_PHYS**, but ...“ — gleicher veralteter Name.
- `SCROLL_KONZEPT.md:309-343` („Interner Aufbau von `ScrollFS_PHYS`“) beschreibt noch den alten
  internen Aufbau mit `F_MUL`/`F_SUB`/`F_DIV`/`F_ADD` statt der heutigen Funktionen
  `F_ScrollListY`/`F_ScrollBarY` und der Wrapper `_Softkey`/`_Button`.
- `SCROLL_KONZEPT.md:191-193` listet die (laut eigenem Dokument `:380` zwischenzeitlich
  korrigierte) vertauschte Event-Zuordnung — irreführend.
- `SCROLL_KONZEPT.md:341` nennt noch den Dateipfad `...\UT\Q\ScrollFS_PHYS.fbt`.
- Der leere Asset-Ordner `.ScrollFS.fbt.assets\` bzw. `.ScrollFS_PHYS.fbt.assets\` existiert
  noch (für `ScrollFS_PHYS.fbt`, das es nicht mehr gibt).

**Empfehlung.** Referenzen und Konzeptdokument nachziehen; verwaisten Asset-Ordner entfernen.

### Befund 9 (Niedrig): Import-Hygiene

- `ScrollFS_PHYS_Softkey.fbt:20` und `ScrollFS_PHYS_Button.fbt:20` importieren
  `iec61131::conversion::F_UINT_TO_UDINT`, verwenden ihn aber nirgends. Unkritisch, weil die
  direkte Verbindung `F_SEL.OUT` (`UINT`) → `u32NewValue` (`UDINT`) zulässig ist und bereits so
  in `AX_SwitchPic_2_1.SUB:51` praktiziert wird. Der Import ist trotzdem überflüssig.
- `ScrollFS.fbt:9-15` importiert die beiden Helper-Funktionen, aber nicht `Q_ChildPosition`
  (gleiches Paket) bzw. `helpers::ReportScrollOffset`. Die `Type`-Attribute sind voll qualifiziert,
  daher funktional unkritisch, aber inkonsistent.

### Befund 10 (Niedrig): Fehlende `Documentation`-CDATA in `ReportScrollOffset`

Anders als alle `Q_*`-Blöcke (z. B. `Q_ChildPosition.fbt:50-155`, `Q_NumericValue.fbt:38-107`) hat
`ReportScrollOffset.fbt` keine `<Attribute Name="Documentation">`-CDATA. Der Inhalt der
Beschreibung steckt nur in der `Identification`, der „Description“-Tab im IDE bleibt leer.
Die zugehörige `helpers\.ReportScrollOffset.fbt.assets\type.adoc` ist leer (das ist bei 4diac
normal, aber hier fehlt dadurch jegliche Beschreibung im Dokumentations-Tab).

---

## 5. Positiv

- Alle sechs Dateien sind XML-wohlgeformt (geprüft).
- Die Event-Richtung ist korrekt: `FIRST→ZERO`, `PAGE_UP→DOWN_FAST`, `LINE_UP→DOWN_SLOW`,
  `LINE_DOWN→UP_SLOW`, `PAGE_DOWN→UP_FAST`, `LAST→FULL`, `GOTO→LOAD` (`ScrollFS.fbt:110-116`).
  Das entspricht der in `SCROLL_KONZEPT.md:380-381` dokumentierten Korrektur und ist für eine
  Liste semantisch richtig (Zeile hoch = Position verringern).
- Der `F_MOVE`-Snapshot von `stObj` bei `INIT` ist korrekt nach dem `Q_NumericValue_PHYS`-Muster
  umgesetzt und stellt `Snap.OUT.*` dauerhaft bereit (`ScrollFS.fbt:59-88`,
  `ScrollFS_PHYS_*.fbt:45-83`).
- Die F_SEL/Ptr-Kette ist event-technisch sauber: `Q_NumericValue` schreibt **nicht** bei `INIT`
  (nur `REQ` führt `u32NewValue`, `Q_NumericValue.fbt:15-17`), daher führt der anfänglich noch
  nicht berechnete `F_SEL.OUT`-Wert zu keinem Fehlschreiben der Pointer.
- `xScale` wird konsistent von den Wrappern über `ScrollFS` bis `Q_ChildPosition` durchgereicht.
- Die `INT`-Rückgabetypen der Helper passen zu `Q_ChildPosition.s16Yposition` (`INT`).

## 6. Offene Verifikationspunkte

1. Existiert die native C++-Implementierung von `ReportScrollOffset` inkl. Registrierung und
   liefert sie immer `INITO`? (Befund 1 — Blocker)
2. Verhalten der On-Screen-Button-Objekte im Pool: momentan oder latching? (Befund 6)
3. Liefert `GcfScript.py` für reale Pools je `i32PosMax == 0` oder negativ? (Befund 3)
4. Gewünschtes Startverhalten der Anschlag-Ausblendung (sichtbare UP-Buttons bei Position 0
   akzeptabel?) (Befund 4)

## 7. Empfohlene Reihenfolge der Behebung

1. Befund 1 (Deployment-Blocker) — native Implementierung sicherstellen.
2. Befund 2 (Clamp vor `LOAD`) und Befund 3 (Guard in `F_ScrollBarY`) — beide im Kern.
3. Befund 4 (INITO auf die F_SEL-Kette).
4. Befund 6 (Button-Aktivierungscode prüfen), Befund 5 (Clamp), Befund 7 (Refactoring).
5. Befund 8-10 (Doku/Hygiene).

## 8. Anhang: Verwendete externe Referenzen

- `RampLimitFS` (Typelibrary `signalprocessing-3.0.0`):
  `C:\4diac\4diac-ide_3.4.0-win32.win32.x86_64\4diac-ide\typelibrary\signalprocessing-3.0.0\typelib\RampLimitFS.fbt`
- Konzept: `Workspace_Scroll\SCROLL_KONZEPT.md`
- Git-Commits zu den geprüften Dateien: `5a8d4793e` (ReportScrollOffset neu), `936dfa031`
  (INITO ergänzt), `00911f112` (INIT-Kette serialisiert)
