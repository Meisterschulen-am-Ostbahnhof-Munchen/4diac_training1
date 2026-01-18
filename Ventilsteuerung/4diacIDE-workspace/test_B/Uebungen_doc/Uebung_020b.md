# Uebung_020b: Manuelle Einschaltverzögerung

```{index} single: Uebung_020b: Manuelle Einschaltverzögerung
```

[Uebung_020b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020b`. Hier wird eine Einschaltverzögerung (TON) manuell aus Grundbausteinen aufgebaut.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020b.png)


## Ziel der Übung

Verstehen der Zeitsteuerung durch Ereignisverzögerung (`E_DELAY`). Es wird gezeigt, wie ein Timer-Verhalten ("Licht geht erst nach 2 Sekunden an") durch das gezielte Verzögern und Abbrechen von Ereignissen realisiert wird.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_020b.SUB` wird ein Verzögerungs-Baustein zwischen die Eingangs-Weiche und den Speicher geschaltet[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_DELAY`**: Wartet die Zeit `DT` (2 Sekunden) ab.
  * **`E_SWITCH`**: Steuert den Start und Stopp des Timers.

-----

## Funktionsweise

1.  **Start**: Nutzer drückt `I1`. Die Weiche schaltet auf `EO1` ➡️ `E_DELAY.START`.
2.  **Warten**: Wenn der Nutzer den Taster für volle 2 Sekunden gedrückt hält, feuert `E_DELAY.EO` ➡️ `E_RS.S`. Die Lampe geht an.
3.  **Abbruch**: Lässt der Nutzer den Taster vor Ablauf der 2 Sekunden los, schaltet die Weiche auf `EO0`. Dieses Event triggert `E_DELAY.STOP` (Timer wird gelöscht) **und** `E_RS.R` (Ausgang wird sicher auf FALSE gesetzt).

Ergebnis: Einschaltverzögerung mit sofortigem Abbruch bei Signalverlust.