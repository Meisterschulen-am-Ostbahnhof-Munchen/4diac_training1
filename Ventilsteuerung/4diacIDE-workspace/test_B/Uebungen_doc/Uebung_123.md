# Uebung_123: Teilnehmer-Filterung

[Uebung_123](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_123.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_123`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_123.png)


## Übersicht

[cite_start]Hier wird gezeigt, wie man den Netzwerk-Scan gezielt auf bestimmte Gerätetypen einschränkt[cite: 1].
Durch die Angabe einer Zieladresse (`VT_ADD`) und einer Maske (`VT_FLT`) am Baustein `NmGetCfInfo_1` wird das Programm so konfiguriert, dass es nur auf Teilnehmer reagiert, die dem Profil eines "Virtual Terminals" (VT) entsprechen. Alle anderen Bus-Teilnehmer (z.B. Joysticks oder Task Controller) werden von diesem Baustein ignoriert. Dies ermöglicht eine saubere Trennung der Kommunikationslogik nach Funktionsgruppen.
