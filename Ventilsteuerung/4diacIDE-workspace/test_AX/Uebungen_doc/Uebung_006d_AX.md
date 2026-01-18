# Uebung_006d_AX: SR-Flip-Flop mit Doppelklick-Set

```{index} single: Uebung_006d_AX: SR-Flip-Flop mit Doppelklick-Set
```

[Uebung_006d_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006d_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006d_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006d_AX.png)


## Ziel der Übung

Kombination von Input-Events und Speichergliedern.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006d_AX.SUB` definiert eine asymmetrische Bedienung[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Set)**: Konfiguriert auf `BUTTON_DOUBLE_CLICK`.
  * **`I2` (Reset)**: Konfiguriert auf `BUTTON_SINGLE_CLICK`.
  * **`AX_SR`**: Speicher.

-----

## Funktionsweise

*   Zum **Einschalten** muss man den Taster `I1` **doppelt** klicken.
*   Zum **Ausschalten** reicht ein **einfacher** Klick auf `I2`.

-----

## Anwendungsbeispiel

**Schutz vor versehentlichem Einschalten**: Ein Gerät (z.B. eine Pumpe), das gefährlich sein kann oder viel Energie verbraucht, soll nicht durch ein versehentliches Berühren des Schalters starten. Der Doppelklick fordert eine bewusste Handlung ("Ja, ich will wirklich"). Das Ausschalten muss hingegen im Notfall schnell und einfach gehen (Einzelklick).