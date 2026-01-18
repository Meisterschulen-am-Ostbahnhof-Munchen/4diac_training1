# Uebung_012a: Modulare Speicherung (Typed SubApp)

```{index} single: Uebung_012a: Modulare Speicherung (Typed SubApp)
```

[Uebung_012a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_012a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_012a`. Hier wird die persistente Speicherung aus Übung 012 in eine wiederverwendbare Sub-Applikation gekapselt.


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Der E_T_FF in IEC 61499: Modulares Kippen für die Industrie 4.0](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF-in-IEC-61499-Modulares-Kippen-fr-die-Industrie-4-0-e3674m7)
* [DIN EN 61499-1 Entschlüsselt: Der Bauplan für modulare, verteilte Steuerungssysteme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entschlsselt-Der-Bauplan-fr-modulare--verteilte-Steuerungssysteme-e367nmj)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
* [ISOBUS nachrüsten: Kabelsalat war gestern – Die modulare Lösung für Ihre Agrartechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/ISOBUS-nachrsten-Kabelsalat-war-gestern--Die-modulare-Lsung-fr-Ihre-Agrartechnik-e3767p4)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_012a.png)


## Übersicht

[cite_start]Die Subapplikation `Uebung_012a.SUB` nutzt den Sub-App-Typ `Uebung_012a_sub`, um die Speicher-Logik modular bereitzustellen[cite: 1]. Der Baustein `CbVtStatus` bleibt auf der obersten Ebene, um die gesamte Seite bei Bedarf zu aktualisieren.

### Typisierte Sub-Applikation: `Uebung_012a_sub`

[cite_start]Dieser Baustein bündelt die Eingabe via `NumericValue_ID`, die Konvertierung, den NVS-Zugriff und die Anzeige-Rückführung[cite: 2]. Er stellt Schnittstellen für den Speicher-Schlüssel (`KEY`) und die Objekt-ID (`u16ObjId`) zur Verfügung.

Dies ermöglicht es, viele verschiedene Einstellwerte (z.B. Druck, Durchfluss, Zeit) sehr schnell und übersichtlich in das Programm zu integrieren, ohne jedes Mal das komplexe Netzwerk aus Übung 012 neu zeichnen zu müssen.