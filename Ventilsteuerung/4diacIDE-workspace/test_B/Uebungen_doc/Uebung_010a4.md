# Uebung_010a4: Softkey auf externes CAN-Modul

```{index} single: Uebung_010a4: Softkey auf externes CAN-Modul
```

[Uebung_010a4](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010a4.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010a4`.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Der E_T_FF in IEC 61499: Modulares Kippen für die Industrie 4.0](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF-in-IEC-61499-Modulares-Kippen-fr-die-Industrie-4-0-e3674m7)
* [DIN EN 61499-1 Entschlüsselt: Der Bauplan für modulare, verteilte Steuerungssysteme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entschlsselt-Der-Bauplan-fr-modulare--verteilte-Steuerungssysteme-e367nmj)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
* [DIN EN 61499: Industrielle Steuerungen modular und ereignisbasiert mit Funktionsbausteinen meistern – Der ESR-Schalter im Fokus](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-Industrielle-Steuerungen-modular-und-ereignisbasiert-mit-Funktionsbausteinen-meistern--Der-ESR-Schalter-im-Fokus-e367nra)
* [Modul 00 - Beweggründe und Ursprünge](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Modul-00---Beweggrnde-und-Ursprnge-e3671op)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010a4.png)


## Ziel der Übung

Kombination verschiedener logiBUS-Teilsysteme.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010a4.SUB` verbindet einen ISOBUS-Softkey mit einem physikalischen Ausgang eines DataPanels[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_F1`**: Eingabequelle vom Traktor-Terminal.
  * **`DigitalOutput_Q1`**: Typ `DataPanel_MI_QX`. Dies ist ein Ausgang auf einer dezentralen IO-Box am CAN-Bus.

-----

## Funktionsweise

Diese Übung verdeutlicht die Mächtigkeit der IEC 61499 Abstraktion: Für die Programmlogik ist es völlig unerheblich, woher ein Signal kommt (Software-Terminal) oder wohin es geht (CAN-Modul). Die Ereignis- und Datenverbindungen überbrücken die Protokollgrenzen zwischen ISOBUS und gerätespezifischem CAN-Protokoll nahtlos.