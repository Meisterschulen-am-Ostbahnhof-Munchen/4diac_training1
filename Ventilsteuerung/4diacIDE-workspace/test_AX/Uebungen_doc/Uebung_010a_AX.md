# Uebung_010a_AX: SoftKey_F1/_F2 auf DigitalOutput_Q1/_Q2

```{index} single: Uebung_010a_AX: Zwei Softkeys (Parallel)
```

[Uebung_010a_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010a_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010a_AX`.

## 🎧 Podcast

* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)

----

![](Uebung_010a_AX.png)

## Ziel der Übung

Erweiterung auf mehrere Softkeys.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010a_AX.SUB` steuert zwei Ausgänge über zwei Softkeys[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_F1`** -> **`DigitalOutput_Q1`**
  * **`SoftKey_F2`** -> **`DigitalOutput_Q2`**

-----

## Funktionsweise

Zwei unabhängige Signalpfade. Zeigt, dass man beliebig viele Softkeys instanziieren kann, solange sie im Objekt-Pool definiert sind.