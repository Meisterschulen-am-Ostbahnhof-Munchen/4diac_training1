# Uebung_132: Daten aktiv abfragen (RX on Request)

[Uebung_132](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_132.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_132`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_132.png)


## Übersicht

[cite_start]In dieser Übung wird der Baustein `AlPgnRxNew8B_REQ` verwendet[cite: 1].
Anstatt passiv auf eine Nachricht zu warten, kann die Steuerung hier aktiv eine Anfrage (Request) nach einer bestimmten PGN an den Partner senden. Ein Klick auf Taster **I1** löst das `REQ`-Ereignis aus, woraufhin die Steuerung die entsprechende Anforderungs-Nachricht auf den Bus schickt. Sobald der Partner antwortet, wird dies als regulärer Empfang (`IND`) gewertet und verarbeitet.
