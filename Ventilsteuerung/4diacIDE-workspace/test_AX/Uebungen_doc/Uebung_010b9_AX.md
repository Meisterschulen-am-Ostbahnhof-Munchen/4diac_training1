# Uebung_010b9_AX: Button Event (STILL_HELD - Blinker)

[Uebung_010b9_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b9_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b9_AX`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010b9_AX.png)


## Ziel der Übung

Wiederholende Events.

-----

## Beschreibung

[cite_start]Nutzt `Button_A1` mit `BT_STILL_HELD`[cite: 1].

-----

## Funktionsweise

Wie im Kommentar beschrieben: *"BT_STILL_HELD wird alle 200ms wiederholt."*
Wenn der Nutzer den Button gedrückt hält, feuert der Baustein alle 200ms ein Event. Da dies an ein Toggle-Flip-Flop geht, blinkt der Ausgang (`Q1`) alle 200ms um (Periode 400ms), solange gedrückt wird.
