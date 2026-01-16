# Uebung_010b3: AUX-Ereignis-Steuerung

[Uebung_010b3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b3`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010b3.png)


## Ziel der Übung

Verwendung von `Aux_IE` (Event) zur Steuerung von Speichern.

-----

## Beschreibung

[cite_start]In `Uebung_010b3.SUB` wird eine AUX-Funktion genutzt, um ein Flip-Flop zu toggeln[cite: 1].

### Funktionsweise

Es wird das Event `AuxDisabled_START` verwendet. In der ISOBUS-Terminologie bedeutet dies den Übergang in den Zustand "Deaktiviert". Das entspricht dem **Loslassen** einer Joystick-Taste. Das Flip-Flop wechselt also beim Loslassen der Taste seinen Zustand.
