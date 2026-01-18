# Uebung_020g: Kombinierte Verzögerung (E_TONOF)

```{index} single: Uebung_020g: Kombinierte Verzögerung (E_TONOF)
```

[Uebung_020g](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020g.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020g`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [E_DELAY in IEC 61499: Präzise, Abbrechbare Zeitverzögerung in Steuerungssystemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_DELAY-in-IEC-61499-Przise--Abbrechbare-Zeitverzgerung-in-Steuerungssystemen-e3674le)
* [FB_TOF und E_TOF: Verzögerungstimer in IEC 61131-3 und 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/FB_TOF-und-E_TOF-Verzgerungstimer-in-IEC-61131-3-und-61499-e368e2d)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020g.png)


## Ziel der Übung

Verwendung des Bausteins `E_TONOF`, der sowohl eine Einschalt- als auch eine Ausschaltverzögerung in einem Gehäuse bietet.

-----

## Funktionsweise

[cite_start]Der Baustein reagiert auf den Pegel am Eingang `IN`[cite: 1]:
*   Wechsel zu `TRUE`: Der Ausgang wird erst nach Ablauf von `PT_ON` (5s) aktiv.
*   Wechsel zu `FALSE`: Der Ausgang bleibt noch für die Zeit `PT_OFF` (5s) aktiv.

Dies filtert kurze Impulse (Störungen) am Eingang komplett heraus und sorgt gleichzeitig für einen definierten Nachlauf.