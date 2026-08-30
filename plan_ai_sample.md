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

## Offene Fragen (vor dem Bauen zu klären)

1. **Skalierungs-Baustein:** neue kleine SubApp/FB `MyLib::sys::F_AI_RAW_TO_PERCENT`
   bauen (`percent = raw / 4095 * 100`, analog zu `F_PWM_RAW_TO_PERCENT`),
   oder reicht eine Inline-Verdrahtung mit Standard-`iec61131::arithmetic`-
   Funktionen direkt im Kanal-Composite? (Ich tendiere zu einer eigenen
   SubApp, für Konsistenz mit dem PWM-Sample-Stil — aber sag Bescheid, falls
   das für nur eine Formel zu viel Bürokratie ist.)
2. **ID-Bereiche für die neuen VT-Objekte** (`Workspace_AI`): da eine
   AI-Kanalzeile doppelt so breit wird wie eine PWM-Zeile, passen vermutlich
   nur 2 Kanäle nebeneinander/pro Seite statt 4 wie bei PWM12 — wie viele
   Seiten/Layout genau, entscheide ich beim Bauen, es sei denn du hast schon
   eine konkrete Vorstellung.
3. **Seitenlayout:** volle 12-Ausgänge-Seite(n) unverändert aus DIDO
   übernehmen, plus neue Analog-Seite(n) — oder eine gemischte Seite pro
   Blick (Eingänge+Ausgänge zusammen wie DIDO es evtl. schon macht)? Ich
   schaue mir DIDOs tatsächliches Seitenlayout nochmal genau an, bevor ich
   das für AI übernehme.

## Stand / Checkliste

### TODO

- [ ] `MyLib::sys::logiBUS_AI_ID_BG_OPC.SUB` (oder ähnlicher Name) — Ein-
      Kanal-Analog-Composite: `logiBUS_AI_ID` liest Rohwert, Skalierung auf
      Prozent, beide Werte via OPC-UA publizieren (`AR_PUBLISH_1`-Paar oder
      neuer BOOL/DWORD-Adapter-Pfad, je nach Datentyp), VT-Anzeige
      (`COutputNumber`×2 + Bargraph) aktualisieren.
- [ ] `MyLib::sys::F_AI_RAW_TO_PERCENT.SUB` (falls Frage 1 mit "eigene
      SubApp" beantwortet wird).
- [ ] `Meins::InputOutputTester::Button_AI_OPC_UA::InputOutputTesterButton_AI_OPC_UA.SUB`
      — Top-Level-Composite: 8× neue Analog-Kanäle + 12× unveränderte
      `Button_IXA_TO_logiBUS_QXA_BG_OPC`-Ausgänge (1:1 aus DIDO) +
      `SystemTickSender`.
- [ ] `SubStrings.gcf` für `Button_AI_OPC_UA` — verschachtelte OPC-UA-
      Adressen für 8 Analog-Kanäle (`/Objects/Analog/I1/RAW`, `/PERCENT`),
      unveränderte Digital-Ausgangs-Adressen aus DIDO übernehmen.
- [ ] VT-Projekt `Workspace_AI` — Kopie von `Workspace_DIDO`, Eingänge-
      Container durch neue Analog-Anzeige-Zeilen ersetzen, Ausgänge-
      Container unverändert übernehmen.
- [ ] GCF `Uebungen::const::UT::AI::DefaultPool_AI.gcf` (oder passender
      Name) — 1:1 aus den echten `.jop`-Objekt-IDs erzeugt.
- [ ] Web-Client `apixon-ai-client` — Kopie von `apixon-diodo-client`,
      Eingänge-Sektion durch 8× (Rohwert+Prozent+Bargraph) ersetzen,
      Ausgänge-Sektion unverändert.
- [ ] Registrierung in `test_AX.sys` prüfen (`Change Type`-Mechanismus wie
      bei PWM — vermutlich kein neues `Application`-Element nötig).
- [ ] Adressierungs-Konsistenz-Check (SUB-`SubStrings.gcf` ↔ VT-Skalierung
      ↔ Web-Client-Knoten-IDs).
- [ ] Live-Test durch den Nutzer (ich kann das nicht automatisieren).

## Kritische Dateien

- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_DIDO_OPC_UA/InputOutputTesterButton_DIDO_OPC_UA.SUB` (Vorlage)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/logiBUS_IXA_BG_OPC.SUB` (digitales Vorbild für die neue Analog-Variante)
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/io/AI/logiBUS_AI_ID.fbt` / `logiBUS_AI_IDA.fbt` / `logiBUS_AI.gcf`
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/io/AI/logiBUS_AI_TODO.md`
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_DIDO/DefaultPool/DefaultPool.jop` (Vorlage)
- `Ventilsteuerung/Web-Clients/apixon-diodo-client/` (Vorlage für `apixon-ai-client`)
- `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`
