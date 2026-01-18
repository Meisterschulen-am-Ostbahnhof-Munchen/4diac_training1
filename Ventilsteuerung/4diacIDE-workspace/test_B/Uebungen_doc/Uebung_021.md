# Uebung_021: Sequenz-Grundlagen (Zylinder 1)

```{index} single: Uebung_021: Sequenz-Grundlagen (Zylinder 1)
```

[Uebung_021](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_021.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_021`. Dies ist der Einstieg in die Ablaufsteuerung (Sequenzierung), simuliert am Beispiel eines Pneumatik-Zylinders.

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-02-21 13-04-43 aktueller Stand logiBUS® Eclipse 4diac™ IDE](https://www.youtube.com/watch?v=OMNP9p12mAw)
* [2025-02-21 15-23-28 logiBUS® mit Eclipse 4diac™ neues IO Konzept für alle Controller](https://www.youtube.com/watch?v=YUCodIng1UA)
* [2025-03-15 16-27-21 Arithmetischer Überlauf führt zu Division durch 0.](https://www.youtube.com/watch?v=7CyOJPYJVz0)
* [2025-07-20 21-12-23  Fusion 360 Schematic SPICE Simulation deutsch](https://www.youtube.com/watch?v=jHT9nZIXxGU)

## 🎧 Podcast

* [Infineon MOTIX BTM9020/9021EP: Datenblatt-Analyse für Automotive – Robuster Motortreiber mit intelligenter Diagnose (HW vs. SPI)](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Infineon-MOTIX-BTM90209021EP-Datenblatt-Analyse-fr-Automotive--Robuster-Motortreiber-mit-intelligenter-Diagnose-HW-vs--SPI-e39av51)
* [JBC Lötspitzen C470 vs. C245 vs. C210 vs. C115: Welche Spitze ist der Allrounder und wann brauchst du den Nano-Spezialisten?](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/JBC-Ltspitzen-C470-vs--C245-vs--C210-vs--C115-Welche-Spitze-ist-der-Allrounder-und-wann-brauchst-du-den-Nano-Spezialisten-e39ak58)

----

![](Uebung_021.png)

## Ziel der Übung

Realisierung einer einfachen Folgesteuerung: Ein Prozess wird gestartet und stoppt automatisch, sobald eine Endlage erreicht ist.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_021.SUB` nutzt zwei Softkeys, um die Bewegung eines Aktors (`Q1`) zu steuern[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_UP_F1`**: Fungiert als **START-Taster**. [cite_start]Er ist auf `SK_RELEASED` konfiguriert[cite: 1].
  * **`SoftKey_F2_DOWN`**: Simuliert den **Endlagenschalter**. [cite_start]Er reagiert sofort beim Drücken (`SK_PRESSED`)[cite: 1].
  * **`E_SR`**: Der Speicher für den Bewegungszustand.
  * **`DigitalOutput_Q1`**: Der Ausgang für das Zylinderventil.

-----

## Funktionsweise

1.  **Start**: Der Nutzer klickt auf **F1**. Das Ereignis setzt den Speicher `E_SR.S` ➡️ Der Ausgang `Q1` wird aktiv, der Zylinder fährt aus.
2.  **Bewegung**: Der Zylinder bewegt sich physikalisch (oder in der Simulation) zur Endposition.
3.  **Stopp**: Sobald der Zylinder die Endlage erreicht, wird (simuliert durch **F2**) der Reset-Eingang `E_SR.R` getriggert ➡️ Der Ausgang `Q1` wird deaktiviert, die Bewegung stoppt.

-----

## Anwendungsbeispiel

**Einfacher Ausstoßer**:
In einer Fertigungslinie soll ein Paket per Knopfdruck vom Band geschoben werden. Der Bediener gibt den Startimpuls, der Zylinder fährt aus, schiebt das Paket weg und wird durch einen mechanischen Endschalter am Ende des Weges automatisch wieder abgeschaltet.