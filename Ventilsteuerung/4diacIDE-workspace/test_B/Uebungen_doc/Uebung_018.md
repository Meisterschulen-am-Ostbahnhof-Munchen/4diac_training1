# Uebung_018: Melodien und Sequenzen (Audio-Delay)

```{index} single: Uebung_018: Melodien und Sequenzen (Audio-Delay)
```

[Uebung_018](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_018.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_018`. Hier wird die Audio-Ausgabe erweitert, um zeitlich versetzte Tonfolgen zu erzeugen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [E_DELAY in IEC 61499: Präzise, Abbrechbare Zeitverzögerung in Steuerungssystemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_DELAY-in-IEC-61499-Przise--Abbrechbare-Zeitverzgerung-in-Steuerungssystemen-e3674le)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_018.png)


## Ziel der Übung

Erlernen der Ereignisverzögerung (`E_DELAY`) zur Erstellung von Sequenzen. Es wird gezeigt, wie man zwei Töne mit unterschiedlichen Frequenzen nacheinander abspielt.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_018.SUB` werden zwei Audio-Bausteine über ein Zeitglied verkettet[cite: 1].

### Funktionsbausteine (FBs)

  * **`Q_CtrlAudioSignal_0`**: Erster Ton (440 Hz).
  * **`E_DELAY`**: Ein Verzögerungs-Baustein. [cite_start]Er wartet nach einem Ereignis am Eingang `START` die Zeit `DT` ab (hier 250 ms), bevor er das Ereignis am Ausgang `EO` weitergibt[cite: 1].
  * **`Q_CtrlAudioSignal_1`**: Zweiter Ton (880 Hz - eine Oktave höher).

-----

## Funktionsweise

1.  Softkey-Klick startet Ton 0.
2.  Gleichzeitig mit dem Start des ersten Tons (oder nach dessen Bestätigung `CNF`) wird der Timer `E_DELAY` gestartet.
3.  Während der erste Ton klingt (150ms) und die kurze Pause danach, läuft die Zeit ab.
4.  Nach 250ms feuert der Timer und startet den zweiten (höheren) Ton.

Das Ergebnis ist ein zweistufiges "Didi"-Signal.

-----

## Anwendungsbeispiel

**Differenzierte Warnsignale**:
Ein kurzes "Piep" ist eine normale Info. Ein "Piep-Piep" (z.B. tiefer Ton gefolgt von hohem Ton) signalisiert das Ende eines Vorgangs. Ein umgekehrtes Signal (hoch nach tief) könnte eine Fehlermeldung akustisch untermalen.