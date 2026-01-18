# Uebung_039: Hydraulik-Ventilsteuerung

```{index} single: Uebung_039: Hydraulik-Ventilsteuerung
```

[Uebung_039](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_039.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_039`. Diese Übung ist speziell auf die Ansteuerung von hydraulischen oder pneumatischen Wegeventilen zugeschnitten.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Außenzahnradmaschinen: Vom Arbeitstier zur Intelligenz der Hydraulik – Herausforderungen, Innovationen & Keplers Erbe](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Auenzahnradmaschinen-Vom-Arbeitstier-zur-Intelligenz-der-Hydraulik--Herausforderungen--Innovationen--Keplers-Erbe-e36opo0)
* [Danfoss und Eaton Hydraulik Zwillingsgeschichte endet](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Danfoss-und-Eaton-Hydraulik-Zwillingsgeschichte-endet-e3bgpv9)
* [Der unterschätzte Held: Warum der Ölbehälter Ihr Hydrauliksystem revolutioniert](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-unterschtzte-Held-Warum-der-lbehlter-Ihr-Hydrauliksystem-revolutioniert-e373nm0)
* [Druckbegrenzungsventile: Lebensversicherung der Hydraulik – Arten, Funktion und Systemintegration](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Druckbegrenzungsventile-Lebensversicherung-der-Hydraulik--Arten--Funktion-und-Systemintegration-e373nal)
* [Kraftpakete im Einsatz: Das Geheimnis der Hydraulikzylinder – Von Baggern bis Hightech-Maschinen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Kraftpakete-im-Einsatz-Das-Geheimnis-der-Hydraulikzylinder--Von-Baggern-bis-Hightech-Maschinen-e373ne8)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_039.png)


## Ziel der Übung

Realisierung einer komplexen Spiegelabfolge. Im Gegensatz zu einfachen Zylindern müssen bei Wegeventilen oft Zustände gehalten werden (Mittelstellung gesperrt), was eine präzise zeitliche und ereignisbasierte Steuerung der Spulen erfordert.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_039.SUB` nutzt einen 5-Schritt-Sequenzer (`sequence_ET_05`)[cite: 1].
Die Ansteuerung der Hardware erfolgt hier über typisierte Sub-Applikationen (`Uebung_039_sub_Outputs`), die den jeweiligen Ventilzustand auch visuell auf dem ISOBUS-Terminal durch Farbumschlag der zugehörigen Softkeys rückmelden.

-----

## Funktionsweise

Die Kette wird manuell durch physische Taster (`I1` bis `I4`) gesteuert, wobei ein zentraler Zeitschritt (5s bei `DT_S3_S4`) eine automatische Sicherheits- oder Wartephase einfügt. Dies zeigt die Kombination aus freier Bedienbarkeit und erzwungenen Prozesszeiten.