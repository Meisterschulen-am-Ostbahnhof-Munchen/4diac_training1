# Uebung_006b: Speicherglied (RS-Flip-Flop)

```{index} single: Uebung_006b: Speicherglied (RS-Flip-Flop)
```

[Uebung_006b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006b`.


## 📺 Video

* [RS-Flip-Flop Baustein E_RS aus der IEC 61499 (Übung 006b)](https://www.youtube.com/watch?v=GXOe8K7Jgr0)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006b.png)


## Ziel der Übung

Verständnis der Reset-Priorität.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006b.SUB` nutzt einen `E_RS` Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_RS`**: Ein ereignisbasiertes RS-Flip-Flop (Reset dominant).

-----

## Funktionsweise

Funktional sehr ähnlich zum SR-Speicher (Übung 006). Der entscheidende Unterschied liegt im Verhalten bei "Gleichzeitigkeit": Sollten im exakt gleichen Moment sowohl ein Setz- als auch ein Rücksetz-Ereignis eintreffen, gewinnt beim `E_RS` das **Rücksetzen**. Der Ausgang wird also sicher auf `FALSE` geschaltet.

-----

## Anwendungsbeispiel

**Gefahrenabschaltung**: Bei einer Maschine hat der Stopp-Befehl immer Vorrang. Wenn ein Fehlerzustand den Stopp auslöst, darf ein gleichzeitiger Startversuch des Bedieners die Abschaltung nicht verhindern. Hier ist ein RS-Glied zwingend erforderlich.