# Uebung_153: PID-Regelung

[Uebung_153](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_153.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_153`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_153.png)


## Ziel der Übung

Präzisere Regelung durch einen PID-Algorithmus.

-----

## Beschreibung

[cite_start]Strukturell identisch zu `Uebung_152`, jedoch wird der Baustein `CTRL_PID` verwendet[cite: 1].
Zusätzlich zum P- und I-Anteil verfügt dieser über einen D-Anteil (`TV` Parameter), der auf die Änderungsgeschwindigkeit der Regelabweichung reagiert. Dies ermöglicht ein schnelleres Einregeln bei plötzlichen Störungen, erfordert aber eine sorgfältigere Parametrierung.
