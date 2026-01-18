# Uebung_006a_AX: Kombiniertes T/SR Flip-Flop

```{index} single: Uebung_006a_AX: Kombiniertes T/SR Flip-Flop
```

[Uebung_006a_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a_AX`. Diese Übung zeigt einen "Alles-Könner"-Baustein.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a_AX.png)


## Ziel der Übung

Kennenlernen des `AX_T_FF_SR`.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a_AX.SUB` nutzt drei Taster[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Set)**
  * **`I2` (Reset)**
  * **`I3` (Toggle)**
  * **`AX_T_FF_SR`**: Vereint Toggle, Set und Reset in einem Baustein.

-----

## Funktionsweise

*   `I1` schaltet an.
*   `I2` schaltet aus.
*   `I3` schaltet um.

Dies bietet maximale Flexibilität für die Bedienung.

-----

## Anwendungsbeispiel

**Smart Home Lichtsteuerung**:
*   Taster an der Wand: Toggle (`I3`).
*   Zentral "Alles Aus" beim Verlassen des Hauses: Reset (`I2`).
*   "Panik-Licht" (Alarmanlage): Set (`I1`).