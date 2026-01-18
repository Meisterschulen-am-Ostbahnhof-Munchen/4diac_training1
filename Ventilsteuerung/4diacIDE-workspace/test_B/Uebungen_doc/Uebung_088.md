# Uebung_088: Fallende Flanke (F_TRIG)

```{index} single: Uebung_088: Fallende Flanke (F_TRIG)
```

[Uebung_088](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_088.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_088`. Hier wird die gezielte Reaktion auf das Ende eines Signals (Ausschaltflanke) demonstriert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [R_TRIG & F_TRIG: So erkennen SPS-Steuerungen Signalflanken zuverlässig – ohne Doppelbehandlung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/R_TRIG--F_TRIG-So-erkennen-SPS-Steuerungen-Signalflanken-zuverlssig--ohne-Doppelbehandlung-e370kqh)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_088.png)


## Ziel der Übung

Verwendung des Bausteins `E_F_TRIG` (Falling Edge Trigger). Im Gegensatz zum einfachen `E_SWITCH` filtert dieser Baustein alle Ereignisse heraus, außer den Moment des Übergangs von `TRUE` nach `FALSE`.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_088.SUB` wird die Reaktion auf eine UND-Logik verglichen[cite: 1].

### Funktionsweise

1.  Zwei Taster `I1` und `I2` werden über ein `AND_2` Gatter verknüpft.
2.  Das Ergebnis (`OUT`) liegt am Eingang `QI` des Flanken-Triggers an.
3.  **Positive Flanke**: Schaltet man die Taster ein, passiert am Ausgang nichts.
4.  **Negative Flanke**: Erst in dem Moment, in dem die UND-Bedingung wieder verloren geht (indem man **einen der beiden** Taster loslässt), feuert `E_F_TRIG.EO`.
5.  Das Flip-Flop toggelt, die Lampe wechselt den Zustand.

-----

## Anwendungsbeispiel

**Sicherheits-Check beim Ausschalten**:
Eine Reinigungsfunktion soll erst dann starten, wenn der Hauptschalter der Maschine ausgeschaltet wurde. Der `F_TRIG` erkennt diesen Ausschalt-Moment und löst den Folgeschritt aus.