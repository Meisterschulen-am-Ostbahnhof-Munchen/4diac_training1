# Uebung_006a3_sub: Richtungs-Merker (SubApp)

```{index} single: Uebung_006a3_sub: Richtungs-Merker (SubApp)
```

[Uebung_006a3_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a3_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_006a3_sub`. Er dient als interner Zustandsautomat zur Realisierung eines alternierenden Richtungswechsels.


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



## Übersicht

[cite_start]Dieser Baustein kapselt die Logik für eine Links/Rechts-Umschaltung[cite: 1].
Er verfügt über einen Ereignis-Eingang `EI`. Bei jedem Eintreffen eines Ereignisses wechselt der Baustein intern seine Richtungsvorgabe. Die Ergebnisse werden über die Daten-Ausgänge `Links` und `Rechts` bereitgestellt.
Dies wird in der Übung 006a3 genutzt, um einen Motor bei jedem Startvorgang automatisch in die jeweils andere Richtung drehen zu lassen. Der Baustein stellt dabei sicher, dass immer eine eindeutige Richtungsentscheidung vorliegt.