# Plan: PWM-Trainingsbeispiel (12 Kanäle)

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
- [x] `Workspace_PWM12` als Kopie von `Workspace_DIDO` angelegt (nur Umbenennung,
      **noch keine PWM-VT-Objekte**)

### Offen ❌

1. **`Meins::InputOutputTester::Button_PWM_OPC_UA::InputOutputTesterButton_PWM_OPC_UA.SUB`**
   — Top-Level-Composite: 8 unveränderte Eingänge (`logiBUS_IXA_BG_OPC`) + 12×
   `RampLimitFS_TO_logiBUS_QDA_PWM_OPC` + `SystemTickSender`. Noch nicht gebaut.
2. **Registrierung in `test_AX.sys`** — neue `Application`/`SubApp`-Zuordnung
   (eigene Application, nicht `App_AX` wiederverwenden, damit DIDO/PWM unabhängig
   testbar bleiben).
3. **VT-Objekte in `Workspace_PWM12`** (größter offener Punkt): 3 neue
   `CDataMask`-Seiten (4 Kanäle/Seite), pro Kanal `CInputNumber` + `CRectangle`
   (Bargraph-PropertySheet) + gemeinsame `CNumberVariable` + 6 `CButton`
   (0/--/-/+/++/F), `CSoftKeyMask` mit 3 Navigations-Softkeys
   (`isobus::UT::io::Softkey::Softkey_IE` → `isobus::UT::Q::Q_ActiveMask`, Muster
   aus `test_B/Uebungen/Uebung_019b.SUB`). ID-Bereiche siehe ursprünglicher Plan.
4. **GCF-Regenerierung** `Uebungen::const::UT::PWM12::DefaultPool_PWM12.gcf` — erst
   nach Punkt 3 möglich (wird aus dem echten `.jop` generiert, nicht von Hand
   vorgeschrieben — siehe Lehre aus `OutputNumber_Tick` im DIDO-Beispiel).
5. **Web-Client `apixon-pwm-client`** — Kopie von `apixon-diodo-client`, 12
   Ausgänge als REAL-Slider/Zahlenfeld (0-100 %) statt Bool-Toggle, 8 Eingänge
   unverändert. `DataType.Float` vs `Double` für OPC-UA REAL empirisch prüfen,
   nicht annehmen.
6. **Adressierungs-Konsistenz-Check** — SUB-`SubStrings.gcf`, VT-Skalierung und
   Web-Client-Knoten-ID-Strings müssen am Ende übereinstimmen.

## Kritische Dateien

- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/F_PWM_PERCENT_TO_RAW.SUB` / `F_PWM_RAW_TO_PERCENT.SUB`
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/signalprocessing/fieldbus/F_PERCENT_TO_FRACTION.fbt` / `F_FRACTION_TO_PERCENT.fbt`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_PWM_OPC_UA/SubStrings.gcf`
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_PWM12/DefaultPool/DefaultPool.jop`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`
- `Ventilsteuerung/apixon-diodo-client/` (Vorlage für `apixon-pwm-client`)
