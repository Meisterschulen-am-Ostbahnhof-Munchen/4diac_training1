# GcfFunctionCall - Function in ST aus einer GCF aufrufen

Uebung im Package `Meins::GcfFunctionCall`: Wie kann eine in ST geschriebene
Function (`.fct`) aus einer GlobalConstants-Datei (`.gcf`) heraus benutzt werden?
Grundlage fuer eine spaetere eigene Lib (analog `MyLib_AX_Option`).

## Inhalt

| Datei | Zweck |
|---|---|
| `F_Double.fct` | ST-Function, `F_Double(Value) = Value * 2` (INT) |
| `const/FuncConst.gcf` | `BASE_VALUE := 7`, `DOUBLE_VALUE := F_Double(BASE_VALUE)` |
| `GcfFunctionCallTest.fbt` | Basic FB: liest `DOUBLE_VALUE` und ruft `F_Double` direkt auf, `Passed` = TRUE wenn beide 14 |
| `Uebung_011d_GcfFunc_AX.SUB` | VT-Anzeige: `DOUBLE_VALUE` als `rPhys` an `Q_NumericValue_PHYS` (`OutputNumber_N3_N`) |

## Ablauf

1. `FuncConst.gcf` importiert nichts; die Function wird per vollem Namen
   `Meins::GcfFunctionCall::F_Double(...)` im `InitialValue` aufgerufen.
2. `Uebung_011d_GcfFunc_AX` importiert `DOUBLE_VALUE` und `OutputNumber_N3_N`
   (aus `Uebungen::const::UT::DefaultPool_Numeric`) und setzt sie als Parameter
   `rPhys` bzw. `stObj` des Bausteins `Q_NumericValue`.
3. Erwartung: Auf N3 erscheint 14 (Offset/Scale des Objekts wirken auf den Wert).

## Ergebnis

Bestanden. Der Export akzeptiert den Funktionsaufruf als `InitialValue` und
wertet ihn zur Exportzeit aus: Im Bootfile `test_AX_FORTE_PC_AX.fboot` steht
`rPhys` direkt als `14.0` (= `F_Double(7)`), weder `F_Double` noch
`DOUBLE_VALUE` tauchen dort auf. Die Function laeuft also nicht zur Laufzeit
auf dem Geraet. Voraussetzung: Die Argumente sind Konstanten.

Nicht geprueft: Anzeige 14 auf N3 im VT (Offset/Scale des Objekts).

Hinweis: `Comment=` in der GCF kurz halten (IDE-Wrap-Bug beim Resave).

## Umbenennung

`Uebung_011d.SUB` hiess so wie `Uebungen/Uebung_011d_AX`/`_AUDI` (andere
Package, gleiche Basis); umbenannt in `Uebung_011d_GcfFunc_AX`, um Verwechslung
zu vermeiden. Name im Dateikopf (`SubAppType Name`) angepasst.
