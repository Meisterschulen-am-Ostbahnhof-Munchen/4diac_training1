# Uebung_094a: Integrierte Freigabe (QI)

```{index} single: Uebung_094a: Integrierte Freigabe (QI)
```

[Uebung_094a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_094a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_094a`. Hier wird eine alternative Methode zur Freigabe-Steuerung gezeigt, die direkt in den Bausteinen eingebaut ist.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [integrierten Vollbrücken-ICs MOTIX™ BTM9020EP](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/integrierten-Vollbrcken-ICs-MOTIX-BTM9020EP-e368kse)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_094a.png)


## Übersicht

[cite_start]Anstatt einen externen `E_PERMIT` Baustein zu nutzen, wird hier der Standard-Port `QI` (Qualified Input) des Eingangsbausteins `DigitalInput_I1` verwendet[cite: 1].
Über ein Toggle-Flip-Flop wird der `QI` Eingang ein- und ausgeschaltet. Steht `QI` auf `FALSE`, ist der gesamte Baustein deaktiviert und sendet keine Ereignisse mehr an den Ausgang `Q1`, selbst wenn sich der physikalische Zustand am Hardware-Pin ändert. Dies ist die sauberste Methode, um ganze Funktionsblöcke im Programm schlafen zu legen.