# Uebung_021: Sequenz-Grundlagen (Zylinder 1)

```{index} single: Uebung_021: Sequenz-Grundlagen (Zylinder 1)
```

[Uebung_021](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_021.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_021`. Dies ist der Einstieg in die Ablaufsteuerung (Sequenzierung), simuliert am Beispiel eines Pneumatik-Zylinders.


## 📺 Video

* [Infineon MOTIX BTM9020/9021EP: Datenblatt-Analyse für Automotive – Robuster Motortreiber mit inte...](https://www.youtube.com/watch?v=EuWZ5Uhp_P0)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Infineon MOTIX BTM9020/9021EP: Datenblatt-Analyse für Automotive – Robuster Motortreiber mit intelligenter Diagnose (HW vs. SPI)](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Infineon-MOTIX-BTM90209021EP-Datenblatt-Analyse-fr-Automotive--Robuster-Motortreiber-mit-intelligenter-Diagnose-HW-vs--SPI-e39av51)
* [Elektrotechnik Grundlagen: Spannung, Strom, Widerstand & Leistung – Das Formelrad entschlüsselt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Elektrotechnik-Grundlagen-Spannung--Strom--Widerstand--Leistung--Das-Formelrad-entschlsselt-e38dlc0)
* [Kraftpakete im Einsatz: Das Geheimnis der Hydraulikzylinder – Von Baggern bis Hightech-Maschinen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Kraftpakete-im-Einsatz-Das-Geheimnis-der-Hydraulikzylinder--Von-Baggern-bis-Hightech-Maschinen-e373ne8)
* [Ohmsches Gesetz: Grundlagen und Anwendungen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Ohmsches-Gesetz-Grundlagen-und-Anwendungen-e368gui)
* [Parallelschaltung von Widerständen: Grundlagen und Anwendung](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Parallelschaltung-von-Widerstnden-Grundlagen-und-Anwendung-e368iop)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

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