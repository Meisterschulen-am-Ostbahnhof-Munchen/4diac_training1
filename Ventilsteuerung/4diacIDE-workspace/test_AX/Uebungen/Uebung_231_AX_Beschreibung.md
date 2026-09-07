# Übung 231: Sollwert mit festem Korrekturfaktor skalieren — F_MUL zwischen zwei PHYSA-Zahlenfeldern

## Thema: Feste lineare Korrektur eines REAL-Sollwerts, AR-Adapter durch eine Funktion "durchbrechen"

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
den unkorrigierten Sollwert, ein `F_MUL` mit festem `IN2`-Parameter skaliert ihn, ein
Ausgabe-Zahlenfeld (`N3`) zeigt das Ergebnis.

### Funktionsbeschreibung
- **Eingabe:** `NumericValue_PHYSA` liest das VT-Eingabefeld `InputNumber_I3_N` und liefert den
  physikalischen (bereits skalierten) REAL-Wert über den `rPhys`-AR-Adapter — siehe
  `Uebung_011f_PHYSA` für das reine Durchschleifen ohne Umrechnung.
- **AR nach REAL:** `AR_R_TO_REAL` "bricht" den AR-Adapter auf: sein `CNF`-Event liefert den
  aktuellen Wert als plain `REAL`-Output (`IN`), sobald sich `I3` ändert. Nur so ist der Wert für
  eine gewöhnliche `REQ`/`CNF`-Funktion wie `F_MUL` überhaupt nutzbar — Adapter-Sockets/Plugs
  lassen sich nicht direkt mit einer Funktion verbinden.
- **Korrektur:** `F_MUL` (IEC 61131-3 Standardfunktion, generisch als Composite mit `REQ`/`CNF`
  gekapselt — genau das Muster, das auch `MyLib::sys::F_AI_RAW_TO_PERCENT` und
  `MyLib::sys::RampLimitFS_TO_logiBUS_QDA_PWM_OPC` (dort für die 13-Bit-PWM-Skalierung)
  verwenden) multipliziert `IN1` (der durchgereichte Sollwert) mit dem festen `IN2 = REAL#1,17619`.
  Dieser Wert ist der Kehrwert von 0,8502 — dem Lastteiler-Verhältnis aus der
  Krauternter-PVEA-Kompensationsrechnung (`KrauternterSchaltplan/Zeichnungen/Schaltplan PWM auf
  PVG v24 - Uebersicht.md`): 12 kΩ Verbraucher-Eingangsimpedanz gegen 2,115 kΩ
  Filter-Ausgangsimpedanz.
- **REAL nach AR:** `AR_REAL_TO_R` macht aus dem korrigierten `REAL`-Wert wieder einen
  AR-Adapter, den `Q_NumericValue_PHYSA` auf das Ausgabefeld `OutputNumber_N3_N` schreibt.

**Warum als SUB (Composite) und nicht als eigener `.fbt` (Basic-FB/ST-Funktion)?** In diesem
Projekt gibt es keinen einzigen selbstgeschriebenen `.fbt` — jede eigene Logik wird als
Composite aus bestehenden Bausteinen verdrahtet, auch eine simple Multiplikation mit fester
Konstante (siehe `F_AI_RAW_TO_PERCENT.SUB`, das genauso einen `F_MUL` mit festem `IN2`
instanziiert statt eigenen ST-Code zu schreiben).

### Arbeitsauftrag
1. Legen Sie die SubApp `Uebung_231_AX` an (bereits als Referenzlösung vorhanden).
2. Verbinden Sie `NumericValue_PHYSA.rPhys` über `AR_R_TO_REAL` → `F_MUL` (`IN2` fest auf einen
   Korrekturfaktor Ihrer Wahl, z.B. `REAL#1.17619`) → `AR_REAL_TO_R` mit
   `Q_NumericValue_PHYSA.rPhys`.
3. Testen Sie: Geben Sie auf dem VT-Eingabefeld `I3` einen Wert ein (z.B. 50,00) und prüfen Sie,
   dass `N3` den mit dem Faktor multiplizierten Wert anzeigt (bei 1,17619: 58,81).
4. Zusatzaufgabe: Welche `IN2`-Werte würden 25 % und 75 % auf die aus der
   PVEA-Kompensationsrechnung bekannten 29,41 % bzw. 88,22 % korrigieren? (Antwort: derselbe
   Faktor 1,17619 — die Korrektur ist linear und gilt für den gesamten Bereich einheitlich.)

### Referenzlösung
`Uebung_231_AX.SUB`. Verwandte Übungen: `Uebung_011f_PHYSA` (reines Durchschleifen ohne
Korrektur), `Uebung_011b1_PHYSA` (Verknüpfung zweier Eingabefelder über `AR_ADD_2`, direkt am
AR-Adapter statt über `REQ`/`CNF`).
