# Uebung_103c: Fixierte Modus-Selektion

```{index} single: Uebung_103c: Fixierte Modus-Selektion
```

[Uebung_103c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_103c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_103c`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_103c.png)


## Ziel der Übung

Testen eines spezifischen Pfads der MUX/DEMUX Struktur.

-----

## Beschreibung

[cite_start]Im Vergleich zu `Uebung_103` wurde das Eingabefeld entfernt[cite: 1]. Der Selektionswert wird stattdessen über einen `F_MOVE` Baustein fest auf den Wert `UINT#1` (Index 1 -> Zweig 2 "rastend") gesetzt.

-----

## Funktionsweise

Der Taster `I1` steuert den Ausgang `Q1` nun permanent im "rastenden" Modus (Toggle), obwohl die Struktur für andere Modi noch vorhanden ist. Dies dient oft zum Debugging oder zum schnellen Einfrieren einer Konfiguration.