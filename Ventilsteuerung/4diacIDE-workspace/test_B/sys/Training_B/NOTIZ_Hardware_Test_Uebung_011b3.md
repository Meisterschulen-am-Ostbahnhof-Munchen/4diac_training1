# Notiz: Hardware-Test Uebung_011b3 (feature/Testing_for_Elias)

Dokumentiert den Test von `Uebungen::Uebung_011b3`
(`test_B/Uebungen/Uebung_011b3.SUB`) auf derselben Hardware wie
`Uebung_011b1` (siehe `NOTIZ_Hardware_Test_Uebung_011b1.md`): ESP32-P4
Rev. 0.3, forte `v0.27-alpha-a-97-gb8dd4796`, IDF `v6.0.2d`.

## Aufbau

Zwei VT-Zahlenfelder (`InputNumber_I1`, `InputNumber_I2`) → je
`F_DWORD_TO_UDINT` → `F_SUB` (`iec61131::arithmetic::F_SUB`, UDINT) →
Ergebnis auf `OutputNumber_N1` (`Q_NumericValue`).

## Ergebnis

✅ **10 - 2 = 8** — korrekt auf der echten Hardware bestätigt.

⚠️ **1 - 12 = UDINT#4294967285** — kein Bug: `F_SUB` rechnet auf `UDINT`
(vorzeichenlos, 32 Bit), daher läuft ein rechnerisch negatives Ergebnis
per Zweierkomplement-Wraparound um (`1 - 12 = -11 ≡ 2^32 - 11 =
4294967285 mod 2^32`). Das ist exakt das in IEC 61131-3 spezifizierte
Verhalten für vorzeichenlose Ganzzahltypen — **kein Fehler in `F_SUB`
oder in dieser Übung.**

## Offener Punkt: SAFE Arithmetic Lib

Für die praktische Anwendung ist ein solcher stiller Wraparound
gefährlich (z. B. Sollwert-Differenzen, Restwegberechnungen), sobald ein
negatives Zwischenergebnis auf einem vorzeichenlosen Typ möglich ist.

**Entscheidung:** Es wird eine **SAFE Arithmetic Lib** benötigt (Clamping
und/oder Über-/Unterlauf-Erkennung für die vorzeichenlosen Grundoperationen).
Diese wird **nicht in dieser Session gebaut** — das übernimmt ein anderer
Bearbeiter/eine andere Session.
