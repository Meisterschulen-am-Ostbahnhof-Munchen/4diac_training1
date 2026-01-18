# Uebung_049: Mehrkanal-Mapping (Standard)

```{index} single: Uebung_049: Mehrkanal-Mapping (Standard)
```

[Uebung_049](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_049.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_049`. Diese Übung dient der Übung von umfangreichen Punkt-zu-Punkt-Verbindungen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-08-17 14-05-25 Vorstellung logiBUS® neues IO System ohne Mapping](https://www.youtube.com/watch?v=5YnRsE5zVBk)
* [2025-08-17 14-39-09 logiBUS® Umwandeln eines Projektes mit Mapping in eines ohne Mapping.](https://www.youtube.com/watch?v=w8nTLn8fQxQ)

## Podcast
* [4diac IDE: Wie der IEC 61499 Standard die Industrieautomatisierung revolutioniert](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Wie-der-IEC-61499-Standard-die-Industrieautomatisierung-revolutioniert-e36756a)
* [IEC 61499 vs. 61131: Brauchen wir einen neuen Standard für IIoT? Analyse einer hitzigen Debatte um Verteilte Intelligenz](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-vs--61131-Brauchen-wir-einen-neuen-Standard-fr-IIoT--Analyse-einer-hitzigen-Debatte-um-Verteilte-Intelligenz-e3ahc2r)
* [IEC 61499: Befreit der neue Standard die Industrieautomation? Ein Vergleich mit 61131 und die Brücke zwischen OT & IT.](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Befreit-der-neue-Standard-die-Industrieautomation--Ein-Vergleich-mit-61131-und-die-Brcke-zwischen-OT--IT-e368446)
* [IEC 61499: Revolution der Industrieautomation – Warum der neue Standard Ihre Systeme fit für die Zukunft macht](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Industrieautomation--Warum-der-neue-Standard-Ihre-Systeme-fit-fr-die-Zukunft-macht-e375evm)
* [Das Alarm Mask Objekt: Dein standardisierter Wachposten für Warnungen auf Landmaschinen](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Das-Alarm-Mask-Objekt-Dein-standardisierter-Wachposten-fr-Warnungen-auf-Landmaschinen-e36e6c3)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_049.png)


## Übersicht

[cite_start]In `Uebung_049.SUB` werden vier digitale Eingänge (`I1` bis `I4`) direkt auf vier digitale Ausgänge (`Q1` bis `Q4`) gemappt[cite: 1]. Dies ist die Basisform der Signalweiterleitung ohne Logik oder Strukturierung, bei der jeder Kanal über eigene Event- und Data-Connections verfügt. Es dient primär dem Training der manuellen Verdrahtung in der 4diac-IDE.