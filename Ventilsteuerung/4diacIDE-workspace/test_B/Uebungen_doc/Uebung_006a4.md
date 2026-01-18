# Uebung_006a4: Motor-Wende-Schaltung (Bibliothek)

```{index} single: Uebung_006a4: Motor-Wende-Schaltung (Bibliothek)
```

[Uebung_006a4](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a4.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a4`. Hier wird die Motorsteuerung aus der vorherigen Übung durch die Verwendung eines fertigen Bibliotheksbausteins optimiert.


## 📺 Video

* [2024 09 05 17 59 50 Bayerische Staatsbibliothek Buch Zugriff](https://www.youtube.com/watch?v=0qTGNMfAspU)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Eclipse 4diac: Innovationsmotor Forschung vs. Nutzerbedürfnisse – Was treibt die Entwicklung wirklich voran?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Innovationsmotor-Forschung-vs--Nutzerbedrfnisse--Was-treibt-die-Entwicklung-wirklich-voran-e38cke4)
* [Der Bipolare Transistor: Das Herzstück eingebetteter Systeme – Verstärkung und Schaltung verstehen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Bipolare-Transistor-Das-Herzstck-eingebetteter-Systeme--Verstrkung-und-Schaltung-verstehen-e368kip)
* [Der Niedergang des Traktoren-Kults: Vom genialen Schwenkkammer-Motor zum teuren Ende der Motorenfabrik Anton Schlüter](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Niedergang-des-Traktoren-Kults-Vom-genialen-Schwenkkammer-Motor-zum-teuren-Ende-der-Motorenfabrik-Anton-Schlter-e3aea7o)
* [Diesels radikale Vision: Warum der Erfinder alle Motoren seiner Zeit für „prinzipiell falsch“ hielt – Der Weg zum Dieselmotor](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Diesels-radikale-Vision-Warum-der-Erfinder-alle-Motoren-seiner-Zeit-fr-prinzipiell-falsch-hielt--Der-Weg-zum-Dieselmotor-e399mvg)
* [Fritz Huber und der Lanz Bulldog: Wie der Glühkopfmotor die Landwirtschaft revolutionierte](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Fritz-Huber-und-der-Lanz-Bulldog-Wie-der-Glhkopfmotor-die-Landwirtschaft-revolutionierte-e39km7k)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a4.png)


## Ziel der Übung

Nutzung von spezialisierten Dienstbausteinen zur Reduktion der Diagramm-Komplexität.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_006a4.SUB` wird das Netzwerk aus Gattern und Sub-Apps durch den Baustein `LinksRechts` ersetzt[cite: 1].

### Funktionsbausteine (FBs)

  * **`LinksRechts`**: Typ `logiBUS::utils::sequence::verteiler::LinksRechts`. [cite_start]Dieser Baustein übernimmt die komplette Verwaltung der zwei Ausgänge inklusive der internen Richtungs-Logik[cite: 1].
  * **`E_T_FF_SR`**: Liefert weiterhin das Startsignal an den Eingang `EI_ON`.

-----

## Vorteil

Durch die Verwendung von Bibliotheksbausteinen wird das Programm lesbarer und wartungsfreundlicher. Die interne Verriegelung ist im Baustein fest programmiert und kann nicht versehentlich durch fehlerhafte Verbindungen im Hauptdiagramm umgangen werden.