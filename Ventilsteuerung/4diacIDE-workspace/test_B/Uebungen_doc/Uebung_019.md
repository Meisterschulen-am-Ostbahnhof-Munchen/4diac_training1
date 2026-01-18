# Uebung_019: Maskenumschaltung (Screen-Switch)

```{index} single: Uebung_019: Maskenumschaltung (Screen-Switch)
```

[Uebung_019](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_019.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_019`. Hier wird gezeigt, wie das Programm die aktive Anzeige (Data Mask) auf dem Terminal umschalten kann.

## 📺 Video

* [2025-02-02 19-11-57 DI_LONG_PRESS_HOLD (Teil 2)](https://www.youtube.com/watch?v=vpA6dfZDwh0)
* [2025-03-30 19-41-34 Python Installation prüfen](https://www.youtube.com/watch?v=pBo6QPdWtgA)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-11-02 13-19-52 LogiBUS® auf dem Weg zu Eclipse 4diac™ 3.0 - Umstellung eines Projektes](https://www.youtube.com/watch?v=5J_PuNkwxNo)
* [2025-11-15 12-19-33 Montage Hutschienenmoped logiBUS® -- Teil 2 -- Einführung und Löten](https://www.youtube.com/watch?v=nohE36SZY9M)

## 🎧 Podcast

* [Als Landtechnik-Spezialist durch die Hölle: Wie Lanz-Wery Krieg, Besatzung und Hyperinflation überlebte – Einblicke in Original-Geschäftsberichte 1915-1922](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Als-Landtechnik-Spezialist-durch-die-Hlle-Wie-Lanz-Wery-Krieg--Besatzung-und-Hyperinflation-berlebte--Einblicke-in-Original-Geschftsberichte-1915-1922-e39athj)
* [Land- und Forstwirtschaft 4.0: Das Fundament der Sicherheit – Analyse der DIN EN ISO 25119-1 und der](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Land--und-Forstwirtschaft-4-0-Das-Fundament-der-Sicherheit--Analyse-der-DIN-EN-ISO-25119-1-und-der-e39kn2f)
* [RASE: How 19th-Century England Revolutionized Agriculture Through "Practice with Science"](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/RASE-How-19th-Century-England-Revolutionized-Agriculture-Through-Practice-with-Science-e36eb1v)
* [Rudolf Diesel: Geniales Werk, mysteriöses Ende – Wer verschwand 1913 auf der Fähre?](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Rudolf-Diesel-Geniales-Werk--mysterises-Ende--Wer-verschwand-1913-auf-der-Fhre-e396oa6)
* [Smart Farming Vision 1991 Auernhammers Blaupausen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Smart-Farming-Vision-1991-Auernhammers-Blaupausen-e3b09r2)

----

![](Uebung_019.png)

## Ziel der Übung

Verwendung des Bausteins `Q_ActiveMask` zur Navigation auf dem Terminal. Es wird demonstriert, wie physische Taster genutzt werden, um zwischen verschiedenen Bedien-Seiten zu blättern.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_019.SUB` nutzt zwei physische Taster, um zwischen zwei Arbeitsmasken zu wählen[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` & `I2`**: Physische Eingangs-Taster.
  * **`F_SEL_E_2`**: Ein Ereignis-Selektor. Er hat zwei `REQ`-Eingänge und gibt beim jeweiligen Trigger die zugeordnete Konstante am Datenausgang aus.
  * **`Q_ActiveMask`**: Der ISOBUS-Ausgangsbaustein. [cite_start]Er sendet den Befehl zum Wechseln der Maske an das Terminal[cite: 1].

-----

## Funktionsweise

*   Druck auf **Taster 1** ➡️ `F_SEL_E_2` liefert die ID von `DataMask_M1` ➡️ `Q_ActiveMask` schaltet das Terminal auf Seite 1.
*   Druck auf **Taster 2** ➡️ `F_SEL_E_2` liefert die ID von `DataMask_M2` ➡️ `Q_ActiveMask` schaltet das Terminal auf Seite 2.

Das System steuert hier also aktiv, was der Bediener sieht.

-----

## Anwendungsbeispiel

**Kontextabhängige Steuerung**:
Wenn der Fahrer am physischen Bedienpult den Schalter für "Pflugbetrieb" umlegt, wechselt das Terminal automatisch von der Straßenansicht zur Feldansicht mit allen relevanten Tiefeneinstellungen. Dies erspart dem Fahrer das manuelle Suchen der richtigen Seite am Touchscreen während der Fahrt.