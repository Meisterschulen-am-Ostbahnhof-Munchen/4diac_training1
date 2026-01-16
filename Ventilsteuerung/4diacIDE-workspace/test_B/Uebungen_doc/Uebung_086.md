# Uebung_086: Ereignis-Weiche (E_SWITCH)

[Uebung_086](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_086.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_086`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_086.png)


## Übersicht

[cite_start]Verwendung des fundamentalen Bausteins `E_SWITCH`[cite: 1].
In dieser Übung wird demonstriert, wie ein Ereignis-Strom (`EI`) basierend auf einem logischen Zustand (`G`) auf zwei verschiedene Pfade aufgeteilt wird.
*   Ist der Schalter `I1` auf `FALSE`, landet das `IND`-Ereignis am Ausgang `EO0`.
*   Ist der Schalter `I1` auf `TRUE`, landet das `IND`-Ereignis am Ausgang `EO1`.
Dies ist die Basis für jede bedingte Programmausführung ("If-Then-Else") in der IEC 61499.
