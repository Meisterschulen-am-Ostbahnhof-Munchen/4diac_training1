# Plan: PWM-Trainingsbeispiel (12 Kanäle)

**Status: abgeschlossen ✅ (2026-08-30)** — Feature fertig, alle beim Live-Test
gefundenen Bugs behoben und vom Nutzer bestätigt (VT + Web-UI stimmen für
alle 12 Kanäle inkl. Fehlerzustand überein, siehe unten).

## Ausgangslage

Analog zum bestehenden DI/DO-Trainingsbeispiel (`Uebungen::Uebung_011b1` /
`Meins::InputOutputTester::Button_DIDO_OPC_UA` / `Workspace_DIDO` /
`apixon-diodo-client`) soll ein zweites, paralleles Beispiel für **12 PWM-Ausgänge**
(0-100 % Duty) entstehen, steuerbar über ISOBUS-VT und Web (OPC-UA). Die 8 digitalen
Eingänge bleiben unverändert (nicht PWM).

Das bestehende DI/DO-Beispiel wurde dazu zuerst auf `_DIDO` umbenannt (SUB-Composite,
VT-Projekt, Web-Client), damit Lernende beide Beispiele klar auseinanderhalten können.

## Architektur-Entscheidungen

- **Wertebereich intern:** SAE J1939/ISO 11783 Fieldbus-Konvention
  `eclipse4diac::signalprocessing::FIELDBUS_SIGNAL::VALID_SIGNAL_W` = 0-64255
  (0x0000-0xFAFF), statt einer erfundenen Skala. `RampLimitFS` arbeitet in diesem
  Bereich (`VAL_ZERO=0`, `SLOW=643` ~1%, `FAST=6426` ~10%, `VAL_FULL=64255`).
- **Umrechnungskette:** OPC-UA/Web nutzt Prozent REAL 0.0-100.0. Intern rechnen
  `FIELDBUS_PERCENT_TO_WORD`/`FIELDBUS_WORD_TO_PERCENT` (Standard-4diac-Funktionen)
  aber mit **Anteil 0.0-1.0**, nicht Prozent. Dafür zwei Umrechnungsebenen:
  - `MyLib::sys::F_PWM_PERCENT_TO_RAW` / `F_PWM_RAW_TO_PERCENT` (SubApp): Anteil
    0.0-1.0 ↔ Fieldbus-Rohwert (DINT, 0-64255)
  - `logiBUS::signalprocessing::fieldbus::F_PERCENT_TO_FRACTION` /
    `F_FRACTION_TO_PERCENT` (FBType): Prozent 0-100 ↔ Anteil 0.0-1.0
- **VT-Balkengrafik:** keine echte `CLinearBargraph`-Vorlage im gesamten Repo
  auffindbar. Lösung: `Class="CRectangle"` + `PropertySheet Name="Bargraph"`
  (dasselbe Schema wie `CArc`), Vorlage aus `4diac_EasyExampleCounter`
  (`LinearBargraph_Tageszaehler`, Objekt 18001).
- **Tasten-Handling:** `isobus::UT::io::Button::Button_IE` mit
  `Parameter InputEvent="BT_PRESSED_LATCHED"` statt `Button_IXA`+`AX_RF_TRIG` —
  einfacher, kein Adapter-Bridging nötig, direktes `.IND → RampLimitFS.<Event>`.
- **Zwei-Quellen-Merge auf `RampLimitFS.PV`:** 4diac IDE lässt keine Mehrfach-
  Verbindung auf einen Dateneingang zu ("Multiple input connections on variable").
  Fix mit dem in `Uebung_015.SUB` bereits bewährten Muster: `E_RS`
  (Set/Reset-Bistabil) + `F_SEL` (Binärauswahl) — je eine Quelle setzt/resettet das
  Bistabil, dessen `Q` steuert `F_SEL.G`, `F_SEL.OUT` ist die einzige Verbindung
  auf `RampLimitFS.PV`.
- **Balken + Zahlenfeld teilen sich eine `CNumberVariable`** (`u16ObjId_VALUEVAR`),
  dadurch reicht eine `Q_NumericValue`-Instanz statt zwei.
- **Namensschema:** `_DIDO`-Pendant heißt `_PWM` (SUB: `Button_PWM_OPC_UA`,
  VT-Projekt: `Workspace_PWM12` — `Workspace_PWM` war schon durch ein unabhängiges
  Einzelkanal-Showcase belegt).

## Stand / Checkliste

### Fertig ✅

- [x] `MyLib::sys::RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB` — Ein-Kanal-PWM-Composite
      (VT-Zahlenfeld+Balken+6 Ramp-Tasten, physischer `logiBUS_QD_PWM`-Ausgang,
      OPC-UA Publish/Subscribe), inkl. Fix der Mehrfachverbindungs-Meldung
- [x] `MyLib::sys::F_PWM_PERCENT_TO_RAW.SUB` / `F_PWM_RAW_TO_PERCENT.SUB`
- [x] `logiBUS::signalprocessing::fieldbus::F_PERCENT_TO_FRACTION.fbt` /
      `F_FRACTION_TO_PERCENT.fbt`
- [x] `Meins::InputOutputTester::Button_PWM_OPC_UA::SubStrings.gcf` (OPC-UA-Adressen
      für 12 PWM-Kanäle, Kategorie `PWM`)
- [x] `Meins::InputOutputTester::Button_PWM_OPC_UA::InputOutputTesterButton_PWM_OPC_UA.SUB`
      — Top-Level-Composite: 8 unveränderte Eingänge (`logiBUS_IXA_BG_OPC`) + 12×
      `RampLimitFS_TO_logiBUS_QDA_PWM_OPC` + `SystemTickSender` (21 Instanzen, 159
      Imports, cross-validiert gegen beide GCF-Dateien)
- [x] **Registrierung:** kein neues `Application`-Element nötig — dieses
      Trainingssystem hat genau EINEN `Control`-Slot pro `System`, der per
      "Change Type" (im 4diac IDE) auf den gewünschten Übungstyp umgeschaltet
      wird (so wurde jede Uebung_* in dieser Session auch getestet). Die PWM-
      Composite ist damit automatisch ein wählbares Ziel, ohne `test_AX.sys`
      strukturell zu ändern.
- [x] **VT-Objekte in `Workspace_PWM12`** — Container_Q (alte DIDO-Ausgabetasten)
      entfernt, 3 neue `CDataMask`-Seiten (`DataMask_PWM1/2/3`, 4 Kanäle/Seite) +
      `CSoftKeyMask` mit 4 Navigations-Softkeys (Eingänge/PWM1/PWM2/PWM3) gebaut.
      Pro Kanal: `CInputNumber` + `CRectangle`(Bargraph-PropertySheet, Vorlage aus
      `4diac_EasyExampleCounter`) + gemeinsame `CNumberVariable` + 6 `CButton`
      (0/--/-/+/++/F, Label-Objekte geteilt über CProxy). Validiert: wohlgeformt,
      keine doppelten IDs, keine hängenden Referenzen (256 Objekte, 4 `.jvi`-Dateien
      neu, `DataMask_M1.jvi` bereinigt + `SoftKeyMask=4000` gesetzt).
- [x] **GCF** `Uebungen::const::UT::PWM12::DefaultPool_PWM12.gcf` — von Hand
      erzeugt, aber Eins-zu-eins aus denselben IDs wie im echten `.jop` (150
      Konstanten, 100 % gegen die Pool-Objekte cross-validiert — kein
      "OutputNumber_Tick"-Risiko, da hier keine IOP-Binärmanipulation im Spiel war,
      sondern Pool und GCF im selben Zug konsistent erzeugt wurden).
- [x] **Web-Client `apixon-pwm-client`** — Kopie von `apixon-diodo-client`, 12
      Ausgänge als REAL-Slider+Zahlenfeld (0-100 %, Node-IDs `PWM_Q01..Q12`), 8
      Eingänge unverändert. Build + 5/5 Tests grün.
- [x] **Adressierungs-Konsistenz-Check** — SUB-`SubStrings.gcf`
      (`PWM_Q01_READ/WRITE`..), VT-Skalierung (`0.0015560939` = 100/64255) und
      Web-Client-Knoten-IDs (`ns=1;s=PWM_Q01..12`) stimmen überein.

### Gefunden beim Live-Test — behoben ✅ (Kanal-Schalter neu entworfen, PERMIT-frei)

- **`logiBUS_QD_PWM`-Anbindung des Kanal-Schalters entsprach NICHT dem
  Muster aus `Uebung_094a`, und die 7× `E_PERMIT`-Gates waren gar nicht
  verlangt** — beides vom Nutzer nach dem Live-Test explizit zurückgemeldet
  ("der QD_PWM Baustein ist mitnichten so angebunden wie in der Übung 094a";
  "irgendwie hast du mit PERMIT um dich geworfen, war nicht verlangt"; auf
  Nachfrage klargestellt: "nein, nicht 1 Permit war verlangt. Gar keines" —
  `Uebung_094a` ist explizit das Beispiel für "QI anstelle Permit", nicht nur
  ein weniger extremes PERMIT-Beispiel).
- **Neuentwurf in `RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB` (2026-08-28):**
  alle `E_PERMIT_*`-Gates entfernt, `Button_X.IND`/`F_SEL_PV.CNF` wieder
  direkt an `RampLimitFS` verdrahtet (wie vor dem Feature). Neu:
  `F_XOR_ENABLED` (`iec61131::bitwiseOperators::F_XOR`) berechnet
  `bEnabled = bDefaultEnabled XOR E_T_FF_SWITCH.Q` und speist
  `logiBUS_QD_PWM.QI` direkt als Datenverbindung (kein Parameter mehr) —
  exakt das `E_T_FF.Q -> DigitalInput_I1.QI`-Muster aus `Uebung_094a`, nur
  mit einem zwischengeschalteten XOR, weil `E_T_FF` selbst keinen
  Seed-Mechanismus für einen anderen Startwert als FALSE hat.
  `INIT_ENABLED.INITO` (einmalig beim Deployment) und `E_T_FF_SWITCH.EO`
  (bei jedem Toggle) stoßen `F_XOR_ENABLED.REQ` an; `F_XOR_ENABLED.CNF`
  feuert `logiBUS_QD_PWM.INIT`, damit der neue `QI`-Wert re-gelatcht wird
  (dessen `INIT`-With-Liste enthält `QI`). Validiert: wohlgeformt, keine
  verwaisten Verbindungsziele, `grep E_PERMIT` liefert 0 Treffer.

### Gefunden beim Live-Test (2026-08-29/30) — behoben ✅ (Kanal-Schalter, Runde 2)

- **`logiBUS_QD_PWM.QO` kam korrekt TRUE/FALSE, aber Status (Hintergrundfarbe/
  Web-UI) aktualisierte sich nicht zuverlässig.** Ursache (vom Nutzer selbst
  diagnostiziert): `logiBUS_QD_PWM` schickt bei `.INIT` nur `INITO`, nicht
  `CNF` — die Status-Kette hing nur am `.CNF` und wurde vom Umschalten des
  Kanal-Schalters nie ausgelöst. **Fix:** `logiBUS_QD_PWM.INITO` (dessen
  With-Liste ebenfalls `QO`/`STATUS` enthält, wie `.CNF`) speist jetzt
  zusätzlich `F_SEL_OK_FAULT.REQ`, `AX_BOOL_TO_X_SWITCH.REQ`,
  `AX_BOOL_TO_X_STATUS.REQ`.
- **`AX_SUBSCRIBE_SWITCH` empfing korrekt TRUE/FALSE, aber der Wert wurde
  nirgends verwendet — nur `AX_X_TO_BOOL_SWITCH.CNF` (reines "es wurde
  geschrieben"-Ereignis) togglete blind `E_T_FF_SWITCH.CLK`.** Nicht
  idempotent: zwei Schreibzugriffe mit demselben Wert togglen zweimal,
  Ergebnis "zufällig invertiert". **Fix:** `AX_X_TO_BOOL_SWITCH` (Typ
  `AX_X_TO_BOOL`) ersetzt durch `AX_RF_TRIG_SWITCH`
  (`adapter::events::unidirectional::AX_RF_TRIG`, IEC 61499 Annex A
  Rising/Falling-Edge-Trigger) — feuert `ER`/`EF` nur bei echter
  Wertänderung. `E_T_FF_SWITCH` (reines Toggle, kein Set/Reset, kein
  Seed-Mechanismus) ersetzt durch `E_T_FF_SR_SWITCH`
  (`iec61499::events::E_T_FF_SR_SYM_INIT`): `ER -> S`, `EF -> R` (externer
  Schreibzugriff setzt jetzt den tatsächlich geschriebenen Wert statt zu
  toggeln), `CLK` bleibt für den physischen VT-Taster (togglet weiterhin).
  `Q_INIT` wird direkt aus `bDefaultEnabled` gespeist — der bisherige
  `F_XOR_ENABLED`-Workaround (`bEnabled = bDefaultEnabled XOR Q`, nötig weil
  das alte `E_T_FF` immer bei FALSE startete) ist damit komplett entfallen,
  `logiBUS_QD_PWM.QI`/`F_SEL_STATUS.G` hängen jetzt direkt an
  `E_T_FF_SR_SWITCH.Q`.
- **Boot-Reihenfolge-Race gefunden und behoben:** `E_T_FF_SR_SWITCH.INIT`
  wurde zunächst von einem eigenen, parallel zur OPC-UA-Adapter-Bootstrap-
  Kette startenden `INIT_ENABLED` gefeuert. Race: der allererste
  Kanal-Enable-Zustand konnte den `AX_PUBLISH_SWITCH`-Adapter erreichen,
  bevor dessen eigene `.INIT`-Sequenz (`AR_SUBSCRIBE_1 -> AR_PUBLISH_1 ->
  AX_SUBSCRIBE_SWITCH -> AX_PUBLISH_SWITCH -> AX_PUBLISH_STATUS`, jeweils
  `.INITO -> .INIT` verkettet) fertig war — der Schreibversuch wurde dann
  vom noch nicht bereiten Adapter verworfen, der OPC-UA-Knoten blieb für
  Kanal 1-8 dauerhaft auf FALSE stehen. **Fix:** `E_T_FF_SR_SWITCH.INIT`
  wird jetzt vom Ende dieser bestehenden Adapter-Kette
  (`AX_PUBLISH_STATUS.INITO`) gefeuert statt von einem eigenen parallelen
  Trigger — garantiert, dass alle Adapter bereit sind, bevor der erste
  Enable-Zustand publiziert wird.
- Bestätigt durch den Nutzer per UA Expert/Web-UI: alle 12 Kanäle zeigen
  beim Deployment korrekt Enabled/Disabled (1-8 an, 9-12 aus), Kanal 9
  manuell aktiviert zeigt korrekt ROT (Kanal-Limit überschritten) auf
  ISOBUS UND Web-UI.

### Erweiterungen nach Live-Test — umgesetzt ✅

- **3-Farben-Status (WEISS/GRÜN/ROT) statt nur GRÜN/ROT:** ursprünglich nur
  `logiBUS_QD_PWM.QO` (ein einzelnes BOOL) für die Statusfarbe verwendet —
  kann WEISS (deaktiviert) nicht codieren. VT-seitig zweistufiges `F_SEL`
  (`F_SEL_OK_FAULT`: `QO` → ROT/GRÜN; `F_SEL_STATUS`: Enable-Zustand →
  WEISS oder Ergebnis von `F_SEL_OK_FAULT`). Web-UI kombiniert dieselben
  zwei bereits publizierten Bits (`PWM_Qnn_SWITCH`=enabled,
  `PWM_Qnn_STATUS`=QO) client-seitig zur selben 3-Farben-Logik, statt
  `STATUS` als einfaches An/Aus-LED zu behandeln — keine neue OPC-UA-Node
  nötig, da beide Bits schon publiziert wurden.
- **`Ramp6Buttons.SUB` extrahiert:** die 7 Taster (6 Ramp-Tasten + Kanal-
  Schalter) aus `RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB` in eine eigene
  wiederverwendbare SubApp ausgelagert, Event-Ausgänge/Input-Vars/FB-
  Reihenfolge an `RampLimitFS`s eigene Event-Reihenfolge angeglichen
  (`SWITCH, ZERO, UP_SLOW, UP_FAST, DOWN_SLOW, DOWN_FAST, FULL`).
- **OPC-UA-Adressraum verschachtelt:** von flachen Geschwister-Knoten
  (`/Objects/PWM/PWM_Q04`, `PWM_Q04_SWITCH`, `PWM_Q04_STATUS`) auf einen
  Ordner pro Kanal umgestellt (`/Objects/PWM/Q04/VALUE`, `/SWITCH`,
  `/STATUS`). Vorher in FORTEs `opcua_local_handler.cpp` geprüft: fehlende
  Zwischenordner werden automatisch als `FolderType`-Objekte angelegt, und
  die Node-ID (`s=PWM_Q04...`) ist vom Browse-Pfad unabhängig — Web-Client
  brauchte daher keine Änderung.
  Betrifft nur `test_AX`; `test_B` hat keine eigene PWM12-Instanz und ist
  daher nicht betroffen.
- **Web-Client responsive:** `.pwm-grid` hatte ein festes `repeat(2, 1fr)`,
  das bei schmalem Fenster nicht auf eine Spalte umgebrochen ist — stattdessen
  wurde der Regler (einziges schrumpfbares Element der Zeile) auf fast 0px
  gequetscht. Fix: `repeat(auto-fit, minmax(280px, 1fr))`.
- **Button-Overflow behoben:** `.pwm-item` als Grid-Zelle hatte
  `min-width: auto` (Standard), wodurch die fixen Breiten von Zahlenfeld/
  Schalter/LED die Spalte nach rechts aus der Karte drückten. Fix:
  `min-width: 0` auf `.pwm-item`.
- **10 zusätzliche Verbindungsstrings** (`Computers.gcf`, 5× 61499-Format
  `IP:61499`, 5× OPC-UA `opc.tcp://IP:4840`) — allgemeine Infrastruktur,
  nicht PWM12-spezifisch, aber im selben Zeitraum ergänzt.

### Gefunden beim Live-Test — behoben ✅

- **Wertebereich-Architektur — entschieden und umgesetzt:** `RampLimitFS.VAL_FULL`
  bleibt `64255` (J1939/`FIELDBUS_SIGNAL_W`-konform, VT-Anzeige und OPC-UA
  bleiben in diesem Bereich). Empirisch bestätigt (nicht geraten), dass
  `logiBUS_QD_PWM.OUT` einen rohen 13-bit-Wert (`0-8191`) erwartet: die
  echten, funktionierenden Beispiele `test_B/Uebungen/Uebung_034.SUB`
  (Analogeingang `F_SHL`-geshiftet direkt auf `PWMOutput_Q4.OUT`) und
  `Uebung_034a1_Q1.SUB` (VT-Variable `NumberVariable_PWM_Value` direkt,
  ohne jede Umrechnung, auf `PWMOutput_Q1.OUT`) belegen das. Fix in
  `RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB`: neue Kette
  `RampLimitFS.OUT →(×8191)→(÷64255)→ F_DINT_TO_DWORD_OUT → logiBUS_QD_PWM.OUT`
  (`F_MUL_TO_PWM13BIT`/`F_DIV_TO_PWM13BIT`, `iec61131::arithmetic`).
  Bargraph-`Min`/`Max` in `Workspace_PWM12` entsprechend von `0/100` auf
  `0/64255` korrigiert (alle 12 Kanäle) — muss exakt zum Prozent-/Rohwert-
  Eingabefeld passen, da alle drei dieselbe `CNumberVariable` teilen.
- **`logiBUS_QD_PWM` fehlt `TRUE` an `QI`** — behoben, Parameter ergänzt.
- **Zweites Eingabefeld (PWM-Rohwert)** — pro Kanal ergänzt
  (`InputNumberRaw_PWM_Q01..12`, `Scale=1`, `NoOfDecimals=0`, `0-64255`,
  teilt sich die `CNumberVariable` mit dem Prozent-Feld).
- **Listener-Bug (beide Eingabefelder reagierten nicht auf Tippen):**
  `NumericValue_Duty.u16ObjId` hing fälschlich am Objekt-ID des
  Prozent-**Feldes** (`u16ObjId_INPUT`) statt an der **Variable**
  (`u16ObjId_VALUEVAR`). Sobald ein Zahlenfeld eine Variable-Referenz hat,
  deaktiviert das VT laut ISO 11783-6 das Editier-Listening auf das
  Feld selbst und meldet Änderungen stattdessen über die Variable — bestätigt
  durch das echte, funktionierende `Uebung_034a1_Q1.SUB`
  (`PWM_Value.u16ObjId = NumberVariable_PWM_Value`, nicht das Feld). Fix
  macht beide Eingabefelder (Prozent + Rohwert) funktional, ohne dass das
  zweite Feld eine eigene FB-Verdrahtung braucht.
- **`E_RS_PV`-Event kam nicht durch, sobald einmal `S` gesetzt war** — behoben:
  `F_UDINT_TO_DINT_VT.CNF` und `F_PWM_PERCENT_TO_RAW.CNF` triggern
  `F_SEL_PV.REQ` jetzt zusätzlich direkt (nicht mehr nur über `E_RS_PV.EO`,
  das nur bei echtem `Q`-Zustandswechsel feuert), sodass jede Aktualisierung
  von jeder der beiden Quellen den Mux neu auswählen und laden lässt.
  Behebt auch das Symptom "Web→VT (Slider ziehen) hat keine Wirkung".

### Layout-Redesign — umgesetzt ✅ (VT-Kanalzeile)

Ursprünglich gefordert (Balkengrafik viel zu groß/vertikal, Spalten- statt
Zeilenlayout, Tasten nicht in `0 -- - + ++ F`-Reihenfolge, Schriftgröße
6×8/24×32 beide ungeeignet — siehe Screenshot-Bestätigung, `DataMask_PWM1.jvi`
4-Spalten-Ansicht mit überlappenden Zahlenfeldern). Jetzt umgesetzt in
`Workspace_PWM12`:

- **4 horizontale Zeilen** pro Seite (`DataMask_PWM1/2/3.jvi`, 3 Seiten),
  je eine Zeile pro Kanal: Label → Prozent-Feld → Rohwert-Feld →
  horizontaler Bargraph (90×28px, Ausrichtung folgt Width/Height-
  Seitenverhältnis, Vorlage aus `Workspace_PWM` Objekt 18000) → 6 Tasten in
  exakt der Reihenfolge `0 -- - + ++ F` links nach rechts (bestätigt:
  `Button_PWM_Q01_{ZERO,DOWN_FAST,DOWN_SLOW,UP_SLOW,UP_FAST,FULL}` in dieser
  Positions-Reihenfolge).
- **Schrift `FontAttributes_16x16`** (ID 23002) aus Krauternners Katalog
  importiert und auf Prozent-/Rohwert-Feld sowie Kanal-Labels angewendet
  (Kompromiss zwischen 6×8/24×32).
- 260→273 Objekte, GCF (163 Konstanten) 1:1 cross-validiert, keine
  Duplikate/hängenden Referenzen, jedes Text-Objekt hat ein Font.

### Bestätigt funktionierend ✅ (Live-Test)

- **Eingänge (I1-I8)** werden auf der VT korrekt angezeigt.
- **`AR_SUBSCRIBE_1` vom Web-Schieberegler her** funktioniert — ein Wert, der
  im Web-Client per Slider geschrieben wird, kommt im Composite an.

### Design-Entscheidungen (kein offener TODO, nur dokumentiert) ℹ️

- **RampLimitFS-Abhängigkeit ist bewusst extern** — referenziert
  `eclipse4diac::signalprocessing::RampLimitFS` (Nightly-Build), nicht ins
  Repo vendored. Mit dem Nutzer abgestimmt: eine spezifische IDE-Version mit
  diesem Baustein wird den Lernenden bereitgestellt. Keine offene Frage,
  bleibt so.

### Live-Test-Fortschritt (durch den Nutzer, laufend) 🧪

- **Reale Verifikation in ISO-Designer/4diac IDE** — läuft bereits und hat
  alle oben behobenen Bugs erst zutage gefördert (Build 0 Fehler/0 Warnungen,
  Eingänge zeigen korrekt an, `AR_SUBSCRIBE_1` vom Web-Slider funktioniert).
  Naturgemäß nur durch den Nutzer selbst am echten Gerät fortsetzbar, nicht
  durch mich automatisierbar — kein separater TODO, sondern der Prozess, in
  dem alle Punkte oben gefunden und nacheinander gefixt wurden.
- **`DataType.Float` für OPC-UA REAL im Web-Client — bestätigt, nicht mehr nur
  Annahme:** direkt im FORTE-Quellcode verifiziert
  (`C:\git2\ms\4diac-forte\com\opc_ua\src\opcua_helper.cpp`): `CIEC_REAL`
  (IEC 61499 32-bit `REAL`) mappt auf `UA_TYPES_FLOAT`, `CIEC_LREAL` (64-bit
  `LREAL`) auf `UA_TYPES_DOUBLE`. Die im Web-Client-Code hinterlassene
  Unsicherheits-Notiz kann raus.

## Kritische Dateien

- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/Ramp6Buttons.SUB` (die 7 Taster, ausgelagert)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/F_PWM_PERCENT_TO_RAW.SUB` / `F_PWM_RAW_TO_PERCENT.SUB`
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/signalprocessing/fieldbus/F_PERCENT_TO_FRACTION.fbt` / `F_FRACTION_TO_PERCENT.fbt`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_PWM_OPC_UA/SubStrings.gcf`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_PWM_OPC_UA/InputOutputTesterButton_PWM_OPC_UA.SUB`
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_PWM12/DefaultPool/DefaultPool.jop`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`
- `Ventilsteuerung/Web-Clients/apixon-pwm-client/src/ApixonPWM.vue` (Kopie von `apixon-diodo-client` als Vorlage)
- `Ventilsteuerung/boot-files/test_AX_FORTE_PC_AX.fboot` (generiert — nicht von Hand editieren, nach jeder Adressraum-/Namensänderung über die IDE neu erzeugen)
