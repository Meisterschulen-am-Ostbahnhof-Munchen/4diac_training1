# Uebung_020h: Ereignisgesteuerter Impuls (E_PULSE)

[Uebung_020h](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020h.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020h`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020h.png)


## Übersicht

[cite_start]Diese Übung zeigt die Ansteuerung des Bausteins `E_PULSE` durch einen Ereignis-Eingang (`logiBUS_IE`)[cite: 1].
Jeder erkannte Einzelklick am Taster löst am Ausgang einen exakt 5 Sekunden langen Impuls aus. Da `E_PULSE` ein reiner Event-Baustein ist, benötigt er kein dauerhaftes Datensignal am Eingang, sondern nur den Start-Trigger.
