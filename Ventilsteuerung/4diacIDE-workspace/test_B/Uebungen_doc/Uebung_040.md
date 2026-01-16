# Uebung_040: Manuelle Schrittwahl (Zähler & Demux)

[Uebung_040](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_040.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_040`. Hier wird eine raffinierte Methode gezeigt, um eine 8-stufige Schrittkette mit nur wenigen Tastern manuell durchzuschalten.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_040.png)


## Ziel der Übung

Kombination von Ereignis-Zählern (`E_CTU`) und Ereignis-Demultiplexern (`E_DEMUX`) zur Steuerung einer Ablaufkette.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_040.SUB` nutzt zwei Zähler-Zweige, um die Ereignis-Eingänge des Sequenzers `sequence_E_08_loop` zu bedienen[cite: 1].

### Funktionsweise

1.  **Start**: Taster **I1** setzt die Kette auf Anfang (Schritt 1).
2.  **Steppen 1-4**: Jeder Klick auf Taster **I2** erhöht den ersten Zähler. Der Demultiplexer leitet das Klick-Event nacheinander an die Eingänge `S1_S2`, `S2_S3` etc. weiter. Der Nutzer "klickt" sich also durch die ersten vier Phasen.
3.  **Steppen 5-8**: Taster **I3** übernimmt analog die Steuerung für die zweite Hälfte der Kette.
4.  **Zähler-Reset**: Sobald ein Demultiplexer den letzten Ausgang erreicht hat, setzt er seinen zugehörigen Zähler automatisch wieder auf Null zurück.

Dies ist eine sehr effiziente Methode, um komplexe manuelle Abläufe auf kleinstem Raum (wenige Bedienelemente) abzubilden.
