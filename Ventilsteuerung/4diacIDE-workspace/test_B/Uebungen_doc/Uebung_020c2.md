# Uebung_020c2: Parametrierbare Einschaltverzögerung

```{index} single: Uebung_020c2: Parametrierbare Einschaltverzögerung
```

[Uebung_020c2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020c2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020c2`. Hier wird die Einschaltverzögerung mit einer Benutzereingabe am Terminal und Datenspeicherung kombiniert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020c2.png)


## Ziel der Übung

Dynamische Anpassung von Timer-Zeiten zur Laufzeit.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_020c2.SUB` wird die Verzögerungszeit (`PT`) nicht fest im Programm hinterlegt, sondern vom ISOBUS-Terminal eingelesen[cite: 1].

### Funktionsbausteine (FBs)

  * **`Uebung_020c2_sub`**: Eine Speicher-SubApp (wie in Übung 012a), die den vom Nutzer eingegebenen Zahlenwert verwaltet.
  * **`F_MULTIME`**: Multipliziert einen Zeitwert. Hier wird der Zahlenwert (z.B. "5") mit der Einheit `T#1s` multipliziert, um den Datentyp `TIME` für den Timer zu erzeugen (z.B. 5 Sekunden).
  * **`E_TON`**: Der eigentliche Verzögerungs-Baustein.

-----

## Funktionsweise

1.  Der Nutzer gibt am Terminal eine "5" ein.
2.  Der Wert wird im NVS gespeichert und an die Logik übergeben.
3.  `F_MULTIME` macht daraus 5 Sekunden.
4.  Wird nun der physische Taster `I1` gedrückt, verzögert `E_TON` das Signal um exakt diese 5 Sekunden.

Ändert der Nutzer den Wert am Terminal auf "10", reagiert der Timer ab sofort mit 10 Sekunden Verzögerung.