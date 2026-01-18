# Uebung_131: Zyklisches Empfangen mit Überwachung

```{index} single: Uebung_131: Zyklisches Empfangen mit Überwachung
```

[Uebung_131](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_131.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_131`. Hier wird der Empfang von Nachrichten um eine Zeit-Überwachung (Timeout) ergänzt.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_131.png)


## Übersicht

[cite_start]Verwendung des Bausteins `AlPgnRxNew8Bcylc`[cite: 1].
Dieser Baustein ist speziell für Nachrichten gedacht, die regelmäßig (zyklisch) erwartet werden. Über den Parameter `u16CtrlTime = 1500`ms wird eine Kontrollzeit definiert. Sollte der Partner für länger als 1,5 Sekunden keine Nachricht mehr senden, wird dies als Kommunikationsabbruch gewertet. Die Applikation kann auf diesen Fehlerfall reagieren, um die Maschine in einen sicheren Zustand zu bringen.
