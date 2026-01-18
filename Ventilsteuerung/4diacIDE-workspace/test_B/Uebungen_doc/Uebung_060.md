# Uebung_060: Task Controller Section Control (TC-SC)

```{index} single: Uebung_060: Task Controller Section Control (TC-SC)
```

[Uebung_060](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_060.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_060`. Dies ist eine High-Level Übung für professionelle ISOBUS-Anwendungen im Bereich des Precision Farming.


## 📺 Video

* [2025-02-21 15-23-28 logiBUS® mit Eclipse 4diac™ neues IO Konzept für alle Controller](https://www.youtube.com/watch?v=YUCodIng1UA)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [ISOBUS revolutioniert Landwirtschaft Universal Terminal Task Controller](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/ISOBUS-revolutioniert-Landwirtschaft-Universal-Terminal-Task-Controller-e3b8omh)
* [Eclipse 4diac: Revolutionizing Industrial Control with Open-Source Cyber-Physical Systems](https://podcasters.spotify.com/pod/show/eclipse-4diac-en/episodes/Eclipse-4diac-Revolutionizing-Industrial-Control-with-Open-Source-Cyber-Physical-Systems-e368lqu)
* [Simplifying Industrial Control: Your Deep Dive into Eclipse 4diac and IEC 61499](https://podcasters.spotify.com/pod/show/eclipse-4diac-en/episodes/Simplifying-Industrial-Control-Your-Deep-Dive-into-Eclipse-4diac-and-IEC-61499-e3681v8)
* [The Future of Industrial Control: Decoding IEC 61499](https://podcasters.spotify.com/pod/show/eclipse-4diac-en/episodes/The-Future-of-Industrial-Control-Decoding-IEC-61499-e36cjlj)
* [Decoding Industrial Control: Function Blocks, Object-Oriented Principles, and the Power of IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Decoding-Industrial-Control-Function-Blocks--Object-Oriented-Principles--and-the-Power-of-IEC-61499-e3722d5)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_060.png)


## Ziel der Übung

Anbindung an einen ISOBUS Task Controller (TC). Es wird demonstriert, wie die automatische Teilbreitenschaltung (Section Control) und die Dokumentation von Arbeitszuständen und Ausbringraten realisiert werden.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_060.SUB` werden Sollwerte vom Task Controller empfangen und Istwerte zurückgemeldet[cite: 1].

### Funktionsbausteine (FBs)

  * **`TC_ID`**: Empfängt Befehle vom Task Controller des Traktors (z.B. "Schalte Teilbreite 5 ein").
  * **`TC_QD`**: Meldet Daten an den Task Controller zurück (z.B. "Teilbreite 5 ist jetzt tatsächlich aktiv").
  * **Quarter-Logik**: Die Zustände der Teilbreiten werden als Quartale (2-Bit) übertragen, um auch Fehlerzustände (z.B. Kabelbruch am Ventil) an den TC melden zu können.
  * **DDI (Data Dictionary Identifier)**: Spezifische Codes (z.B. `SETPOINT_CONDENSED_WORK_STATE`), die definieren, welche Information gerade übertragen wird.

-----

## Funktionsweise

1.  **Sollwert-Empfang**: Der Task Controller sendet ein DWORD, das die Zustände von 16 Teilbreiten enthält.
2.  **Verarbeitung**: Die Steuerung zerlegt dieses Wort in einzelne Quartale und dann in boolesche Signale für die Ventile (SubApp `Out`).
3.  **Istwert-Rückmeldung**: Die tatsächlichen Zustände der Ventile werden wieder zu einem DWORD zusammengefügt und als "Actual Condensed Work State" an den TC zurückgesendet.
4.  **Arbeitsstatus**: Sobald mindestens eine Teilbreite aktiv ist (`F_GT`), meldet die Steuerung dem TC den "Actual Work State" (Arbeit läuft), woraufhin der TC mit der Flächenaufzeichnung beginnt.

-----

## Anwendungsbeispiel

**Automatische Teilbreitenschaltung bei einer Spritze**:
Der Traktor erkennt per GPS, dass ein Teil des Gestänges über eine bereits behandelte Fläche fährt. Der Task Controller sendet den Befehl "Teilbreite 1-4 AUS". Das logiBUS-Programm empfängt diesen Befehl, schaltet die physischen Magnetventile ab und meldet dem Fahrer am Bildschirm den Erfolg durch den korrekten Ist-Status zurück.