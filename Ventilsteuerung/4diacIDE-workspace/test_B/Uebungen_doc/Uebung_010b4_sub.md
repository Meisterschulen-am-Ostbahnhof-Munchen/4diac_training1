# Uebung_010b4_sub: Softkey-Mapping-Einheit (SubApp)

```{index} single: Uebung_010b4_sub: Softkey-Mapping-Einheit (SubApp)
```

[Uebung_010b4_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b4_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## 🎧 Podcast

* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)
* [From "Mass Errors" to Masterpiece: Streamlining Industrial Software by Eliminating Mapping](https://podcasters.spotify.com/pod/show/logibus/episodes/From-Mass-Errors-to-Masterpiece-Streamlining-Industrial-Software-by-Eliminating-Mapping-e3759t4)
* [Logibus Revolution: Unpacking the "No Mapping" Future and Streamlined Development](https://podcasters.spotify.com/pod/show/logibus/episodes/Logibus-Revolution-Unpacking-the-No-Mapping-Future-and-Streamlined-Development-e375aph)
* [Logibus Unleashed: How Eliminating "Mapping" Simplifies Complex Systems and Boosts Usability](https://podcasters.spotify.com/pod/show/logibus/episodes/Logibus-Unleashed-How-Eliminating-Mapping-Simplifies-Complex-Systems-and-Boosts-Usability-e375a3m)
* [logiBUS's No-Mapping Revolution: Untangling Industrial Control and User Experience](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUSs-No-Mapping-Revolution-Untangling-Industrial-Control-and-User-Experience-e375aa2)

## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-08-17 14-05-25 Vorstellung logiBUS® neues IO System ohne Mapping](https://www.youtube.com/watch?v=5YnRsE5zVBk)

## Übersicht

[cite_start]Dieser Sub-App-Typ dient der strukturierten Anbindung von ISOBUS-Softkeys an Hardware-Ausgänge[cite: 1].
Er bündelt eine `Softkey_IX` Instanz und einen `DigitalOutput_QX` Baustein. Über die Parameter `u16ObjId` und `Output` kann die Zuordnung zwischen virtuellem Button und physischer Lampe/Ventil direkt an der Sub-App vorgenommen werden. Dies ermöglicht den Aufbau von großen Bedien-Matrizen (wie in Übung 010b4 gezeigt) mit minimalem Verdrahtungsaufwand im Hauptdiagramm.