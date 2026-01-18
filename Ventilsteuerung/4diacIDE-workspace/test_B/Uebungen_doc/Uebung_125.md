# Uebung_125: Antwort auf Anfrage (TX on Request)

```{index} single: Uebung_125: Antwort auf Anfrage (TX on Request)
```

[Uebung_125](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_125.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_125`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_125.png)


## Übersicht

[cite_start]Verwendung des Bausteins `AlPgnTxNew8B_REQ` mit Callback-Funktion[cite: 1].
In dieser Übung sendet die Steuerung die Daten nicht von sich aus, sondern wartet passiv auf eine Anfrage (ISO Request) eines anderen Teilnehmers. Sobald eine Anfrage für die spezifizierte PGN (`61184`) eintrifft, holt sich der Baustein die aktuellen Daten über den Adapter-Port `CB` (Callback) aus der Sub-Applikation `DataSupply` und sendet die Antwort automatisch zurück. Dies spart Buslast, da Daten nur bei echtem Bedarf übertragen werden.