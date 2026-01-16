# Uebung_093: Zeitgesteuerte Ereignis-Tabelle (E_TABLE)

[Uebung_093](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_093.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_093`. Hier wird ein komplexes Zeitmuster für Ereignisse definiert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_093.png)


## Ziel der Übung

Verwendung des Bausteins `E_TABLE`. Im Gegensatz zum gleichmäßigen Takt des `E_TRAIN` erlaubt dieser Baustein die Definition von individuellen Verzögerungszeiten für jedes Ereignis in einer Liste (Array).

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_093.SUB` ist ein Zeit-Array hinterlegt: `[T#0s, T#2s, T#3s, T#4s]`[cite: 1].

### Funktionsweise

Ein Klick auf **I1** startet die Tabelle:
1.  Ereignis 1: Sofort (`0s`).
2.  Ereignis 2: Nach weiteren 2 Sekunden.
3.  Ereignis 3: Nach weiteren 3 Sekunden.
4.  Ereignis 4: Nach weiteren 4 Sekunden.

Das angeschlossene Flip-Flop erzeugt somit ein unregelmäßiges Blinkmuster am Ausgang `Q1`, das exakt dem vorgegebenen Zeitplan entspricht. Dies ermöglicht die Programmierung von spezifischen Start-Sequenzen oder rhythmischen Abläufen.
