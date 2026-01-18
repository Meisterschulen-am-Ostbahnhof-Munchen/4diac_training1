# Uebung_122: Netzwerk-Scan (16 Teilnehmer)

```{index} single: Uebung_122: Netzwerk-Scan (16 Teilnehmer)
```

[Uebung_122](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_122.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_122`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Industrielle Netzwerke: Das Nervensystem der modernen Fabrik – OT, IT & die Zukunft der Automatisierung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Industrielle-Netzwerke-Das-Nervensystem-der-modernen-Fabrik--OT--IT--die-Zukunft-der-Automatisierung-e375g9g)
* [Open Source in der Industrie: Mehr als Code – Ein Netzwerk für Innovation und Kollaboration](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Open-Source-in-der-Industrie-Mehr-als-Code--Ein-Netzwerk-fr-Innovation-und-Kollaboration-e372av2)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_122.png)


## Übersicht

[cite_start]Diese Übung demonstriert die Erfassung einer größeren Anzahl von Bus-Teilnehmern[cite: 1].
Unter Verwendung des Bausteins `LOG_16` werden die Namen von bis zu 16 verschiedenen Control Functions im Netzwerk gleichzeitig gepuffert und analysiert. Für jeden Teilnehmer wird über eine Kette von `NmSetNameField` Bausteinen eine detaillierte Analyse der Identität durchgeführt. Dies ist ein Werkzeug für komplexe Diagnosesysteme, die den gesamten Geräteverbund eines Gespanns überwachen müssen.