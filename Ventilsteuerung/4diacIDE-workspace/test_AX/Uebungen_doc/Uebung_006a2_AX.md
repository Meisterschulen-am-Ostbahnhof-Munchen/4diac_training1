# Uebung_006a2_AX: Zentral-Reset für mehrere Speicher

```{index} single: Uebung_006a2_AX: Zentral-Reset für mehrere Speicher
```

[Uebung_006a2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a2_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a2_AX`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* ["Store Version" – Dein Schlüssel zur Verwaltung von Objektdatenpools im nichtflüchtigen VT-Speicher (ISO 11783-6)](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/Store-Version--Dein-Schlssel-zur-Verwaltung-von-Objektdatenpools-im-nichtflchtigen-VT-Speicher-ISO-11783-6-e36vfh0)
* [Ende der EEG-Förderung: Ihr Weg zur Energie-Autarkie – PV, Speicher & smarte Nutzung](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Ende-der-EEG-Frderung-Ihr-Weg-zur-Energie-Autarkie--PV--Speicher--smarte-Nutzung-e371mk0)
* [ESP32-S3-DevKitC-1 Doku-Analyse: Das Speicher-Monster (32MB Flash/16MB PSRAM) und die Macht der Dual-USB-Ports](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/ESP32-S3-DevKitC-1-Doku-Analyse-Das-Speicher-Monster-32MB-Flash16MB-PSRAM-und-die-Macht-der-Dual-USB-Ports-e39hamt)
* [Smart Power: Wie dezentrale Steuerung die Energiekosten in Industrieanlagen senkt und das Netz stabilisiert](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Smart-Power-Wie-dezentrale-Steuerung-die-Energiekosten-in-Industrieanlagen-senkt-und-das-Netz-stabilisiert-e372aq3)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a2_AX.png)


## Ziel der Übung

Demonstration einer Zentral-Aus-Funktion.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a2_AX.SUB` steuert zwei unabhängige Lampen, die gemeinsam gelöscht werden können[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1`**: Toggelt Lampe 1.
  * **`I2`**: Toggelt Lampe 2.
  * **`I3`**: Reset für beide.
  * **2x `AX_T_FF_SR`**: Je einer pro Lampe.

-----

## Funktionsweise

*   `I1` ist mit `CLK` von FF1 verbunden.
*   `I2` ist mit `CLK` von FF2 verbunden.
*   `I3` ist mit `R` von **beiden** Flip-Flops verbunden (Fan-Out).

Ein Druck auf `I3` schaltet sofort beide Lampen aus, egal in welchem Zustand sie waren.

-----

## Anwendungsbeispiel

**Bürobeleuchtung**: Jeder Schreibtisch hat sein eigenes Licht (`I1`, `I2`), aber am Ausgang gibt es einen Schalter "Raum verlassen", der alles ausschaltet (`I3`).