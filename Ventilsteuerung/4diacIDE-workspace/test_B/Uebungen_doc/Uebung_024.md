# Uebung_024: Sequenz mit Wartezeit (Delay)

```{index} single: Uebung_024: Sequenz mit Wartezeit (Delay)
```

[Uebung_024](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_024.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_024`. Hier wird eine zeitliche Pause in den automatischen Ablauf integriert.


## 📺 Video

* [2024 09 05 17 59 50 Bayerische Staatsbibliothek Buch Zugriff](https://www.youtube.com/watch?v=0qTGNMfAspU)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [Analyse der Novellierung der Meisterprüfungsverordnung im Land- und Baumaschinenmechatroniker-Handwerk: Ein Detaillierter Vergleich der Verordnungen von 2024 und 2001](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Analyse-der-Novellierung-der-Meisterprfungsverordnung-im-Land--und-Baumaschinenmechatroniker-Handwerk-Ein-Detaillierter-Vergleich-der-Verordnungen-von-2024-und-2001-e37aejv)
* [Strip-Till im Maisanbau: Wie Hochpräzision Wasser spart und den Boden schützt – Einblick in die Agrartechnik 2024](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Strip-Till-im-Maisanbau-Wie-Hochprzision-Wasser-spart-und-den-Boden-schtzt--Einblick-in-die-Agrartechnik-2024-e3ahcvp)
* [E_DELAY in IEC 61499: Präzise, Abbrechbare Zeitverzögerung in Steuerungssystemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_DELAY-in-IEC-61499-Przise--Abbrechbare-Zeitverzgerung-in-Steuerungssystemen-e3674le)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_024.png)


## Ziel der Übung

Integration von Zeitgliedern (`E_DELAY`) in eine Ereigniskette.

-----

## Funktionsweise

[cite_start]Im Vergleich zu Übung 023 wird zwischen zwei Schritten ein Verzögerungs-Baustein eingefügt[cite: 1].
Wenn Zylinder 2 seine Endlage erreicht (`F3`), wird nicht sofort der nächste Schritt ausgelöst, sondern der Eingang `E_DELAY.START` getriggert. Erst nach Ablauf der Zeit `DT` (hier 2 Sekunden) feuert das `EO`-Event und setzt die Sequenz fort (z.B. Start des Einfahrens).

-----

## Anwendungsbeispiel

**Pressvorgang**:
Ein Zylinder fährt aus und drückt zwei Bauteile zusammen. Sobald die Endlage erreicht ist, muss der Druck für 2 Sekunden gehalten werden (Wartezeit), bevor der Zylinder wieder einfährt und das Werkstück freigibt.