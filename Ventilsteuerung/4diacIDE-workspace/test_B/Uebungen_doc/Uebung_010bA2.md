# Uebung_010bA2: AUX-Zustands-Events (Enabled)

```{index} single: Uebung_010bA2: AUX-Zustands-Events (Enabled)
```

[Uebung_010bA2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010bA2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010bA2`. Hier geht es um die Feinheiten der AUX-Spezifikation bezüglich rastender und tastender Eingänge.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Taster & Events: GPIO-Grundlagen für Land- und Baumaschinen Mechatroniker](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Taster--Events-GPIO-Grundlagen-fr-Land--und-Baumaschinen-Mechatroniker-e36aaen)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010bA2.png)


## Funktionsweise

[cite_start]Verwendet `AuxFunction2_X1` mit dem Event `AuxEnabled`[cite: 1]. Das Verhalten hängt vom Typ des zugewiesenen Bedienelements (Joystick-Taste) ab:
*   Bei einem **tastenden Bediener** (NonLatched) wird das Event nur einmal beim Drücken gesendet.
*   Bei einem **rastenden Bediener** (Latched) wird das Event zyklisch wiederholt, solange der Schalter aktiv ist.
Dies verdeutlicht, wie die Software auf die Hardware-Eigenschaften des verwendeten Joysticks reagiert.