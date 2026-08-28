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

### Gefunden beim Live-Test (noch zu fixen) 🔴

- **Wertebereich-Architektur (Entscheidung noch am Reifen, Stand aktuell):**
  Erst-Idee war, `RampLimitFS.VAL_FULL` von `64255` auf `8191` zu ändern
  (weil Bargraph/CInputNumber im Test mit `0-8191` funktionierten, wie im
  Referenzprojekt `Workspace_PWM`, Objekt 18000: `Min=0`/`Max=8191`).
  **Korrigierte Richtung:** `RampLimitFS.VAL_FULL` bleibt `64255` — das ist
  die korrekte J1939/ISO-11783-Konvention für ein 16-bit-Signal
  (`VALID_SIGNAL_W = 0x0000-0xFAFF = 0-64255`, alles darüber wird laut
  Protokoll ignoriert/ist reserviert; Quelle:
  `C:\4diac\4diac-ide_3.3.0-win32.win32.x86_64_nightly_2026-08-26_2003_sp10\4diac-ide\typelibrary\signalprocessing-3.0.0\typelib\FIELDBUS_SIGNAL.gcf`).
  Stattdessen kommt **eine zusätzliche Skalierungsstufe vor `logiBUS_QD_PWM`**
  hinzu, die von `64255` auf den vom PWM-Ausgang tatsächlich erwarteten
  Rohwertbereich (vermutlich `8191`, wie in `Workspace_PWM`) umrechnet.
  Damit bleibt der Netzwerk-/RampLimitFS-Wert J1939-konform, und nur die
  letzte Stufe vor der Hardware bekommt die geräteeigene Skalierung.
  **Noch offen:** wie genau sich das zur VT-Anzeige (Bargraph/CInputNumber,
  aktuell mit `Min=0`/`Max=8191`/`Scale=0.01220852` getestet) verhält — ob
  die VT-Anzeige direkt am `64255`er RampLimitFS-Wert hängt (dann bräuchte
  *sie* auch eine eigene 64255→8191-Umrechnung vor der Anzeige) oder ob sie
  ohnehin schon über eine eigene Konvertierungsstufe läuft. Nicht selbst
  entscheiden, sondern auf weitere Ansage warten.
- **`logiBUS_QD_PWM` fehlt `TRUE` an `QI`** — der Ausgang bekommt dadurch
  kein Enable/Init-Signal und funktioniert nicht. Muss verdrahtet werden.
- **Zweites Eingabefeld (PWM-Rohwert) fehlt komplett** — pro Kanal soll es
  neben dem Prozent-Zahlenfeld (mit Komma/Skalierung) noch ein zweites
  Eingabefeld für den PWM-**Rohwert** geben (ganzzahlig, kein Komma/Scale=1),
  wie im Referenzprojekt `Workspace_PWM`. In `Workspace_PWM12` ist aktuell
  pro Kanal nur ein `CInputNumber` gebaut — das zweite Feld muss ergänzt
  werden (eigenes `CInputNumber`-Objekt + CProxy + Verdrahtung).
- **`E_RS_PV`-Event kommt nicht durch, sobald einmal `S` gesetzt wurde:**
  Sobald `E_RS`s `Q`-Ausgang einmal auf `TRUE` steht (durch `S`), feuert das
  `EO`-Ereignisausgang bei weiteren `S`-Events offenbar nicht mehr erneut
  (Bistabile FBs lösen ihr Ausgangsevent typischerweise nur bei echtem
  Zustandswechsel aus, nicht bei jedem `REQ`, wenn der Zustand schon steht).
  Damit wird der nachgeschaltete `F_SEL.G` nie erneut getriggert, und keine
  weiteren Werte von dieser Quelle laufen mehr durch den Mux —
  der Zwei-Quellen-Merge auf `RampLimitFS.PV` "friert" nach dem ersten
  `S`-Event ein. Betrifft das `E_RS`+`F_SEL`-Muster aus
  `RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB` (siehe Architektur-Entscheidungen
  oben). Noch zu klären: anderer Bistabil-Baustein, oder zusätzliches
  Re-Trigger-Event nötig, oder Muster grundsätzlich überdenken.
  **Passendes Symptom:** VT→Web zieht den Web-Slider korrekt nach; Web→VT
  (Slider ziehen) hat keine Wirkung — vermutlich dieselbe Ursache, da der
  Web-Schreibpfad über `AR_SUBSCRIBE_1` genau den `E_RS_PV`-Zweig des Mux
  benutzt und nach dem ersten erfolgreichen Durchlauf einfriert.

### Layout-Redesign gewünscht (VT-Kanalzeile) 🎨

- **Balkengrafik viel zu groß** — nimmt aktuell unverhältnismäßig viel Platz
  weg (Stand: `Bargraph_PWM_Q0n` vertikal, 110×200px, 4 Kanäle als Spalten
  pro Seite).
- **Umstellung auf horizontales Layout:** Seite in **3 oder 4 Zeilen**
  einteilen (nicht Spalten wie bisher) — je eine Zeile pro PWM-Kanal, alle
  Bedienelemente eines Kanals horizontal nebeneinander in dieser Zeile.
- **Balkengrafik horizontal, links-nach-rechts**, in genau dieser
  Reihenfolge (identisch mit der ursprünglichen Button-Reihenfolge):
  `0 -- - + ++ F` — also ganz links der `0`-Button, ganz rechts der
  `F`-Button (Full), Balken füllt sich dazwischen von links (leer/0) nach
  rechts (voll/F).
- **Begründung/Workflow:** Drückt man rechts (Richtung `F`), bewegt sich der
  Balken nach rechts (Wert steigt); drückt man links (Richtung `0`), bewegt
  er sich nach links (Wert sinkt) — Button-Position und Balken-Bewegungsrichtung
  stimmen dann visuell überein, das ist intuitiver als das bisherige
  vertikale Layout.
- Betrifft `Workspace_PWM12`s `DataMask_PWM1/2/3.jvi` (aktuelles Pro-Kanal-
  Layout aus dem ursprünglichen Plan: Zahlenfeld + vertikaler Bargraph +
  6 Tasten in 2×3-Raster) — kompletter Neuentwurf des Kanal-Layouts nötig,
  nicht nur eine Anpassung.
- **Screenshot-Bestätigung (`DataMask_PWM1.jvi`, 4-Spalten-Ansicht):** Zeigt
  genau die beschriebenen Probleme visuell — die Prozent-Zahlenfelder
  (Font `24x32`) laufen über die Spaltenbreite hinaus und überlappen sich
  zu einer einzigen unlesbaren Zeile quer über alle 4 Kanäle
  (`0 .0000.0000.0000.000`); darunter je ein großer leerer grauer
  Rechteck-Platzhalter (vertikaler Bargraph, ~110×200px, nimmt den Großteil
  der Spaltenhöhe ein); darunter die 6 Tasten aktuell im 2×3-Raster
  (`0`/`F` oben, `-`/`+` Mitte, `--`/`++` unten) — bestätigt, dass die
  Tasten noch nicht in der gewünschten horizontalen `0 -- - + ++ F`-Reihe
  liegen.
- **Schriftgröße:** `6x8` ist kaum lesbar, `24x32` ist so riesig, dass die
  Zahlenfelder nicht mehr auseinanderzuhalten sind (siehe Screenshot). Eine
  Zwischengröße ist nötig — z. B. aus Krauternters Font-Katalog (siehe
  `Objekthierarchie`-Recherche oben): `12x16`, `16x16` oder `16x24` als
  Kandidaten, noch nicht final entschieden.

### Bestätigt funktionierend ✅ (Live-Test)

- **Eingänge (I1-I8)** werden auf der VT korrekt angezeigt.
- **`AR_SUBSCRIBE_1` vom Web-Schieberegler her** funktioniert — ein Wert, der
  im Web-Client per Slider geschrieben wird, kommt im Composite an.

### Noch offen (nicht automatisiert prüfbar) ⚠️

- **Reale Verifikation in ISO-Designer/4diac IDE** — alle Validierungen in dieser
  Session waren strukturell (wohlgeformt, keine dangling refs, keine doppelten
  IDs). Der eigentliche Test (Pool öffnen, kompilieren, "Change Type" auf die
  PWM-Composite, echte Hardware) steht noch aus.
- **`DataType.Float` vs `Double`** für OPC-UA REAL im Web-Client — Annahme
  `Float` (korrekte 32-Bit-IEC-61499-REAL-Zuordnung), noch nicht gegen echtes
  FORTE verifiziert (Kommentar im Code hinterlassen).
- **RampLimitFS-Abhängigkeit** — referenziert weiterhin extern
  (`eclipse4diac::signalprocessing::RampLimitFS`, Nightly-Build), wie mit dem
  Nutzer abgestimmt (spezifische IDE wird den Lernenden bereitgestellt).

## Kritische Dateien

- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/RampLimitFS_TO_logiBUS_QDA_PWM_OPC.SUB`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Type Library/MyLib/sys/F_PWM_PERCENT_TO_RAW.SUB` / `F_PWM_RAW_TO_PERCENT.SUB`
- `Ventilsteuerung/4diacIDE-workspace/.lib/logiBUS-3.0.0/typelib/signalprocessing/fieldbus/F_PERCENT_TO_FRACTION.fbt` / `F_FRACTION_TO_PERCENT.fbt`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/Meins/InputOutputTester/Button_PWM_OPC_UA/SubStrings.gcf`
- `Ventilsteuerung/ISO-DesignerProjects/Workspace_PWM12/DefaultPool/DefaultPool.jop`
- `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`
- `Ventilsteuerung/Web-Clients/apixon-diodo-client/` (Vorlage für `apixon-pwm-client`)
