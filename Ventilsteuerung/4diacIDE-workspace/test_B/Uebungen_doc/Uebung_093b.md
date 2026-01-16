# Uebung_093b: Mehrkanal-Zeit-Tabelle (E_N_TABLE)

[Uebung_093b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_093b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_093b`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_093b.png)


## Übersicht

[cite_start]Erweiterung des Tabellen-Konzepts unter Verwendung des Bausteins `E_N_TABLE`[cite: 1].
Anstatt alle Ereignisse an einen gemeinsamen Ausgang zu senden, verfügt dieser Baustein über separate Ausgänge (`EO0` bis `EOn`) für jeden Tabelleneintrag.
In dieser Übung werden dadurch vier verschiedene Lampen (`Q1` bis `Q4`) in einer zeitlich exakt definierten, unregelmäßigen Abfolge nacheinander eingeschaltet. Dies ist die effizienteste Methode, um komplexe Start-Up-Sequenzen für Multi-Aktor-Systeme zu definieren.
