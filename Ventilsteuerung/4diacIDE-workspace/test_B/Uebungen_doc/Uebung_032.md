# Uebung_032: Mehrfarbige LED-Streifen Effekte

[Uebung_032](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_032.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_032`. Hier werden vorkonfigurierte Farbbausteine für LED-Streifen genutzt.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_032.png)


## Ziel der Übung

Verwendung des Bausteins `logiBUS_LED_strip_QX`. Dies ist ein High-Level Baustein, der Farbe, Frequenz und Hardware-Anbindung für RGB-Streifen in einem Block vereint.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_032.SUB` werden vier verschiedene Farben (Grün, Gelb, Rot, Blau) auf vier Taster gemappt[cite: 1].

### Funktionsbausteine (FBs)

  * **`logiBUS_LED_strip_QX`**: Kombi-Baustein für RGB-Streifen.
  * **Parameter**:
    * `Colour`: Auswahl aus einer Palette (z.B. `LED_RED`).
    * `FREQ`: Blinkfrequenz (hier einheitlich 5 Hz).

-----

## Funktionsweise

Jeder Taster aktiviert "seine" Farbe auf dem Streifen. Da alle Bausteine auf den Parameter `Output_strip` (Kanal 0) konfiguriert sind, überschreiben sie sich gegenseitig.
*   Druck auf **Grün** ➡️ Streifen blitzt schnell grün.
*   Druck auf **Rot** ➡️ Streifen wechselt sofort auf schnelles rotes Blitzen.

Dies ermöglicht eine sehr schnelle Programmierung von farbigen Status-Signalen.
