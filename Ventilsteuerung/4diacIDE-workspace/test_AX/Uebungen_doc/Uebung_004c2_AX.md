# Uebung_004c2_AX: Langer Tastendruck (Start)

```{index} single: Uebung_004c2_AX: Langer Tastendruck (Start)
```

[Uebung_004c2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c2_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c2_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Ereignisse und IEC 61499: Der Startschuss für intelligente Systeme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Ereignisse-und-IEC-61499-Der-Startschuss-fr-intelligente-Systeme-e368461)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c2_AX.png)


## Ziel der Übung

Nutzung des Ereignisses `BUTTON_LONG_PRESS_START`.

-----

## Funktionsweise

[cite_start]Der Baustein `DigitalInput_CLK_I1` in `Uebung_004c2_AX.SUB` ist auf `BUTTON_LONG_PRESS_START` konfiguriert[cite: 1].

Das Event `IND` wird gefeuert, sobald der Taster eine bestimmte Zeit lang gedrückt *gehalten wurde* (z.B. > 500ms). Es feuert genau in dem Moment, in dem die Zeit abgelaufen ist, auch wenn der Taster noch weiter gedrückt bleibt.

-----

## Anwendungsbeispiel

**Licht dimmen**: Ein kurzer Klick schaltet Ein/Aus (siehe Übung 004a). Ein langer Druck (erkannt durch `LONG_PRESS_START`) startet den Dimm-Vorgang.