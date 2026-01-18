# Uebung_003d: Wiederholung Parallelsteuerung

```{index} single: Uebung_003d: Wiederholung Parallelsteuerung
```

[Uebung_003d](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003d.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_003d`. Diese Übung ist strukturell identisch mit `Uebung_003` und dient der Festigung des Verständnisses für parallele Signalpfade in der IEC 61499.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_003d.png)


## Ziel der Übung

Das Ziel ist die Wiederholung der direkten I/O-Verknüpfung mittels Ereignis- und Datenverbindungen. Es wird sichergestellt, dass das Konzept der asynchronen und unabhängigen Datenflüsse verstanden wurde.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_003d.SUB` verbindet zwei Eingangsbausteine direkt mit zwei Ausgangsbausteinen[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`** ➡️ **`DigitalOutput_Q1`**
  * **`DigitalInput_I2`** ➡️ **`DigitalOutput_Q2`**

Die Bausteintypen sind `logiBUS_IX` (Eingang) und `logiBUS_QX` (Ausgang).

-----

## Funktionsweise

Die Signale werden 1:1 und latenzarm von den Eingängen auf die Ausgänge durchgeschleift. Jede Änderung am Eingang `I1` löst sofort eine Aktualisierung von `Q1` aus, ohne dass die Logik für `I2`/`Q2` davon beeinflusst wird.

-----

## Anwendungsbeispiel

Diese Übung eignet sich hervorragend als **Verdrahtungstest-Programm**:
Wenn eine neue Hardware-Konfiguration aufgebaut wurde, lädt man dieses "transparente" Programm hoch, um zu prüfen, ob alle Taster und Lampen physikalisch korrekt angeschlossen und adressiert sind. Ein Druck auf den Taster muss die zugehörige Lampe unmittelbar zum Leuchten bringen.