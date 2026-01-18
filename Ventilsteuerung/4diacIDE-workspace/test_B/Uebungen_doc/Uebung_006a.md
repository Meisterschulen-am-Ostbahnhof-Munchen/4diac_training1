# Uebung_006a: Universal-Flip-Flop (Toggle/Set/Reset)

```{index} single: Uebung_006a: Universal-Flip-Flop (Toggle/Set/Reset)
```

[Uebung_006a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a`. Hier wird ein hochflexibler Speicherbaustein verwendet, der drei verschiedene Bedienweisen kombiniert.


## 📺 Video

* [SR&T-Flip-Flop Übung 006a](https://www.youtube.com/watch?v=lfumU4WoIGs)
* [Toggle-Flip-Flop Baustein E_T_FF aus der IEC 61499 (Übung 004a)](https://www.youtube.com/watch?v=XZqsqNy_g_g)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)

## Podcast
* [Universal Automation: So entkoppeln Sie Software und Hardware für die Zukunft der Industrie](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Universal-Automation-So-entkoppeln-Sie-Software-und-Hardware-fr-die-Zukunft-der-Industrie-e36849a)
* [Unlocking Universal Automation: The IEC 61499 Revolution from Factory Floors to the Seas](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Unlocking-Universal-Automation-The-IEC-61499-Revolution-from-Factory-Floors-to-the-Seas-e376p9m)
* [Unpacking E_T_FF_SR: The Secret Toggle Switch of Industrial Control Systems](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Unpacking-E_T_FF_SR-The-Secret-Toggle-Switch-of-Industrial-Control-Systems-e367ntv)
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
* [ISOBUS revolutioniert Landwirtschaft Universal Terminal Task Controller](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/ISOBUS-revolutioniert-Landwirtschaft-Universal-Terminal-Task-Controller-e3b8omh)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a.png)


## Ziel der Übung

Einführung des `E_T_FF_SR` Bausteins. Dieser vereint die Funktionen eines Toggle-Flip-Flops mit denen eines SR-Speichers.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a.SUB` verknüpft drei separate Taster mit einem zentralen Speicherglied[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Set)**: Schaltet den Ausgang ein.
  * **`I2` (Reset)**: Schaltet den Ausgang aus.
  * **`I3` (Toggle)**: Wechselt den aktuellen Zustand.
  * **`E_T_FF_SR`**: Der Kombi-Baustein für alle drei Ereignistypen.

-----

## Funktionsweise

Der Baustein reagiert auf jedes der drei Eingangs-Events individuell:
*   Ein Event an `S` setzt den Zustand fest auf `TRUE`.
*   Ein Event an `R` setzt den Zustand fest auf `FALSE`.
*   Ein Event an `CLK` invertiert den aktuellen Zustand (Toggle).

Alle Ereignisse führen zu einer Aktualisierung des Ausgangs `Q` und feuern das Bestätigungs-Event `EO` ab, um die Hardware anzusteuern.

-----

## Anwendungsbeispiel

**Gebäude-Lichtsteuerung**:
*   **Vor Ort**: Ein Taster im Zimmer toggelt das Licht (`I3`).
*   **Zentrale**: Am Hauseingang gibt es einen Taster "Gute Nacht", der alle Lichter per Reset (`I2`) ausschaltet.
*   **Alarmanlage**: Im Falle eines Einbruchs setzt die Zentrale alle Lichter per Set (`I1`) dauerhaft ein.