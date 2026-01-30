# Uebung_003c: Mapping auf ISOBUS AUX (Standard-Pins)

```{index} single: Uebung_003c: Mapping auf ISOBUS AUX (Standard-Pins)
```

[Uebung_003c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003c`. Hier wird demonstriert, wie lokale Hardware-Eingänge an das ISOBUS-System als "Auxiliary Inputs" angebunden werden, wobei eine typisierte Sub-Applikation zur Strukturierung verwendet wird.

## 🎧 Podcast

* [Altbayerisch für Einsteiger: Von Gratler-Schnupfen und Stadthodern – Eine Laute-Reise durch Lektion 3C](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Altbayerisch-fr-Einsteiger-Von-Gratler-Schnupfen-und-Stadthodern--Eine-Laute-Reise-durch-Lektion-3C-e376jh4)

----

![](Uebung_003c.png)

## Ziel der Übung

Das Ziel ist es, lokale physische Schalter (`I1` bis `I4`) für das ISOBUS-Netzwerk verfügbar zu machen. In der ISOBUS-Welt können diese Eingänge als "Auxiliary Inputs" (Hilfseingänge) definiert werden. Der Endbenutzer kann diese dann am Terminal flexibel auf verschiedene Maschinenfunktionen mappen (z.B. "Taster 1 steuert Klappe auf/zu").

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003c.SUB` nutzt vier Instanzen des Typs `Uebung_003c_sub`, um vier Kanäle für das ISOBUS-Mapping bereitzustellen[cite: 1].

### Typisierte Sub-Applikation: `Uebung_003c_sub`

[cite_start]Dieser Baustein verbindet einen Standard-Digitaleingang mit einem ISOBUS-Auxiliary-Ausgang[cite: 2]. Er verfügt über folgende Parameter:
  * **`Input`**: Auswahl des lokalen Hardware-Pins (z.B. `Input_I1`).
  * **`iInpNr`**: Die fortlaufende Nummer des AUX-Eingangs im Objekt-Pool (Index 0 bis n).

Intern werden die Ereignisse (`IND -> REQ`) und Daten (`IN -> OUT`) vom `logiBUS_IX` zum `Aux_QX` Baustein durchgereicht.

### Konfiguration der Kanäle

In `Uebung_003c` erfolgt das Mapping wie folgt:
*   `F1`: `Input_I1` ➡️ AUX Index 0
*   `F2`: `Input_I2` ➡️ AUX Index 1
*   `F3`: `Input_I3` ➡️ AUX Index 2
*   `F4`: `Input_I4` ➡️ AUX Index 3

-----

## Funktionsweise

1.  Der Bediener betätigt einen der physischen Schalter (z.B. `I1`).
2.  Die entsprechende Instanz (z.B. `F1`) erkennt die Pegeländerung.
3.  Ein `IND`-Event wird ausgelöst und triggert den `REQ`-Port des `Aux_QX` Bausteins.
4.  Der `Aux_QX` Baustein sendet eine standardisierte ISOBUS-Nachricht in das CAN-Netzwerk, die den Status des "Auxiliary Input N" mitteilt.
5.  Das verbundene ISOBUS-Anbaugerät empfängt diese Nachricht und führt die vom Nutzer zugewiesene Aktion aus.

-----

## Anwendungsbeispiel

**Nachrüstung von Bedienelementen**:
Ein Traktor verfügt über keine originalen ISOBUS-Joystick-Tasten. Man installiert eine kleine Konsole mit vier Standard-Tastern in der Kabine und verbindet diese mit der logiBUS-Steuerung. Dank dieser Software-Logik erscheinen die Taster für alle ISOBUS-Geräte (z.B. Feldspritze, Düngerstreuer) als vollwertige, frei belegbare Bedienelemente auf dem Terminal.