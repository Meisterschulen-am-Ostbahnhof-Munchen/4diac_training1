# Uebung_007a3_AX: Korrekter Blinker (Definierter Stopp)

```{index} single: Uebung_007a3_AX: Korrekter Blinker (Definierter Stopp)
```

[Uebung_007a3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_007a3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_007a3_AX`. Diese Übung zeigt die "saubere" Lösung für einen schaltbaren Blinker.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [The Unstoppable Counter: Why IEC 61499's ECTU Guarantees Safe, Event-Driven Control (and Never Overflows)](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/The-Unstoppable-Counter-Why-IEC-61499s-ECTU-Guarantees-Safe--Event-Driven-Control-and-Never-Overflows-e3a9qsh)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_007a3_AX.png)


## Ziel der Übung

Sicherstellen, dass der Blinker immer im Zustand "AUS" stoppt.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_007a3_AX.SUB` verwendet eine komplexere Logik[cite: 1]:

  * **`AX_CYCLE`**: Der Taktgeber (Startet/Stoppt).
  * **`E_SR`**: Ein Speicher ("Blinker ist aktiv").
  * **`AX_SPLIT_2`**: Verteilt das Signal vom Speicher (zur Lampe und zur Rückkopplung).
  * **`AX_AE_MERGE`**: Führt das Taktsignal (`AE_CYCLE.EO` - nur Event) und das Rückkopplungssignal (`E_SR.Q` - Event und BOOL) zusammen. Das Daten-Bit vom `E_SR.Q` bleibt dabei erhalten.
  * **`E_SWITCH`**: Das eigentliche "Herzstück". Es nutzt das gemergte Signal, um das `AX_SR`-Flip-Flop umzuschalten.

Aber das Wichtigste: Der `STOP` Eingang ist **zusätzlich** direkt mit `E_SR.R` verbunden.

-----

## Funktionsweise

1.  **Start/Blinken**: `START` drückt den Taster und startet den `AE_CYCLE`. Wenn `E_SR.Q` aktiv ist, sorgt die Schleife über `E_SWITCH` (durch `AX_AE_MERGE` getriggert) für das Toggeln.
2.  **Stoppen**: Wenn `STOP` gedrückt wird:
    *   Der `AE_CYCLE` stoppt (keine neuen Takte).
    *   Der `E_SR` wird **resettet**. Damit wird der Ausgang `Q` und somit die Lampe `Q1` **zwingend** auf FALSE gesetzt.

-----

## Anwendungsbeispiel

**Professioneller Indikator**: Eine Störungsleuchte in der Industrie muss blinken, wenn ein Fehler vorliegt, und **aus** sein, wenn der Fehler quittiert wurde. Sie darf niemals dauerhaft leuchten (das würde oft "Betriebsbereit" oder etwas anderes bedeuten).