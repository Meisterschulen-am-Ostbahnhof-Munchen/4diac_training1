# Plan: PI-Trainingsbeispiel (8 Puls-Eingänge / Frequenzmessung)

## Ausgangslage

Analog zum bestehenden AI-Trainingsbeispiel (`Meins::InputOutputTester::Button_AI_OPC_UA` /
`Workspace_AI` / `apixon-ai-client`, gemergt in `develop` via PR #149) soll ein viertes,
paralleles Beispiel entstehen: **die 8 Analog-Eingänge werden durch 8 Puls-Eingänge
(Frequenzmessung) ersetzt, die 12 digitalen Ausgänge bleiben unverändert.**

Nutzervorgabe: *"die Oberfläche können wir FAST so lassen, mach eine Kopie"* — AI ist die
Kopiervorlage (nicht DIDO), weil die 8-Eingänge-Varianten-Struktur, das softkey-paginierte
VT-Layout (2 Kanäle/Seite, 4 Seiten) und das Oszilloskop-Web-Widget der näherliegende
Ausgangspunkt sind.

Namensschema (vierte Variante nach `_DIDO`/`_PWM`/`_AI`): **`_PI`** — `Button_PI_OPC_UA`,
`Workspace_PI`, Web-Client `apixon-pi-client`. Geprüft, kollisionsfrei (keiner der drei
Namen existiert bereits im Repo).

**Branch:** `feature/PI-Sample` (bereits von `develop` abgezweigt und ausgecheckt, sauber,
identisch zu `develop`/`origin/develop`).

## Vorarbeit (recherchiert und verifiziert, nicht geraten)

- **`logiBUS::io::PI::logiBUS_PI_ID`/`logiBUS_PI_IDA`** (`.lib/logiBUS-3.0.0/typelib/io/PI/`)
  sind strukturell ein 1:1-Gegenstück zu `logiBUS_AI_ID`/`logiBUS_AI_IDA`: gleiches
  INIT/REQ/IND/CNF-Eventschema, `Input:logiBUS::io::PI::logiBUS_PI_S` (Konstanten
  `PulseInput_I1..I9`+`Invalid`). Poll-Parameter: `ImpulseDelta:DWORD` (statt
  `AnalogInput_hysteresis`), `TimeDelta:DWORD`, `TimeRateLimit:DWORD`.
- **`IN:DWORD` ist ein roher, monoton akkumulierender Impulszähler** — kein eingebauter
  Frequenz-Ausgang. Reale FORTE-Hardware-Anbindung
  (`C:\git\hr\LOGIBUS_integration_datapanel\4diac-forte\logiBUS-modules\logiBUS-io\handle\esp32_pulse_in\IOHandleESP32PulseIN.cpp`)
  nutzt die ESP32-PCNT-Hardware, liest denselben Pin über dieselbe `EPinDigitalIn`-GPIO-
  Tabelle wie die digitalen Eingänge (Combo-Pin-Wiederverwendung). Hardware-Doku
  (`APIXON_Node-ISO_20.md`) dokumentiert bislang keinen Pulse-Input-Abschnitt — Doku-Lücke,
  analog zum `logiBUS_AI_TODO.md`-Muster, kein Blocker.
- **Frequenz-Ableitung, verifiziert:** `logiBUS_PI_ID.IN` (DWORD) → `AD_TO_AR_NUM`
  (DWORD-Adapter → REAL-Adapter, numerisch korrekt — direkt gelesen, intern
  `F_DWORD_TO_UDINT`→`F_UDINT_TO_REAL`, keine Bit-Reinterpretation) → OSCAT `FT_DERIV`
  (`.lib/OSCAT/typelib/Basic/POUs/Engineering/Control/FT_DERIV.fbt`, gelesen: Zeittaktung
  intern über `T_PLC_US()`, kein externer Zeit-Input nötig; Formel
  `out := delta_in/delta_t_us*1e6*K`). **Bei `K=1.0` ist der Output bereits Hz** (Impulse/
  Sekunde) — kein zusätzlicher Skalierungsfaktor nötig. Getriggert wird `FT_DERIV.REQ` durch
  dieselbe Event-Kette, die aus `logiBUS_PI_ID.IND`/`.CNF` kommt (bestätigtes Muster aus
  `Uebung_151_AX.SUB`/`test_B/Uebung_151.SUB`).
- **`AD_TO_AR_NUM` geprüft und verwendet** (statt AI's zweistufiger
  `AD_TO_AUDI`→`AUDI_TO_AR`-Verdrahtung): `.fbt`-Datei selbst gelesen, `FBNetwork` ist exakt
  `F_DWORD_TO_UDINT`→`F_UDINT_TO_REAL`, bit-identisch zur bewährten Kette, nur als ein
  Composite-Baustein. Spart einen Verdrahtungsschritt gegenüber dem AI-Muster.

## Architektur-Entscheidungen (mit Nutzer abgestimmt)

- **Wertdarstellung:** Oszilloskop zeigt **nur Frequenz** über Zeit (0-100 Hz Y-Achse) —
  AI's rollierendes Canvas-Widget wiederverwenden. Genau **zwei** Zahlenfelder pro Kanal:
  **Frequenz (Hz)** und **Zähler** (roher, akkumulierender Impulszählwert) — beide für sich
  aussagekräftig (anders als AI's Rohwert/Prozent, die dieselbe Größe nur umskaliert
  zeigten). Bargraph zeigt **nur Frequenz**, skaliert **0-100 Hz**. Zähler read-only, kein
  Reset (nicht angefragt, `logiBUS_PI_ID` bietet auch keinen).
- **KEINE geteilte `CNumberVariable`:** anders als bei AI (Rohwert/Prozent sind reine
  Reskalierungen derselben Zahl, eine `CNumberVariable` reicht) sind Frequenz und Zähler bei
  PI **keine proportionalen Versionen derselben Zahl** (Frequenz ist die zeitliche Ableitung
  des Zählers). **PI braucht pro Kanal zwei echte, unabhängige `CNumberVariable`n** → 16
  GCF-Konstanten statt AI's 8 (`NumberVariable_PI_FREQ_I01..08`,
  `NumberVariable_PI_COUNT_I01..08`).
- **VT-Feldbreite Zähler:** AI's Rohwert-Feld brauchte nur 4 Ziffern (0-4095). PI's Zähler
  ist ein unbegrenzt wachsendes DWORD — Zähler-`COutputNumber` mit **≥8-10 Ziffern**
  auslegen, nicht AI's schmales 4-stelliges Feld kopieren.
- **Poll-Parameter (mit Nutzer abgestimmt):** `ImpulseDelta=100` (löst zusätzlich zur
  Zeit-Poll-Rate alle 100 Impulse ein IND aus — bewusst UNGLEICH AI's `hysteresis=0`),
  `TimeDelta=250`, `TimeRateLimit=100`.
- **FT_DERIV:** einfaches `FT_DERIV` (nicht `FT_DERIV_10`), `K=1.0`, keine Glättung.
- **`test_AX.sys`:** Control-Slot wird beim Bauen sofort auf `Button_PI_OPC_UA` umgeschaltet
  (wie beim AI-Sample), fürs direkte Live-Testen.
- **OPC-UA-Adressschema** (verschachtelt von Anfang an, Lehre aus AI/PWM):
  `/Objects/Pulse/I{n}/FREQ` (REAL, Hz), `/Objects/Pulse/I{n}/COUNT` (DWORD, roh).
  Node-IDs flach: `s=PI_I{n}_FREQ`, `s=PI_I{n}_COUNT`.

## Per-Kanal-Composite: `MyLib::sys::logiBUS_PI_IDA_OPC.SUB`

```
logiBUS_PI_IDA (Input:logiBUS_PI_S, ImpulseDelta=100, TimeDelta=250, TimeRateLimit=100)
  └─ .IN (AD-Adapter, DWORD, roher Zähler) → AD_SPLIT_2/_3
       ├─ OUT1 → AD_PUBLISH_1 → OPC-UA "COUNT" (roh, DWORD)
       ├─ OUT2 → AD_TO_AUDI → Q_NumericValue_AUDI (VT-Zahlenfeld "Zähler", eigene CNumberVariable)
       └─ OUT3 → AD_TO_AR_NUM → REAL
                     └─ FT_DERIV (K=1.0, run=TRUE) → REAL (Hz)
                          ├─ → AR_PUBLISH_1 → OPC-UA "FREQ" (REAL, Hz)
                          └─ → Q_NumericValue (VT-Zahlenfeld "Frequenz", eigene CNumberVariable)
```

`FT_DERIV.REQ` wird von derselben Kette gespeist wie `AD_TO_AR_NUM`s Event (letztlich aus
`logiBUS_PI_IDA.IN.E1`), nicht von einem eigenen Zyklus-Timer — sonst rechnet `FT_DERIV`
mit veralteten Werten. Zwei separate `Q_NumericValue`/`Q_NumericValue_AUDI`-Instanzen (nicht
eine gemeinsame wie bei AI), da zwei unabhängige `CNumberVariable`-IDs gebunden werden.

## Stand / Checkliste

### TODO

- [ ] `MyLib::sys::logiBUS_PI_IDA_OPC.SUB` bauen (Design oben).
- [ ] `Meins::InputOutputTester::Button_PI_OPC_UA::InputOutputTesterButton_PI_OPC_UA.SUB` +
      `SubStrings.gcf` — 8× `logiBUS_PI_IDA_OPC` (Input=`PulseInput_I1..I8`) + 12×
      unveränderte `Button_IXA_TO_logiBUS_QXA_BG_OPC` (1:1 aus AI/DIDO) + `SystemTickSender`.
- [ ] `Uebungen::const::UT::PI::DefaultPool_PI.gcf` — 1:1 aus dem echten `.jop`-Pool erzeugt,
      16 `NumberVariable_PI_*`-Konstanten statt AI's 8.
- [ ] `Ventilsteuerung/ISO-DesignerProjects/Workspace_PI/` — Kopie von `Workspace_AI`:
      `DataMask_M1`/`Container_Q`/`Button_Q01-12` unverändert, `CSoftKeyMask` mit 5 Softkeys
      ("Ausgänge" + "PI1-2"/"PI3-4"/"PI5-6"/"PI7-8" — Beschriftung nach Kanal-Bereich, nicht
      Seitennummer, dieselbe Lehre aus AI). Pro Kanal: Label + Frequenz-`COutputNumber`
      (eigene CNumberVariable) + Zähler-`COutputNumber` (eigene CNumberVariable, breiteres
      Feld) + Bargraph (Min=0/Max=100, Frequenz-CNumberVariable). `iso-designer-jop`-Skill
      vor jeder `.jop`/`.jvi`-Bearbeitung laden.
- [ ] `apixon-pi-client` — Kopie von `apixon-ai-client`: Subscriptions auf
      `PI_I{n}_FREQ`/`PI_I{n}_COUNT` statt `AI_I{n}_RAW`/`AI_I{n}_PERCENT`, zweite
      Zahlenanzeige wird Zähler (ganzzahlig, kein `toFixed`), Oszilloskop-Beschriftung von
      "%" auf "Hz" (Zeichen-Mathematik bleibt unverändert — der bestehende `/100`-Divisor
      passt zufällig exakt auf den bestätigten 0-100-Hz-Bereich), `sampleIntervalMs`-Anzeige
      unverändert übernehmen.
- [ ] `test_AX.sys` — Control-Slot auf `Button_PI_OPC_UA` umschalten.
- [ ] Optional: `logiBUS_PI_TODO.md` (Doku-Lücke Hardware-Doku, analog `logiBUS_AI_TODO.md`).
- [ ] Adressierungs-Konsistenz-Check (SUB-`SubStrings.gcf` ↔ VT-Objekt-IDs ↔ Web-Client).
- [ ] Live-Test durch den Nutzer.

## Kritische Dateien

- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/logiBUS_AI_IDA_OPC.SUB` (Vorlage)
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/io/PI/logiBUS_PI_IDA.fbt` / `logiBUS_PI_ID.fbt` / `logiBUS_PI.gcf`
- `Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/conversion/unidirectional/AD_AR/AD_TO_AR_NUM.fbt`
- `Ventilsteuerung/4diacIDE-workspace/.lib/OSCAT/typelib/Basic/POUs/Engineering/Control/FT_DERIV.fbt`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Uebungen/Uebung_151_AX.SUB` (Referenz-Verdrahtung Zähler→REAL→FT_DERIV)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_AI_OPC_UA/InputOutputTesterButton_AI_OPC_UA.SUB` + `SubStrings.gcf` (Vorlage Top-Level)
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_AI/DefaultPool/DefaultPool.jop` (Vorlage VT-Pool)
- `Ventilsteuerung/Web-Clients/apixon-ai-client/src/ApixonAI.vue` (Vorlage Web-Client)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`
