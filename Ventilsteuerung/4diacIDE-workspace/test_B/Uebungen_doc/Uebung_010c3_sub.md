# Uebung_010c3_sub: Softkey mit Feedback (SubApp)

```{index} single: Uebung_010c3_sub: Softkey mit Feedback (SubApp)
```

[Uebung_010c3_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010c3_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## 🎧 Podcast

* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)

## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Übersicht

[cite_start]Dieser Sub-App-Typ kombiniert eine Softkey-Eingabe mit einem automatischen visuellen Feedback auf dem Terminal[cite: 1].
Er bündelt die Bausteine `Softkey_IX`, `GreenWhiteBackground` und `DigitalOutput_QX`. Der Anwender muss lediglich die `u16ObjId` des Softkeys und den physischen `Output` angeben. Der Baustein stellt sicher, dass bei jeder Betätigung sowohl der Hardware-Ausgang geschaltet als auch der Hintergrund des Softkeys am Terminal farblich (Grün/Weiß) angepasst wird. Dies reduziert den Projektierungsaufwand bei komplexen Bedienoberflächen erheblich.