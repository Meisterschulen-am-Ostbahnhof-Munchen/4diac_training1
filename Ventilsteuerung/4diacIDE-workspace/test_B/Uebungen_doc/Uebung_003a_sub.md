# Uebung_003a_sub: Universal-Kanal (SubApp)

```{index} single: Uebung_003a_sub: Universal-Kanal (SubApp)
```

[Uebung_003a_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003a_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_003a_sub`. Dieser Baustein dient als wiederverwendbare Vorlage für die 1:1 Verbindung eines digitalen Eingangs mit einem digitalen Ausgang.


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Universal Automation: So entkoppeln Sie Software und Hardware für die Zukunft der Industrie](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Universal-Automation-So-entkoppeln-Sie-Software-und-Hardware-fr-die-Zukunft-der-Industrie-e36849a)
* [Unlocking Universal Automation: The IEC 61499 Revolution from Factory Floors to the Seas](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Unlocking-Universal-Automation-The-IEC-61499-Revolution-from-Factory-Floors-to-the-Seas-e376p9m)
* [ISOBUS revolutioniert Landwirtschaft Universal Terminal Task Controller](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/ISOBUS-revolutioniert-Landwirtschaft-Universal-Terminal-Task-Controller-e3b8omh)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



## Ziel der Übung

Kapselung der logiBUS I/O-Logik. Durch die Erstellung eines eigenen Typs wird die Komplexität der Einzelverbindungen nach außen hin verborgen. Der Anwender muss nur noch die Hardware-IDs zuweisen.

-----

## Beschreibung und Komponenten

[cite_start]Der Typ `Uebung_003a_sub` bündelt einen Eingangs- und einen Ausgangsbaustein[cite: 1].

### Interne Funktionsbausteine (FBs)

  * **`IX`**: Typ `logiBUS_IX`. Liest den über den Parameter `Input` zugewiesenen Hardware-Pin ein.
  * **`QX`**: Typ `logiBUS_QX`. Schaltet den über den Parameter `Output` zugewiesenen Hardware-Pin.

-----

## Schnittstellen

[cite_start]Der Baustein verfügt über zwei Konfigurations-Eingänge[cite: 1]:
*   **`Input`**: Erwartet eine Konstante vom Typ `logiBUS_DI_S` (z.B. `Input_I1`).
*   **`Output`**: Erwartet eine Konstante vom Typ `logiBUS_DO_S` (z.B. `Output_Q1`).

Intern sind die Ereignis-Ports (`IND -> REQ`) und die Daten-Ports (`IN -> OUT`) fest miteinander verbunden. Sobald dieser Typ in einem Projekt platziert wird, arbeitet er völlig autark für den zugewiesenen Hardware-Kanal.