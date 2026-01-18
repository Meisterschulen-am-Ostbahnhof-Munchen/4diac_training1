# Uebung_020d_AX: Ausschaltverzögerung (aufgelöst)

```{index} single: Uebung_020d_AX: Ausschaltverzögerung (aufgelöst)
```

[Uebung_020d_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020d_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020d_AX`. Hier wird eine Ausschaltverzögerung (TOF) aus diskreten Ereignis- und Speicherbausteinen aufgebaut.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020d_AX.png)


## Ziel der Übung

Das Ziel dieser Übung ist die Analyse der Ausschaltverzögerung auf Logikebene. Im Gegensatz zur Einschaltverzögerung (`Uebung_020b_AX`) startet hier die Zeitmessung erst beim *Loslassen* des Tasters.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020d_AX.SUB` nutzt eine Ereignis-Weiche, um den Speicher beim Drücken sofort zu setzen und beim Loslassen zeitverzögert zurückzusetzen[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Typ `logiBUS_IXA`. Signaleingang.
  * **`AX_SWITCH`**: [cite_start]Trennt steigende (`EO1`) und fallende (`EO0`) Flanken[cite: 1].
  * **`AX_RS`**: Der Ergebnisspeicher.
  * **`E_DELAY`**: [cite_start]Verzögert das Rücksetz-Ereignis um 2 Sekunden (`DT = T#2S`)[cite: 1].
  * **`DigitalOutput_Q1`**: Typ `logiBUS_QXA`. Signalausgang.

-----

## Funktionsweise

Die Logik arbeitet wie folgt:

1.  **Einschalten (Sofort)**:
    Wird `I1` gedrückt, sendet die Weiche ein Event an `EO1`. Dieses Event setzt sofort den Speicher `AX_RS.S` -> `Q1` geht an. Gleichzeitig wird eine eventuell noch laufende Verzögerung gestoppt (`E_DELAY.STOP`).
2.  **Loslassen (Start der Verzögerung)**:
    Wird `I1` losgelassen, sendet die Weiche ein Event an `EO0`. Dieses Event startet die Zeitmessung `E_DELAY.START`. Der Speicher bleibt vorerst auf TRUE.
3.  **Ausschalten (Nach Ablauf der Zeit)**:
    Nach 2 Sekunden feuert `E_DELAY.EO`. Dieses Event setzt den Speicher zurück (`AX_RS.R`) -> `Q1` geht aus.

Im Ergebnis leuchtet die Lampe sofort beim Drücken und bleibt nach dem Loslassen noch genau 2 Sekunden lang an.

-----

## Anwendungsbeispiel

**Nachlaufsteuerung**: Ein Treppenhauslicht oder ein Lüfter soll sofort anspringen, wenn der Schalter betätigt wird, aber nach dem Verlassen des Raumes noch für eine gewisse Zeit weiterlaufen.