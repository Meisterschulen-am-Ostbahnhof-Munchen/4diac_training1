# Uebung_033_sub: Modularer RGB-Kanal (SubApp)

```{index} single: Uebung_033_sub: Modularer RGB-Kanal (SubApp)
```

[Uebung_033_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_033_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_033_sub`. Er dient als wiederverwendbares Modul zur Steuerung von farbigen LED-Anzeigen.


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

[cite_start]Dieser Baustein bündelt einen digitalen Eingangsbaustein (`IX`) und einen spezialisierten RGB-Streifen-Ausgang (`logiBUS_LED_strip_QX`)[cite: 1].
Er stellt Parameter für die Wahl des Eingangs-Buttons (`Input`), der Farbe (`Colour`) und des Ausgangs-Kanals (`Output`) bereit. Intern ist er auf eine feste Blinkfrequenz von 1 Hz voreingestellt. Durch die Kapselung dieser komplexen Treiber-Logik können farbige Status-Anzeigen in Projekten sehr einfach durch Parametrierung statt durch aufwendige Einzelverdrahtung realisiert werden.