# Uebung_020g_AX: Ein- und Ausschaltverzögerung (TONOF)

```{index} single: Uebung_020g_AX: Ein- und Ausschaltverzögerung (TONOF)
```

[Uebung_020g_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020g_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020g_AX`. Hier wird der kombinierte Verzögerungsbaustein `AX_TONOF` verwendet.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020g_AX.png)


## Ziel der Übung

Das Ziel ist es, ein Signal in beide Richtungen zeitlich zu filtern. Kurze Impulse (sowohl positive als auch negative) werden ignoriert. Nur wenn ein Zustand länger als die definierte Zeit stabil anliegt, wird er an den Ausgang weitergegeben.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020g_AX.SUB` nutzt den Baustein `AX_TONOF`[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Typ `logiBUS_IXA`.
  * **`AX_TONOF`**: [cite_start]Vereint Einschaltverzögerung (`PT_ON`) und Ausschaltverzögerung (`PT_OFF`) in einem Baustein. Hier sind beide Zeiten auf 5 Sekunden eingestellt[cite: 1].
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`.

-----

## Funktionsweise

1.  **Einschalten**: Wird `I1` gedrückt, passiert am Ausgang zunächst nichts. Erst nach **5 Sekunden** dauerhaften Drückens schaltet `Q1` ein.
2.  **Ausschalten**: Wird `I1` losgelassen, bleibt `Q1` zunächst an. Erst nach **5 Sekunden** im losgelassenen Zustand schaltet `Q1` aus.

Kurzes Antippen (< 5s) führt nicht zum Einschalten. Kurzes Loslassen (< 5s) führt nicht zum Ausschalten.

-----

## Anwendungsbeispiel

**Füllstandsüberwachung**: Ein Schwimmerschalter in einem Tank, in dem das Medium schwappt. Die Pumpe soll erst einschalten, wenn der Sensor 5 Sekunden lang "Leer" meldet, und erst ausschalten, wenn er 5 Sekunden lang "Voll" meldet. Dies verhindert ein nervöses Flattern der Pumpe bei Wellenbewegungen.