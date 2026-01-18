# Uebung_126: Zyklisches Senden mit Callback

```{index} single: Uebung_126: Zyklisches Senden mit Callback
```

[Uebung_126](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_126.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_126`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_126.png)


## Übersicht

[cite_start]Verwendung des Bausteins `AlPgnTxNew8Bcycl_REQ`[cite: 1].
Hier wird die Nachricht in einem festen Zeitintervall (Parameter `u16DefRepRate = 500`ms) wiederholt auf den Bus gesendet. Der Baustein nutzt ebenfalls den Callback-Mechanismus (`CB`), um vor jedem Sendevorgang die allerneuesten Daten aus der Applikation abzufragen. Dies ist das Standard-Verfahren für Status-Nachrichten, die permanent zur Verfügung stehen müssen (z.B. Herzschlag oder Sensordaten).
