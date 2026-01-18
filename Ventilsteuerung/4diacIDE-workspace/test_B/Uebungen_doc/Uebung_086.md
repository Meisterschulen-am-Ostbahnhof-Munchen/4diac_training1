# Uebung_086: Ereignis-Weiche (E_SWITCH)

```{index} single: Uebung_086: Ereignis-Weiche (E_SWITCH)
```

[Uebung_086](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_086.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_086`.

## 📺 Video

* [Ereignisschalter E_SWITCH aus der IEC 61499 (Übung 86)](https://www.youtube.com/watch?v=Gev-kGR4-Tc)
* [Das Relais im Detail: Schaltverstärker, Schutz und die Geheimnisse von A1/A2, 85/86 und der Hyste...](https://www.youtube.com/watch?v=OUNlE4NABX4)
* [Das Technologie-Panorama von 1863: Lanz & Comp. und die Revolution der deutschen Landwirtschaft d...](https://www.youtube.com/watch?v=ShV0oAGoY58)
* [Der Katalog von 1863](https://www.youtube.com/watch?v=fk7tIjl2pTk)

## 🎧 Podcast

* [Das Relais im Detail: Schaltverstärker, Schutz und die Geheimnisse von A1/A2, 85/86 und der Hysterese](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-Relais-im-Detail-Schaltverstrker--Schutz-und-die-Geheimnisse-von-A1A2--8586-und-der-Hysterese-e3audsc)
* [Das Technologie-Panorama von 1863: Lanz & Comp. und die Revolution der deutschen Landwirtschaft durch Import, Innovation und Guano](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-Technologie-Panorama-von-1863-Lanz--Comp--und-die-Revolution-der-deutschen-Landwirtschaft-durch-Import--Innovation-und-Guano-e39auqa)

----

![](Uebung_086.png)

## Übersicht

[cite_start]Verwendung des fundamentalen Bausteins `E_SWITCH`[cite: 1].
In dieser Übung wird demonstriert, wie ein Ereignis-Strom (`EI`) basierend auf einem logischen Zustand (`G`) auf zwei verschiedene Pfade aufgeteilt wird.
*   Ist der Schalter `I1` auf `FALSE`, landet das `IND`-Ereignis am Ausgang `EO0`.
*   Ist der Schalter `I1` auf `TRUE`, landet das `IND`-Ereignis am Ausgang `EO1`.
Dies ist die Basis für jede bedingte Programmausführung ("If-Then-Else") in der IEC 61499.