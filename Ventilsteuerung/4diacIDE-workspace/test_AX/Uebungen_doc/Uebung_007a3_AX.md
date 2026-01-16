# Uebung_007a3_AX: Korrekter Blinker (Definierter Stopp)

[Uebung_007a3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_007a3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_007a3_AX`. Diese Übung zeigt die "saubere" Lösung für einen schaltbaren Blinker.


## Podcast
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
  * **`AX_MERGE_2`**: Führt das Taktsignal (`AX_CYCLE.Q`) und das Rückkopplungssignal zusammen.
  * **`E_SWITCH`**: Das eigentliche "Herzstück". Es nutzt das Taktsignal (via Merge), um das SR-Flip-Flop umzuschalten.

Aber das Wichtigste: Der `STOP` Eingang ist **zusätzlich** direkt mit `E_SR.R` verbunden.

-----

## Funktionsweise

1.  **Blinken**: Wenn aktiv, sorgt die Schleife über `E_SWITCH` und `E_SR` für das Toggeln (ähnlich zu Übung 004b).
2.  **Stoppen**: Wenn `STOP` gedrückt wird:
    *   Der `AX_CYCLE` stoppt (keine neuen Takte).
    *   Der `E_SR` wird **resettet**. Damit wird der Ausgang `Q` und somit die Lampe `Q1` **zwingend** auf FALSE gesetzt.

-----

## Anwendungsbeispiel

**Professioneller Indikator**: Eine Störungsleuchte in der Industrie muss blinken, wenn ein Fehler vorliegt, und **aus** sein, wenn der Fehler quittiert wurde. Sie darf niemals dauerhaft leuchten (das würde oft "Betriebsbereit" oder etwas anderes bedeuten).
