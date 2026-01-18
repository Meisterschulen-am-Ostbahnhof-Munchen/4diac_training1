# Uebung_006a3: Motor-Wende-Schaltung (Diskret)

```{index} single: Uebung_006a3: Motor-Wende-Schaltung (Diskret)
```

[Uebung_006a3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006a3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006a3`. Dies ist eine anspruchsvollere Anwendung zur Steuerung eines Motors mit zwei Drehrichtungen und automatischer Umschaltung.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Eclipse 4diac: Innovationsmotor Forschung vs. Nutzerbedürfnisse – Was treibt die Entwicklung wirklich voran?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Innovationsmotor-Forschung-vs--Nutzerbedrfnisse--Was-treibt-die-Entwicklung-wirklich-voran-e38cke4)
* [Der Bipolare Transistor: Das Herzstück eingebetteter Systeme – Verstärkung und Schaltung verstehen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Bipolare-Transistor-Das-Herzstck-eingebetteter-Systeme--Verstrkung-und-Schaltung-verstehen-e368kip)
* [Der Niedergang des Traktoren-Kults: Vom genialen Schwenkkammer-Motor zum teuren Ende der Motorenfabrik Anton Schlüter](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Niedergang-des-Traktoren-Kults-Vom-genialen-Schwenkkammer-Motor-zum-teuren-Ende-der-Motorenfabrik-Anton-Schlter-e3aea7o)
* [Diesels radikale Vision: Warum der Erfinder alle Motoren seiner Zeit für „prinzipiell falsch“ hielt – Der Weg zum Dieselmotor](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Diesels-radikale-Vision-Warum-der-Erfinder-alle-Motoren-seiner-Zeit-fr-prinzipiell-falsch-hielt--Der-Weg-zum-Dieselmotor-e399mvg)
* [Fritz Huber und der Lanz Bulldog: Wie der Glühkopfmotor die Landwirtschaft revolutionierte](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Fritz-Huber-und-der-Lanz-Bulldog-Wie-der-Glhkopfmotor-die-Landwirtschaft-revolutionierte-e39km7k)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006a3.png)


## Ziel der Übung

Aufbau einer Steuerung für Vorwärts- und Rückwärtslauf mit Software-Verriegelung. Es muss sichergestellt werden, dass niemals beide Richtungen gleichzeitig angesteuert werden können.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006a3.SUB` kombiniert einen Haupt-Ein/Aus-Speicher mit einer Logik zur Richtungsentscheidung[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_T_FF_SR`**: Bestimmt, ob der Motor läuft (Ein/Aus).
  * **`LinksRechts_T_FF` (SubApp)**: Ein interner Merker, der bei jedem Start die Richtung wechselt.
  * **2x `AND_2_BOOL`**: Verknüpfen das "Ein"-Signal mit der gewählten Richtung.
  * **`Q1` (Linkslauf) & `Q2` (Rechtslauf)**: Die Hardware-Ausgänge.

-----

## Funktionsweise

1.  Der Nutzer startet das System über `I1`, `I2` oder `I3`.
2.  Das Flip-Flop liefert ein "Global Ein" Signal.
3.  Die SubApp `LinksRechts_T_FF` entscheidet, welcher Zweig aktiv ist.
4.  Durch die UND-Gatter kann das "Ein"-Signal nur zu einem der beiden Ausgänge durchdringen.

Diese Schaltung demonstriert, wie man komplexe Entscheidungen durch die Kombination von Basisfunktionen (Speicher, Logikgatter, Sub-Applikationen) löst.

-----

## Anwendungsbeispiel

**Reversierendes Rührwerk**: Ein Motor in einem Mischtank soll bei jedem Einschalten die Drehrichtung ändern, um eine bessere Durchmischung des Mediums zu erreichen. Die Software stellt dabei sicher, dass der Motor immer nur in eine Richtung Strom erhält.