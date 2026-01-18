# Uebung_004c1: Doppelklick-Auswertung

```{index} single: Uebung_004c1: Doppelklick-Auswertung
```

[Uebung_004c1](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c1.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c1`. Ab hier widmen wir uns den erweiterten Fähigkeiten des `logiBUS_IE` Bausteins, der komplexe Taster-Muster erkennen kann.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c1.png)


## Ziel der Übung

Nutzung des Ereignisses `BUTTON_DOUBLE_CLICK` zur Steuerung einer Speicherfunktion.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_004c1.SUB` schaltet eine Lampe nur bei einem Doppelklick um[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1`**: Typ `logiBUS_IE`. Dieser ist im Parameter `InputEvent` auf `BUTTON_DOUBLE_CLICK` konfiguriert.
  * **`E_T_FF`**: Das Toggle-Flip-Flop.

-----

## Funktionsweise

Der Eingangsbaustein überwacht das zeitliche Muster am Hardware-Pin `I1`.
1.  Ein einfacher Tastendruck wird ignoriert (kein Event an `IND`).
2.  Werden zwei Klicks innerhalb einer definierten Zeit (meist < 500ms) erkannt, feuert der Baustein **einmal** das Ereignis `IND`.
3.  Dieses Ereignis triggert das Flip-Flop, welches den Zustand der Lampe wechselt.

-----

## Anwendungsbeispiel

**Vermeidung von Fehlbedienungen**: Kritische Befehle (wie z.B. "Alle Motoren Stopp" oder "Daten löschen") können auf einen Doppelklick gelegt werden, damit ein versehentliches Berühren des Tasters keine Folgen hat.