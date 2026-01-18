# Uebung_072c: Integration der Geschwindigkeit (Wegberechnung)

```{index} single: Uebung_072c: Integration der Geschwindigkeit (Wegberechnung)
```

[Uebung_072c](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_072c.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_072c`. Hier wird eine mathematische Methode gezeigt, um aus der Geschwindigkeit die zurückgelegte Strecke selbst zu berechnen (Integration).


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Druckbegrenzungsventile: Lebensversicherung der Hydraulik – Arten, Funktion und Systemintegration](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Druckbegrenzungsventile-Lebensversicherung-der-Hydraulik--Arten--Funktion-und-Systemintegration-e373nal)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_072c.png)


## Ziel der Übung

Verwendung des Bausteins `INTEGRAL`. Es wird demonstriert, wie man einen Wegwert manuell berechnet, falls die TECU keinen kumulierten Distanzwert liefert oder dieser für eine Teilmessung (Tageskilometerzähler) genullt werden soll.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_072c.SUB` berechnet den Weg durch zeitliche Integration der radarbasierten Geschwindigkeit[cite: 1].

### Funktionsbausteine (FBs)

  * **`I_GBSD`**: Liefert die aktuelle Geschwindigkeit.
  * **`CYCLE_TIME`**: Misst die Zeit zwischen zwei Geschwindigkeits-Nachrichten (`TM`).
  * **`INTEGRAL`**: Summiert das Produkt aus Geschwindigkeit und Zeit (`v * dt`) auf.
  * **`OFFSET_UDINT`**: Erlaubt das Addieren eines Startwerts oder das Zurücksetzen der Zählung.

-----

## Funktionsweise

Das Programm führt permanent die physikalische Grundformel `Weg = Geschwindigkeit * Zeit` aus. Da die TECU-Daten nie ganz glatt sind, nutzt der `INTEGRAL` Baustein kleine Zeitintervalle (`CYCLE_TIME`), um eine hohe Genauigkeit der aufsummierten Strecke zu erreichen. Das Ergebnis wird am Terminal als `Wheel_based_machine_distance` angezeigt (auch wenn es hier aus Radar-Daten berechnet wurde).