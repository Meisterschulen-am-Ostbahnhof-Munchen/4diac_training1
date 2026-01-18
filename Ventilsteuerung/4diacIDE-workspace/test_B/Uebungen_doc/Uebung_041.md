# Uebung_041: Ein-Tasten-Lauflicht (Zähler-Steuerung)

```{index} single: Uebung_041: Ein-Tasten-Lauflicht (Zähler-Steuerung)
```

[Uebung_041](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_041.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_041`. Hier wird die manuelle Steuerung einer 8-stufigen Schrittkette auf einen einzigen Taster reduziert.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
* [Eclipse 4diac FORTE: IEC 61499 verstehen – Der LEGO®-Baukasten für Ihre Industrie 4.0 Steuerung](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-FORTE-IEC-61499-verstehen--Der-LEGO-Baukasten-fr-Ihre-Industrie-4-0-Steuerung-e3682kc)
* [Eclipse 4diac: Open Source als Game Changer für industrielle Steuerungen?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Open-Source-als-Game-Changer-fr-industrielle-Steuerungen-e372eru)
* [DIN EN 61499-1 Entschlüsselt: Der Bauplan für modulare, verteilte Steuerungssysteme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entschlsselt-Der-Bauplan-fr-modulare--verteilte-Steuerungssysteme-e367nmj)
* [DIN EN 61499-1: Die Lego-Steine für flexible und ereignisgesteuerte Industriesteuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Die-Lego-Steine-fr-flexible-und-ereignisgesteuerte-Industriesteuerungen-e3681o1)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_041.png)


## Ziel der Übung

Optimierung der Bedienlogik aus Übung 040. Es wird gezeigt, wie man durch die Kombination von Zähler (`E_CTU`) und Demultiplexer (`E_DEMUX_8`) alle Phasen einer Schrittkette mit nur einer einzigen Taste nacheinander durchschalten kann.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_041.SUB` wird ein zentraler Ereignispfad genutzt, um den Sequenzer `sequence_E_08_loop` anzusteuern[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Start)**: Setzt die Sequenz auf den ersten Schritt.
  * **`I2` (Step)**: Der einzige Taster zum Weiterschalten.
  * **`E_CTU_0`**: Zählt die Klicks auf `I2`.
  * **`E_DEMUX_0`**: Leitet das Klick-Ereignis basierend auf dem Zählerstand an den passenden Transitions-Eingang der Schrittkette weiter.
  * **`I4` (Reset)**: Löscht sowohl die Schrittkette als auch den Zähler.

-----

## Funktionsweise

1.  **Initialisierung**: Ein Klick auf **I1** startet das Lauflicht bei `Q1`.
2.  **Manueller Durchlauf**: Jeder Klick auf **I2** erhöht den internen Zähler. Der Demultiplexer sorgt dafür, dass das erste Event an `S1_S2` geht, das zweite an `S2_S3` und so weiter.
3.  **Überlauf**: Nach dem 8. Schritt setzt sich die Logik automatisch zurück und beginnt (beim nächsten Klick) wieder von vorn.

Dies ermöglicht eine vollständige Prozesskontrolle mit minimaler Hardware-Anforderung.

-----

## Anwendungsbeispiel

**Sequenzielle Menüführung**:
Ein einziger Knopf am Joystick dient zum Durchblättern von 8 verschiedenen Betriebsmodi. Jede Betätigung schaltet eine Stufe weiter und aktiviert den entsprechenden Aktor oder Parameter-Satz.