# Uebung_035a2: Ampelschaltung mit Blinkphase

[Uebung_035a2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_035a2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_035a2`. Hier wird die Ampelsteuerung um die in einigen Ländern (z.B. Österreich) übliche Grün-Blinkphase erweitert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_035a2.png)


## Übersicht

[cite_start]Unter Verwendung eines 5-Schritt-Sequenzers wird ein zusätzlicher Zustand "Grün Blinken" eingefügt[cite: 1].
Nach der Grünphase (Schritt 3) startet der Sequenzer einen `E_TRAIN` Baustein (Schritt 4). Dieser erzeugt 4 kurze Impulse im 500ms Takt, die über ein Toggle-Flip-Flop die grüne Lampe blinken lassen. Erst nach Abschluss dieser Blink-Sequenz schaltet das System in die Gelbphase (Schritt 5). Dies zeigt die nahtlose Integration von Sub-Sequenzen innerhalb einer übergeordneten Schrittkette.
