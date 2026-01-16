# Uebung_012a: Modulare Speicherung (Typed SubApp)

[Uebung_012a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_012a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_012a`. Hier wird die persistente Speicherung aus Übung 012 in eine wiederverwendbare Sub-Applikation gekapselt.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_012a.png)


## Übersicht

[cite_start]Die Subapplikation `Uebung_012a.SUB` nutzt den Sub-App-Typ `Uebung_012a_sub`, um die Speicher-Logik modular bereitzustellen[cite: 1]. Der Baustein `CbVtStatus` bleibt auf der obersten Ebene, um die gesamte Seite bei Bedarf zu aktualisieren.

### Typisierte Sub-Applikation: `Uebung_012a_sub`

[cite_start]Dieser Baustein bündelt die Eingabe via `NumericValue_ID`, die Konvertierung, den NVS-Zugriff und die Anzeige-Rückführung[cite: 2]. Er stellt Schnittstellen für den Speicher-Schlüssel (`KEY`) und die Objekt-ID (`u16ObjId`) zur Verfügung.

Dies ermöglicht es, viele verschiedene Einstellwerte (z.B. Druck, Durchfluss, Zeit) sehr schnell und übersichtlich in das Programm zu integrieren, ohne jedes Mal das komplexe Netzwerk aus Übung 012 neu zeichnen zu müssen.
