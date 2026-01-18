# Uebung_003b2_sub: Funk-zu-CAN Treiber (SubApp)

```{index} single: Uebung_003b2_sub: Funk-zu-CAN Treiber (SubApp)
```

[Uebung_003b2_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_003b2_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_003b2_sub`. Dieser Baustein dient als universeller Koppler zwischen einer Funkfernbedienung und einem CAN-Bus Ausgangsmodul (DataPanel).


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Infineon MOTIX BTM9020/9021EP: Datenblatt-Analyse für Automotive – Robuster Motortreiber mit intelligenter Diagnose (HW vs. SPI)](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Infineon-MOTIX-BTM90209021EP-Datenblatt-Analyse-fr-Automotive--Robuster-Motortreiber-mit-intelligenter-Diagnose-HW-vs--SPI-e39av51)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



## Ziel der Übung

Abstraktion von Funk-Signalen. Der Baustein ermöglicht es, Funktasten so einfach zu handhaben wie direkt verdrahtete Eingänge und diese auf ein dezentrales Ausgangsmodul zu mappen.

-----

## Beschreibung und Komponenten

[cite_start]Der Typ `Uebung_003b2_sub` bündelt den Funk-Empfang und die CAN-Ausgabe[cite: 1].

### Interne Funktionsbausteine (FBs)

  * **`IX`**: Typ `Funk_IX`. Empfängt die Signale der über `Input` gewählten Funktaste.
  * **`QX`**: Typ `DataPanel_MI_QX`. Sendet CAN-Nachrichten an das gewählte DataPanel (`u8SAMember`) und schaltet dort den physischen Port (`Output`).

-----

## Schnittstellen

[cite_start]Der Baustein bietet drei Konfigurationsmöglichkeiten[cite: 1]:
*   **`Input`**: Name der Funktaste (z.B. `Key_01`).
*   **`u8SAMember`**: CAN-Bus Adresse des Zielmoduls.
*   **`Output`**: Nummer des Ausgangs am Modul (z.B. `DigitalOutput_1A`).

Durch die Verwendung dieses Typs kann eine komplexe Funkfernsteuerung durch einfaches "Eintragen" der IDs in der Hauptanwendung konfiguriert werden.