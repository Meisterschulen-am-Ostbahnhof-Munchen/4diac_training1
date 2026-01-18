# Uebung_020d: Manuelle Ausschaltverzögerung

```{index} single: Uebung_020d: Manuelle Ausschaltverzögerung
```

[Uebung_020d](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020d.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020d`. Hier wird die Funktion einer Ausschaltverzögerung (TOF) manuell aus Grundbausteinen aufgebaut.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020d.png)


## Ziel der Übung

Realisierung eines Nachlauf-Verhaltens. Der Ausgang soll beim Drücken des Tasters sofort angehen, aber nach dem Loslassen noch eine definierte Zeit (2 Sekunden) aktiv bleiben.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_020d.SUB` wird die TOF-Logik durch geschickte Verknüpfung von `E_DELAY` und `E_RS` implementiert[cite: 1].

### Funktionsweise

1.  **Einschalten**: Nutzer drückt `I1`. Die Weiche leitet das Event an `EO1`. Dies bewirkt zwei Dinge:
    *   Der Speicher `E_RS` wird sofort gesetzt (Lampe geht an).
    *   Ein eventuell noch laufender Verzögerungs-Timer wird gestoppt (`E_DELAY.STOP`).
2.  **Halten**: Solange gedrückt wird, bleibt der Zustand stabil.
3.  **Ausschalten**: Nutzer lässt `I1` los. Die Weiche schaltet auf `EO0`. Dies triggert den Verzögerungs-Timer (`E_DELAY.START`).
4.  **Nachlauf**: Erst wenn die 2 Sekunden abgelaufen sind, feuert der Timer `E_DELAY.EO` ➡️ `E_RS.R`. Der Speicher wird zurückgesetzt, die Lampe geht aus.

-----

## Anwendungsbeispiel

**Innenraum-Beleuchtung im Auto**: Sobald die Tür geöffnet wird (`I1`), geht das Licht an. Wird die Tür geschlossen, bleibt das Licht noch einige Sekunden hell, damit man sich anschnallen kann, und geht dann erst aus.