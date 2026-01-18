# Uebung_160: Motor-Drehrichtungssteuerung

```{index} single: Uebung_160: Motor-Drehrichtungssteuerung
```

[Uebung_160](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_160.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_160`. Hier wird die einfache logische Verknüpfung zur Steuerung eines umschaltbaren Antriebs gezeigt.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Eclipse 4diac: Innovationsmotor Forschung vs. Nutzerbedürfnisse – Was treibt die Entwicklung wirklich voran?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Innovationsmotor-Forschung-vs--Nutzerbedrfnisse--Was-treibt-die-Entwicklung-wirklich-voran-e38cke4)
* [Der Niedergang des Traktoren-Kults: Vom genialen Schwenkkammer-Motor zum teuren Ende der Motorenfabrik Anton Schlüter](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Niedergang-des-Traktoren-Kults-Vom-genialen-Schwenkkammer-Motor-zum-teuren-Ende-der-Motorenfabrik-Anton-Schlter-e3aea7o)
* [Diesels radikale Vision: Warum der Erfinder alle Motoren seiner Zeit für „prinzipiell falsch“ hielt – Der Weg zum Dieselmotor](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Diesels-radikale-Vision-Warum-der-Erfinder-alle-Motoren-seiner-Zeit-fr-prinzipiell-falsch-hielt--Der-Weg-zum-Dieselmotor-e399mvg)
* [Fritz Huber und der Lanz Bulldog: Wie der Glühkopfmotor die Landwirtschaft revolutionierte](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Fritz-Huber-und-der-Lanz-Bulldog-Wie-der-Glhkopfmotor-die-Landwirtschaft-revolutionierte-e39km7k)
* [Glühkopfmotor, Gier und Kontrollverlust: Wie die Familie Lanz ihr Traktoren-Imperium verlor](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Glhkopfmotor--Gier-und-Kontrollverlust-Wie-die-Familie-Lanz-ihr-Traktoren-Imperium-verlor-e3ab3er)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_160.png)


## Ziel der Übung

Realisierung einer Steuerung für Linkslauf, Rechtslauf und ein Summensignal (Motor Aktiv).

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_160.SUB` werden zwei Taster auf drei Ausgänge gemappt[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1`**: Taster für Linkslauf.
  * **`I2`**: Taster für Rechtslauf.
  * **`OR_2_BOOL`**: Logische ODER-Verknüpfung.
  * **`Q5`**: Ausgang Linkslauf.
  * **`Q6`**: Ausgang Rechtslauf.
  * **`Q56`**: Ausgang "Motor läuft" (Summe).

-----

## Funktionsweise

*   Drückt der Nutzer **I1**, wird der Ausgang `Q5` aktiv.
*   Drückt der Nutzer **I2**, wird der Ausgang `Q6` aktiv.
*   Über das ODER-Gatter wird der Ausgang `Q56` immer dann aktiv, wenn **entweder I1 ODER I2** (oder beide) gedrückt werden.

Diese Schaltung demonstriert die Kombination von direkter Signalweiterleitung und logischer Vorverarbeitung für Anzeige-Zwecke.

-----

## Anwendungsbeispiel

**Zinkenrotor oder Förderband**:
Die Ausgänge `Q5` und `Q6` steuern die jeweiligen Schütze für die Drehrichtung. Der Ausgang `Q56` steuert eine zentrale Warnleuchte oder ein Entlastungsventil, das immer offen sein muss, wenn der Motor sich in irgendeine Richtung bewegt.