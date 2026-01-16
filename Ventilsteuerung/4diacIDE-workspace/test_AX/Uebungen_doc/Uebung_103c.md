# Uebung_103c: Fixierte Modus-Selektion

[Uebung_103c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_103c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_103c`.


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
