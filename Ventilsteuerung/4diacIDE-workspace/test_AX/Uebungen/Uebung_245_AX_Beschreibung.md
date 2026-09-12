# Übung 245: Sollwert mit festem Korrekturfaktor skalieren — AR_MUL_2 zwischen zwei PHYSA-Zahlenfeldern

## Thema: Feste lineare Korrektur eines REAL-Sollwerts, rein über AR-Adapter (kein REQ/CNF nötig)

### Situationsbeschreibung

Ein Sollwert (z.B. ein Tastgrad in Prozent) durchläuft auf dem Weg zum Verbraucher eine
Signalkette mit einem systematischen, aber bekannten und konstanten Fehler — z.B. einen
Tiefpassfilter, dessen Ausgangsimpedanz gegen die Eingangsimpedanz des angeschlossenen
Verbrauchers einen Lastteiler bildet (Spannungsteiler-Effekt: der Verbraucher "zieht" das
Signal herunter). Wenn dieser Effekt konstant ist (gleiche Bauteile, gleiche Impedanzen),
kann er mit einem festen multiplikativen Korrekturfaktor kompensiert werden: der gesendete
Sollwert wird um genau den Kehrwert des Lastteiler-Verhältnisses erhöht, damit am Verbraucher
der ursprünglich gewünschte Wert ankommt.

Diese Übung baut das Kernstück dieser Kompensation nach: ein Eingabe-Zahlenfeld (`I3`) liefert
den unkorrigierten Sollwert, ein `AR_MUL_2` mit einem über `initval_AR` fest eingespeisten
zweiten Faktor skaliert ihn, ein Ausgabe-Zahlenfeld (`N3`) zeigt das Ergebnis.

### Funktionsbeschreibung

- **Eingabe:** `NumericValue_PHYSA` liest das VT-Eingabefeld `InputNumber_I3_N` und liefert den
  physikalischen (bereits skalierten) REAL-Wert über den `rPhys`-AR-Adapter — siehe
  `Uebung_011f_PHYSA` für das reine Durchschleifen ohne Umrechnung.
- **Fester Faktor als AR-Konstante:** `initval_AR` (`INIT_VAL = REAL#1,17619`) erzeugt aus einem
  festen Parameter einen AR-Adapter-Wert — sein unverdrahtetes `INIT`-Event feuert automatisch
  einmalig beim Kaltstart (dasselbe Prinzip wie bei den unverdrahteten `INIT`-Events von
  `Q_NumericValue_PHYSA` in dieser und anderen Übungen: ein nicht verbundenes Event dieser Art
  wird von 4diac beim Ressourcen-Start automatisch ausgelöst).
- **Korrektur:** `AR_MUL_2` (generischer AR-nativer Multiplikations-FB, exakt das Muster von
  `AR_ADD_2` aus `Uebung_011b1_PHYSA`, nur mit `MUL` statt `ADD`) multipliziert `IN1` (der
  durchgereichte Sollwert von `I3`) mit `IN2` (der Konstante aus `initval_AR`) — rein über
  AR-Adapter-Verbindungen, ganz ohne eigene `REQ`/`CNF`-Verkabelung. Der Faktor 1,17619 ist der
  Kehrwert von 0,8502 — einem beispielhaften Lastteiler-Verhältnis, wie es bei einem Danfoss-PVEA-
  Proportionalventil mit vorgeschaltetem PWM-Tiefpassfilter auftreten kann: 12 kΩ
  Verbraucher-Eingangsimpedanz gegen 2,115 kΩ Filter-Ausgangsimpedanz.
- **Ausgabe:** `AR_MUL_2.OUT` geht direkt (AR-Adapter) auf `Q_NumericValue_PHYSA.rPhys`, das das
  Ergebnis auf `OutputNumber_N3_N` schreibt.

**Warum als SUB (Composite) und nicht als eigener `.fbt` (Basic-FB/ST-Funktion)?** In diesem
Projekt gibt es keinen einzigen selbstgeschriebenen `.fbt` — jede eigene Logik wird als
Composite aus bestehenden Bausteinen verdrahtet, auch eine simple Multiplikation mit fester
Konstante (siehe `MyLib::sys::F_AI_RAW_TO_PERCENT`, das ebenso einen Standard-`F_MUL` mit festem
`IN2` instanziiert statt eigenen ST-Code zu schreiben — dort im `REQ`/`CNF`-Stil, hier rein über
AR-Adapter, je nachdem was die Nachbarbausteine schon anbieten).

### Arbeitsauftrag

1. Legen Sie die SubApp `Uebung_245_AX` an (bereits als Referenzlösung vorhanden).
2. Verbinden Sie `NumericValue_PHYSA.rPhys` (`IN1`) und `initval_AR.OUT` (`IN2`) mit den beiden
   Sockets von `AR_MUL_2`, dessen `OUT`-Plug mit `Q_NumericValue_PHYSA.rPhys`.
3. Testen Sie: Geben Sie auf dem VT-Eingabefeld `I3` einen Wert ein (z.B. 50,00) und prüfen Sie,
   dass `N3` den mit dem Faktor multiplizierten Wert anzeigt (bei 1,17619: 58,81).
4. Zusatzaufgabe: Auf welche Werte korrigiert derselbe Faktor 1,17619 die Eingaben 25 % und 75 %?
   (Antwort: 29,40 % bzw. 88,21 % — die Korrektur ist linear und gilt mit demselben Faktor für
   den gesamten Bereich einheitlich, keine gesonderten `INIT_VAL`-Werte pro Eingabe nötig.)

### Referenzlösung

`Uebung_245_AX.SUB`. Verwandte Übungen: `Uebung_011f_PHYSA` (reines Durchschleifen ohne
Korrektur), `Uebung_011b1_PHYSA` (Verknüpfung zweier Eingabefelder über `AR_ADD_2`, dasselbe
AR-native Verdrahtungsmuster wie hier, nur mit `ADD` statt `MUL` und ohne `initval_AR`).
