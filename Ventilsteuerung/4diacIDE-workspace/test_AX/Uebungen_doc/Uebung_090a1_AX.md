# Uebung_090a1_AX: Signal-Multiplexer (2-fach)

```{index} single: Uebung_090a1_AX: Signal-Multiplexer (2-fach)
```

[Uebung_090a1_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_090a1_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_090a1_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [R_TRIG & F_TRIG: So erkennen SPS-Steuerungen Signalflanken zuverlässig – ohne Doppelbehandlung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/R_TRIG--F_TRIG-So-erkennen-SPS-Steuerungen-Signalflanken-zuverlssig--ohne-Doppelbehandlung-e370kqh)
* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)
* [logiBUS® verstehen: Direkte Signalweiterleitung – Das "Hallo Welt" der Automatisierung](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg)
* [Das tödliche Dilemma des Relais: Warum Silberkontakte bei Kleinsignalen versagen und Gold bei Last schmilzt – Der Freibrenn-Effekt erklärt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-tdliche-Dilemma-des-Relais-Warum-Silberkontakte-bei-Kleinsignalen-versagen-und-Gold-bei-Last-schmilzt--Der-Freibrenn-Effekt-erklrt-e3a9lhv)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_090a1_AX.png)


## Ziel der Übung

Auswahl eines Signals aus mehreren Quellen (Umschalter).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_090a1_AX.SUB` verwendet einen `AX_MUX_2` Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` & `I2`**: Die beiden Signalquellen.
  * **`I4`**: Der Wahlschalter (Selector).
  * **`F_MUX_2`**: Der Multiplexer.
  * **`F_BOOL_TO_UINT`**: Hilfsbaustein zur Konvertierung.

-----

## Funktionsweise

Der Multiplexer erwartet am Eingang `K` eine Ganzzahl (UINT), um zu entscheiden, welchen Eingang er durchschaltet.
Da `I4` ein boolesches Signal liefert, wird dieses konvertiert:
*   `I4 = FALSE` -> `K = 0` -> `MUX` schaltet `IN1` (`I1`) auf den Ausgang.
*   `I4 = TRUE` -> `K = 1` -> `MUX` schaltet `IN2` (`I2`) auf den Ausgang.

Der Ausgang `Q1` folgt also entweder `I1` oder `I2`, abhängig von der Stellung von `I4`.

-----

## Anwendungsbeispiel

**Hand/Automatik-Umschaltung**:
*   `I1`: Signal aus der Automatik-Steuerung.
*   `I2`: Signal vom Hand-Taster.
*   `I4`: Schlüsselschalter "Hand/Auto".
Der Ausgang (`Q1`) wird je nach Betriebsart von der Automatik oder manuell gesteuert.