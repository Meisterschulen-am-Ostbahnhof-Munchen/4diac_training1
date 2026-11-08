# Plan: AI-Trainingsbeispiel (8 Analog-Eingänge)

## Ausgangslage

Analog zum bestehenden DIDO-Trainingsbeispiel (`Meins::InputOutputTester::Button_DIDO_OPC_UA` /
`Workspace_DIDO` / `apixon-diodo-client`) soll ein drittes, paralleles Beispiel entstehen:
**die 8 digitalen Eingänge werden durch 8 Analog-Eingänge ersetzt, die 12 digitalen
Ausgänge bleiben unverändert** (exakt dieselbe Verdrahtung/Bausteine wie in DIDO,
nicht anfassen).

Namensschema (dritte Variante nach `_DIDO`/`_PWM`): **`_AI`**
(`Button_AI_OPC_UA`, `Workspace_AI` — Name frei, geprüft), Web-Client
`apixon-ai-client`.

## Vorarbeit (bereits erledigt)

- **Roh-Vollausschlag von `logiBUS_AI_ID.IN`/`logiBUS_AI_IDA.IN` bestätigt:**
  `0-4095` (12 bit, fix, kein Konfigurationsspielraum im ESP32-P4-Continuous-
  Mode) — siehe `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/io/AI/logiBUS_AI_TODO.md`.
  Bereits im Baustein-Kommentar und in der Hardware-Doku
  (`APIXON_Node-ISO_20.md`, DE+EN) nachgetragen.
- **Analog-Eingänge sind alle Combo-Pins** mit den gleichnamigen digitalen
  Eingängen (I1↔AnalogInput_I1 usw.), 7× ADC1 + `AnalogInput_I3` allein auf
  ADC2 (unproblematisch auf diesem WLAN-losen Chip).
- **Konstanten existieren bereits:** `logiBUS::io::AI::logiBUS_AI.gcf` →
  `AnalogInput_I1..I9`, `Invalid` (jeweils `logiBUS_AI_S := (Pin := N)`).

## Architektur-Entscheidungen (mit Nutzer abgestimmt)

- **Wertdarstellung:** sowohl **Rohwert (0-4095)** als auch **Prozent
  (0.0-100.0 % REAL)** anzeigen — beide, nicht nur eins. Eine spätere
  Kalibrierfunktion (physikalische Sensor-Grenzen, z.B. 0°C/100°C) ist
  explizit **Schritt 2**, jetzt noch nicht bauen.
- **VT-/Web-Darstellung pro Kanal:** `COutputNumber` (nicht `CInputNumber` —
  rein lesend, nichts editierbar) für Rohwert UND Prozent, plus Bargraph
  (Prozent-gesteuert). Platz für die künftige Kalibrierung reservieren —
  laut Nutzer **braucht eine Kanalzeile etwa doppelt so viel Platz wie eine
  PWM-Ausgangszeile** (die hatte 6 Tasten, die hier komplett entfallen, aber
  2 Zahlenfelder statt 1 plus reservierter Platz gleichen das mehr als aus).
- **OPC-UA-Adressraum von Anfang an verschachtelt** (Lehre aus dem
  PWM-Sample, das erst flach gebaut und später umgestellt werden musste):
  `/Objects/Analog/I1/RAW`, `/Objects/Analog/I1/PERCENT` (analog zu PWM12s
  finaler `/Objects/PWM/Q04/VALUE|SWITCH|STATUS`-Struktur). Node-IDs bleiben
  flach (`s=AI_I1_RAW`, `s=AI_I1_PERCENT` o.ä.), da Node-ID und Browse-Pfad
  laut FORTE-Quellcode (`opcua_local_handler.cpp`) unabhängig sind.
- **DO-Seite unverändert:** dieselben `Button_IXA_TO_logiBUS_QXA_BG_OPC`-
  Instanzen wie in DIDO, 1:1 aus DIDOs Composite übernommen, keine
  Änderung an deren Verdrahtung.
- **Poll-Parameter (`logiBUS_AI_ID`):** Defaults der FB übernehmen
  (`TimeDelta=250ms`, `TimeRateLimit=100ms`, `AnalogInput_hysteresis=0`),
  sofern nicht anders gewünscht — reine Dauerpoll-Anzeige, keine
  Schwellwert-Logik in diesem Schritt.

## Offene Fragen — beantwortet ✅

1. **Skalierungs-Baustein:** ja, eigene SubApp (`F_AI_RAW_TO_PERCENT.SUB`) —
   gebaut, dazu spaeter auch eine volladapterbasierte Parallel-Variante
   (`F_AI_RAW_TO_PERCENT_AD.SUB`, siehe unten).
2. **ID-Bereiche/Kanaele pro Seite:** 2 Zeilen/Seite, also 4 Seiten (2
   Kanaele je Seite) — umgesetzt.
3. **Seitenlayout:** wie bei PWM — 1. Seite identisch (hier: die
   unveraenderte Ausgaenge-Seite aus DIDO, `Container_Q`/`Button_Q01-12`),
   dann 4 neue Seiten fuer die 8 Analog-Kanaele angehaengt.

## Stand / Checkliste

### Fertig ✅

- [x] `MyLib::sys::F_AI_RAW_TO_PERCENT.SUB` — Rohwert (DWORD 0-4095) linear
      in Prozent (REAL 0.0-100.0) via `F_DWORD_TO_UDINT`→`F_UDINT_TO_REAL`→
      `F_MUL` (Faktor `100/4095=0.0244200244`).
- [x] `MyLib::sys::F_AI_RAW_TO_PERCENT_AD.SUB` — volladapterbasierte
      Parallel-Variante (gleiches Ergebnis, `AD_TO_AUDI`→`AUDI_TO_AR`→
      `AR_MUL_2`+`initval_AR` statt Daten-FBs mit expliziter REQ/CNF-Kette).
      **Wichtiger Fund dabei:** `AD_TO_AR` (der naheliegende 1-Schritt-Weg)
      ist eine Bit-Reinterpretation, keine numerische Umwandlung — verifiziert
      im echten FORTE-Quellcode (`forte_real.cpp`, `CIEC_REAL::setValue`,
      Case `e_DWORD`). Dokumentiert in
      `Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/conversion/unidirectional/AD_AR/AD_TO_AR_TODO.md`
      inkl. Querverweis auf 7 bereits existierende `Uebung_028*_AR`-Uebungen,
      die dieselbe Falle schon dokumentiert hatten (nicht neu entdeckt).
- [x] `MyLib::sys::logiBUS_AI_IDA_OPC.SUB` — Ein-Kanal-Analog-Composite:
      `logiBUS_AI_IDA` liest Rohwert per Adapter, `AD_SPLIT_2`/`_3` verteilt
      auf OPC-UA-Rohwert-Publish (`AD_PUBLISH_1`), VT-Anzeige
      (`Q_NumericValue`/`Q_NumericValue_AUDI`) und Prozent-Berechnung
      (`F_AI_RAW_TO_PERCENT`) → `AR_PUBLISH_1` fuer OPC-UA-Prozent.
- [x] `Meins::InputOutputTester::Button_AI_OPC_UA::InputOutputTesterButton_AI_OPC_UA.SUB`
      — Top-Level-Composite: 8× `logiBUS_AI_IDA_OPC` + 12× unveraenderte
      `Button_IXA_TO_logiBUS_QXA_BG_OPC`-Ausgaenge (1:1 aus DIDO) +
      `SystemTickSender`. Validiert: alle Imports/Parameter/SubApp-Typen
      loesen auf.
- [x] `SubStrings.gcf` fuer `Button_AI_OPC_UA` — verschachtelte OPC-UA-
      Adressen (`/Objects/Analog/I1/RAW`, `/PERCENT`, ... `I8`), unveraenderte
      Digital-Ausgangs-Adressen 1:1 aus DIDO.
- [x] VT-Projekt `Workspace_AI` — Kopie von `Workspace_DIDO`: `Container_I`
      entfernt, `Container_Q`/`Button_Q01-12` unveraendert. Neu:
      `CSoftKeyMask` + 5 Softkeys (Ausgaenge, AI1-2/AI3-4/AI5-6/AI7-8 —
      Beschriftung nach Kanal-Bereich pro Seite benannt, nicht nach
      Seitennummer, um Verwechslung zu vermeiden), 4 neue `CDataMask`-Seiten
      (2 Kanaele/Seite). Pro Kanal: Label + Rohwert-`COutputNumber` +
      Prozent-`COutputNumber` (teilen sich eine `CNumberVariable`,
      Scale=1 bzw. 0.0244200244) + Bargraph (`CRectangle`, Min=0/Max=4095,
      LinearBargraph-ID-Block 18000 statt PWM12s Rectangle-Block 14000 —
      bewusste Abweichung, folgt der offiziellen ID-Konvention). Validiert:
      wohlgeformt, 0 doppelte JVS-IDs, 0 haengende Referenzen, alle Text-
      Objekte haben einen Font, GCF-IDs 1:1 gegen den echten Pool geprueft.
- [x] GCF `Uebungen::const::UT::AI::DefaultPool_AI.gcf` — 1:1 aus den echten
      `.jop`-Objekt-IDs erzeugt (39 Konstanten, cross-validiert).
- [x] Web-Client `apixon-ai-client` — Kopie von `apixon-diodo-client`,
      Eingaenge-Sektion durch 8× (Rohwert+Prozent+Mini-Bargraph, rein
      lesend) ersetzt, Ausgaenge-Sektion unveraendert. Build + 5/5 Tests
      gruen, `vue-tsc` sauber, visuell im Browser geprueft (auch bei
      schmalem Viewport, responsive ohne Overflow).

### Noch offen

- [ ] Registrierung in `test_AX.sys` — noch nicht angefasst (aktuell auf
      die PWM-Composite verdrahtet), `Change Type`-Mechanismus wie bei PWM
      erwartet, kein neues `Application`-Element noetig.
- [ ] Entscheidung: `logiBUS_AI_IDA_OPC.SUB` mit der daten- oder der
      adapterbasierten Prozent-Variante final verdrahten (aktuell nutzt die
      SUB `F_AI_RAW_TO_PERCENT` [Daten], `F_AI_RAW_TO_PERCENT_AD` liegt als
      gleichwertige Alternative daneben).
- [ ] Live-Test durch den Nutzer (ich kann das nicht automatisieren).
- [ ] Committen (aktuell nur `logiBUS_AI_TODO.md`, `AD_TO_AR_TODO.md` und
      dieser Plan sind committed — der eigentliche Sample-Code liegt noch
      unstaged, wartet auf dein Go).

## Kritische Dateien

- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_DIDO_OPC_UA/InputOutputTesterButton_DIDO_OPC_UA.SUB` (Vorlage)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/logiBUS_IXA_BG_OPC.SUB` (digitales Vorbild für die neue Analog-Variante)
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/io/AI/logiBUS_AI_ID.fbt` / `logiBUS_AI_IDA.fbt` / `logiBUS_AI.gcf`
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/io/AI/logiBUS_AI_TODO.md`
- `Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/conversion/unidirectional/AD_AR/AD_TO_AR_TODO.md`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/F_AI_RAW_TO_PERCENT.SUB` / `F_AI_RAW_TO_PERCENT_AD.SUB`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/logiBUS_AI_IDA_OPC.SUB`
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_DIDO/DefaultPool/DefaultPool.jop` (Vorlage)
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_AI/DefaultPool/DefaultPool.jop`
- `Ventilsteuerung/Web-Clients/apixon-diodo-client/` (Vorlage für `apixon-ai-client`)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`
