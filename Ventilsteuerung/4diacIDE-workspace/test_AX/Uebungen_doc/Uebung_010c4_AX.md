# Uebung_010c4_AX: Mehrfachnutzung Smart Softkey

```{index} single: Uebung_010c4_AX: Mehrfachnutzung Smart Softkey
```

[Uebung_010c4_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010c4_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010c4_AX`.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [DIN EN 61499-1: Der digitale Lego-Baukasten für flexible Automatisierung und smarte Zukunft](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Der-digitale-Lego-Baukasten-fr-flexible-Automatisierung-und-smarte-Zukunft-e3681pb)
* [Industrielle Automation verstehen: SPS, PLS, SCADA, MES und ERP entschlüsselt – Eine Reise durch die Smart Factory](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Industrielle-Automation-verstehen-SPS--PLS--SCADA--MES-und-ERP-entschlsselt--Eine-Reise-durch-die-Smart-Factory-e3671qn)
* [Anatomy of a Smart Machine](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Anatomy-of-a-Smart-Machine-e3a9qvt)
* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)
* [logiBUS®: Revolutioniert die Agrar-IT – So wird ISOBUS zum Smart Home für Landwirte](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-Revolutioniert-die-Agrar-IT--So-wird-ISOBUS-zum-Smart-Home-fr-Landwirte-e3674sl)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010c4_AX.png)


## Ziel der Übung

Beweis der Wiederverwendbarkeit.

-----

## Beschreibung

[cite_start]Die Subapplikation `Uebung_010c4_AX.SUB` instanziiert den Typ `Uebung_010c4_sub_AX` (vermutlich identisch zu c3) zweimal[cite: 1].
*   Instanz 1: F1 auf Q1.
*   Instanz 2: F2 auf Q2.

Beide Softkeys haben nun automatisch die "Grün-bei-Druck"-Logik integriert.