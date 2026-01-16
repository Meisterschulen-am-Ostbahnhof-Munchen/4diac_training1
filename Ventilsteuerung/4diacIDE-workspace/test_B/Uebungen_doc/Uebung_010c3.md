# Uebung_010c3: Strukturierung von UI-Feedback (Typed)

[Uebung_010c3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010c3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010c3`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010c3.png)


## Übersicht

[cite_start]Hier wird die Kapselung konsequent zu Ende geführt: Aus der Sub-Applikation wird ein echter Typ `Uebung_010c3_sub` erstellt[cite: 1]. Dieser Baustein kann nun wie ein Standard-Baustein aus der Bibliothek verwendet werden. Er verlangt lediglich die Angabe der Softkey-ID und des Hardware-Ausgangs als Parameter und erledigt die gesamte interne Verschaltung von Logik und Feedback automatisch.
