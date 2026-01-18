# Uebung_020f_AX: Impulsglied (TP)

```{index} single: Uebung_020f_AX: Impulsglied (TP)
```

[Uebung_020f_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f_AX`. Hier wird ein Impuls-Timer (TP - Timer Pulse) verwendet, um eine definierte Einschaltdauer zu erzwingen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020f_AX.png)


## Ziel der Übung

Das Ziel dieser Übung ist die Anwendung des `AX_TP` Bausteins. Ein Impulsglied ist ideal, wenn eine Aktion für eine exakte Zeitspanne ausgeführt werden soll, unabhängig davon, wie lange der auslösende Taster gedrückt bleibt.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020f_AX.SUB` nutzt einen Adapter-Timer vom Typ `AX_TP`[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Typ `logiBUS_IXA`. Der Auslöser.
  * **`AX_TP`**: [cite_start]Erzeugt bei einer steigenden Flanke am Eingang einen Impuls der Länge `PT` (hier 5 Sekunden) am Ausgang `Q`[cite: 1].
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`. Der Aktor.

-----

## Funktionsweise

1.  **Triggerung**: Sobald der Eingang `I1` den Zustand `TRUE` einnimmt, startet der Timer.
2.  **Aktivierung**: Der Ausgang `Q` wird sofort `TRUE` und die Lampe `Q1` leuchtet.
3.  **Zeitablauf**: Auch wenn der Nutzer den Taster sofort wieder loslässt (oder ihn 10 Sekunden lang gedrückt hält), bleibt die Lampe für exakt **5 Sekunden** an.
4.  **Abschluss**: Nach Ablauf der 5 Sekunden geht die Lampe automatisch aus. Ein neuer Impuls kann erst nach dem nächsten Flankenwechsel am Eingang ausgelöst werden.

-----

## Anwendungsbeispiel

**Schmierung oder Reinigung**: Eine Zentralschmierung an einer Maschine oder eine Reinigungsdüse soll nach einem Startsignal für genau 5 Sekunden aktiv sein, um die korrekte Menge an Medium abzugeben.