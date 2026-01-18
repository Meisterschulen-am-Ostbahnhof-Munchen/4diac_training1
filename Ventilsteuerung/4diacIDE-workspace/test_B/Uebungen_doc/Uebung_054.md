# Uebung_054: Signal-Vektoren (Arrays)

```{index} single: Uebung_054: Signal-Vektoren (Arrays)
```

[Uebung_054](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_054.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_054`. Dies ist die dritte Methode der Signalbündelung: Die Verwendung von Feldern (Arrays).


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [R_TRIG & F_TRIG: So erkennen SPS-Steuerungen Signalflanken zuverlässig – ohne Doppelbehandlung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/R_TRIG--F_TRIG-So-erkennen-SPS-Steuerungen-Signalflanken-zuverlssig--ohne-Doppelbehandlung-e370kqh)
* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)
* [logiBUS® verstehen: Direkte Signalweiterleitung – Das "Hallo Welt" der Automatisierung](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg)
* [Das tödliche Dilemma des Relais: Warum Silberkontakte bei Kleinsignalen versagen und Gold bei Last schmilzt – Der Freibrenn-Effekt erklärt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-tdliche-Dilemma-des-Relais-Warum-Silberkontakte-bei-Kleinsignalen-versagen-und-Gold-bei-Last-schmilzt--Der-Freibrenn-Effekt-erklrt-e3a9lhv)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_054.png)


## Ziel der Übung

Verwendung von `BOOLS_TO_ARR08X` und `ARR08X_TO_BOOLS`.

-----

## Beschreibung

[cite_start]In `Uebung_054.SUB` werden vier Digitalsignale in ein Array (eine indizierte Liste von Werten) verpackt[cite: 1].
Im Gegensatz zur Struktur (wo jeder Kanal einen Namen hat, z.B. `X_00`) greift man bei einem Array über die Position (Index 0 bis 7) auf die Daten zu. Dies ist besonders vorteilhaft, wenn Signalpfade in Programmschleifen verarbeitet werden sollen.