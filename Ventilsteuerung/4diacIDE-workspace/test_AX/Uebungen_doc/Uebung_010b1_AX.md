# Uebung_010b1_AX: ISOBUS AUX Input (Joystick)

[Uebung_010b1_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b1_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b1_AX`. Neben Softkeys und Buttons ist AUX-N die dritte wichtige Eingabemethode im ISOBUS.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010b1_AX.png)


## Ziel der Übung

Verarbeitung von Auxiliary Inputs (z.B. Joystick-Tasten).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010b1_AX.SUB` verbindet eine AUX-Funktion mit einem Ausgang[cite: 1].

### Funktionsbausteine (FBs)

  * **`AuxFunction2_X1`**: Typ `isobus::UT::io::Auxiliary::IN::Aux_IXA`. Dieser Baustein lauscht auf ISOBUS AUX-Nachrichten für die definierte Funktion.

-----

## Funktionsweise

Im Gegensatz zu Softkeys, die fest auf dem Bildschirm sind, ist eine AUX-Funktion abstrakt. Der Nutzer muss am Terminal erst einen physischen Eingang (z.B. Taste auf dem Joystick) dieser Funktion ("Funktion 2") zuweisen (Teaching).
Sobald das Mapping steht: Joystick-Taste drücken -> `Aux_IXA` wird TRUE -> Ausgang schaltet.
