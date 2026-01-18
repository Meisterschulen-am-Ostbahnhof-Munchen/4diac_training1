# Uebung_020f2: Zyklischer Impulsgeber (FB_TP)

```{index} single: Uebung_020f2: Zyklischer Impulsgeber (FB_TP)
```

[Uebung_020f2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f2`. Hier wird der klassische IEC 61131-3 Timer-Baustein `FB_TP` verwendet.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020f2.png)


## Übersicht

Diese Übung implementiert einen Impulsgeber unter Verwendung des klassischen `FB_TP` Bausteins. Da dieser Baustein für eine zyklische SPS-Umgebung entworfen wurde, muss in der ereignisbasierten IEC 61499 ein `E_CYCLE` zur regelmäßigen Triggerung genutzt werden.

## Funktionsweise

1.  **Trigger**: Die steigende Flanke von `Input_I1` startet über einen `E_SWITCH` den Taktgeber `E_CYCLE`.
2.  **Berechnung**: Der `E_CYCLE` triggert alle 500ms den `REQ`-Eingang des `FB_TP`. Nur so kann der Timer intern die Zeit hochzählen und den Ausgang `ET` (Elapsed Time) aktualisieren.
3.  **Abschluss**: Sobald der Impuls beendet ist (`Q` geht auf `FALSE`), stoppt der `E_CYCLE` automatisch, um unnötige CPU-Last zu vermeiden.

-----

## Vergleich zur AX-Variante

Im Gegensatz zur `AX_FB_TP` Variante (Übung 020f2_AX) werden hier klassische boolesche Ein- und Ausgänge verwendet, anstatt auf die flexibleren AX-Adapter zu setzen. Die zugrunde liegende Problematik des zyklischen Aufrufs bleibt jedoch identisch.