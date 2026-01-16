# Uebung_010bA2: AUX-Zustands-Events (Enabled)

[Uebung_010bA2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010bA2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010bA2`. Hier geht es um die Feinheiten der AUX-Spezifikation bezüglich rastender und tastender Eingänge.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010bA2.png)


## Funktionsweise

[cite_start]Verwendet `AuxFunction2_X1` mit dem Event `AuxEnabled`[cite: 1]. Das Verhalten hängt vom Typ des zugewiesenen Bedienelements (Joystick-Taste) ab:
*   Bei einem **tastenden Bediener** (NonLatched) wird das Event nur einmal beim Drücken gesendet.
*   Bei einem **rastenden Bediener** (Latched) wird das Event zyklisch wiederholt, solange der Schalter aktiv ist.
Dies verdeutlicht, wie die Software auf die Hardware-Eigenschaften des verwendeten Joysticks reagiert.
