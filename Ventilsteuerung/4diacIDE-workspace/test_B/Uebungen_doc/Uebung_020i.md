# Uebung_020i: Teach-In Zeitsteuerung

```{index} single: Uebung_020i: Teach-In Zeitsteuerung
```

[Uebung_020i](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020i.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020i`. Dies ist eine sehr praxisnahe Übung, bei der eine Zeitdauer nicht durch Zahlenwerte, sondern durch "Vormachen" (Teach-In) gelernt wird.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020i.png)


## Ziel der Übung

Programmierung einer variablen Impulsdauer unter Verwendung des `E_STOPWATCH` Bausteins.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020i.SUB` nutzt zwei Taster: Einen zum Ausführen und einen zum Lernen der Zeit[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_STOPWATCH`**: Misst die Zeit zwischen einem Start- und einem Stopp-Ereignis.
  * **`E_PULSE`**: Erzeugt den zeitgesteuerten Impuls.
  * **`I2` (Lern-Taster)**: Ein normaler Pegel-Eingang (`IX`).
  * **`I1` (Start-Taster)**: Ein Klick-Event-Eingang (`IE`).

-----

## Funktionsweise

1.  **Lern-Modus**: Der Nutzer hält Taster `I2` gedrückt.
    *   Beim Drücken (steigende Flanke) startet die Stoppuhr.
    *   Beim Loslassen (fallende Flanke) stoppt die Stoppuhr.
    *   Die gemessene Zeitdauer (`TD`) wird sofort an den Parameter `PT` des Pulsgebers übergeben.
2.  **Arbeits-Modus**: Der Nutzer klickt kurz auf Taster `I1`.
    *   Der `E_PULSE` wird getriggert.
    *   Er schaltet den Ausgang für genau die Zeit an, die vorher mit Taster `I2` "vorgegeben" wurde.

-----

## Anwendungsbeispiel

**Zentralschmierung oder Bewässerung**:
Anstatt mühsam Sekundenwerte in ein Terminal einzutippen, drückt der Wartungstechniker einmalig so lange auf den Lern-Taster, wie er meint, dass der Vorgang dauern soll. Die Steuerung übernimmt diese Zeitspanne für alle zukünftigen automatischen Zyklen.