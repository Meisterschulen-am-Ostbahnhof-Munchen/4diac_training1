# Uebung_026_sub: Sequenz-Aktor-Einheit (SubApp)

```{index} single: Uebung_026_sub: Sequenz-Aktor-Einheit (SubApp)
```

[Uebung_026_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_026_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_026_sub`. Dieser Baustein dient als standardisiertes Interface für Aktoren innerhalb einer komplexen Schrittkette.


## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [ISOBUS: Wie Logos auf euer Traktor-Terminal kommen – Das Picture Graphic Objekt erklärt](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Wie-Logos-auf-euer-Traktor-Terminal-kommen--Das-Picture-Graphic-Objekt-erklrt-e36aagf)
* [Bulldog Legende: Wie der einfache LANZ-Traktor die Landwirtschaft revolutionierte und zum Duden-Eint](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Bulldog-Legende-Wie-der-einfache-LANZ-Traktor-die-Landwirtschaft-revolutionierte-und-zum-Duden-Eint-e39kif6)
* [Der Niedergang des Traktoren-Kults: Vom genialen Schwenkkammer-Motor zum teuren Ende der Motorenfabrik Anton Schlüter](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Der-Niedergang-des-Traktoren-Kults-Vom-genialen-Schwenkkammer-Motor-zum-teuren-Ende-der-Motorenfabrik-Anton-Schlter-e3aea7o)
* [Glühkopfmotor, Gier und Kontrollverlust: Wie die Familie Lanz ihr Traktoren-Imperium verlor](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Glhkopfmotor--Gier-und-Kontrollverlust-Wie-die-Familie-Lanz-ihr-Traktoren-Imperium-verlor-e3ab3er)
* [Schlüter: Vom Kaiserreich-Motor zum 500-PS-Giganten – Aufstieg und Fall der bärenstarken Traktoren aus Freising](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Schlter-Vom-Kaiserreich-Motor-zum-500-PS-Giganten--Aufstieg-und-Fall-der-brenstarken-Traktoren-aus-Freising-e3a8j4o)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



## Ziel der Übung

Kapselung der Ausgangs-Logik. Der Baustein trennt die Ablauf-Logik (wann muss was passieren) von der Hardware-Logik (wie wird der Zylinder angesteuert).

-----

## Beschreibung und Komponenten

[cite_start]Der Typ `Uebung_026_sub` kombiniert einen Speicher mit einer Plausibilitätsprüfung[cite: 1].

### Interne Funktionsbausteine (FBs)

  * **`E_SR`**: Speichert, ob der Aktor gerade aktiv sein soll.
  * **`QX`**: Typ `logiBUS_QX`. Steuert den physischen Port an.
  * **`E_SWITCH`**: Dient als Rückmelde-Gatter. [cite_start]Nur wenn der Speicher tatsächlich auf TRUE steht, wird das Bestätigungs-Event am Ausgang `EO1` weitergegeben[cite: 1].

-----

## Schnittstellen

[cite_start]Der Baustein bietet eine klare Event-Schnittstelle[cite: 1]:
*   **`SET`**: Schaltet den Aktor ein.
*   **`RESET`**: Schaltet den Aktor aus.
*   **`EO1`**: Meldet den erfolgreichen Vollzug des Einschaltbefehls zurück (Quittierung).

In der Hauptanwendung ermöglicht dieser Typ eine sehr übersichtliche Verschaltung der Phasenübergänge, da die Details der Speicherverwaltung und Hardware-Adressierung im Inneren verborgen bleiben.