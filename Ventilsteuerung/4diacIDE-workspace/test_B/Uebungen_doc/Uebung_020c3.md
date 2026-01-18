# Uebung_020c3: Zyklische Timer-Aktualisierung (FB_TON)

```{index} single: Uebung_020c3: Zyklische Timer-Aktualisierung (FB_TON)
```

[Uebung_020c3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020c3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020c3`. Hier wird der klassische IEC 61131-3 Timer-Baustein `FB_TON` verwendet, der eine regelmäßige Triggerung (Takt) benötigt.

**Wichtiger Hinweis: Dieser Baustein funktioniert nur korrekt, wenn er zyklisch aufgerufen wird.**



## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Die drei Timer der DIN EN 61131-3 entschlüsselt – TP, TON & TOF präzise erklärt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Die-drei-Timer-der-DIN-EN-61131-3-entschlsselt--TP--TON--TOF-przise-erklrt-e3dma77)
* [E_TOF vs. FB_TOF: Der Event-Timer, der nicht zyklisch tickt – Revolution für Automatisierungssysteme?](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_TOF-vs--FB_TOF-Der-Event-Timer--der-nicht-zyklisch-tickt--Revolution-fr-Automatisierungssysteme-e3673qk)
* [E_TON in der Industrieautomation: Wie ein simpler Timer Sicherheit und Stabilität schafft](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_TON-in-der-Industrieautomation-Wie-ein-simpler-Timer-Sicherheit-und-Stabilitt-schafft-e3672u9)
* [Ereignisgesteuerte Timer: Wann welcher am Lüfter Sinn macht – ETON, ETOF, ETP & mehr entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Ereignisgesteuerte-Timer-Wann-welcher-am-Lfter-Sinn-macht--ETON--ETOF--ETP--mehr-entschlsselt-e36c4o0)
* [FB_TOF und E_TOF: Verzögerungstimer in IEC 61131-3 und 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/FB_TOF-und-E_TOF-Verzgerungstimer-in-IEC-61131-3-und-61499-e368e2d)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020c3.png)


## Ziel der Übung

Das Ziel ist es, eine Einschaltverzögerung mit einem klassischen SPS-Verhalten (inkl. ET-Ausgang) in einer ereignisbasierten Umgebung zu realisieren. Im Gegensatz zum ereignisbasierten `E_TON` benötigt der `FB_TON` einen regelmäßigen Trigger (Abtastung), um seine interne Zeitrechnung und den Ausgang `ET` zu aktualisieren.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_020c3.SUB` wird ein Taktgeber verwendet, um den klassischen Timer anzutreiben[cite: 1].

### Funktionsbausteine (FBs)

  * **`FB_TON`**: Der klassische TON-Baustein.
  * **`E_CYCLE`**: Ein Zeitgeber, der alle 500ms ein Ereignis an den `REQ`-Eingang des Timers sendet.

-----

## Funktionsweise

Damit der `FB_TON` korrekt funktioniert, muss er "befragt" werden.
1.  Der Nutzer drückt Taster `I1`. Das Signal liegt am Dateneingang `IN` des Timers an.
2.  Gleichzeitig startet der Taster über eine Weiche den `E_CYCLE`.
3.  Alle 500ms fordert der Cycle den Timer zur Berechnung auf (`REQ`).
4.  Erst bei diesen Abfragen prüft der Timer, wie viel Zeit vergangen ist.
5.  Sobald die 5 Sekunden erreicht sind, wechselt der Ausgang `Q` auf TRUE.

Diese Methode ist notwendig, wenn man Bausteine aus der 61131-Welt in die 61499-Event-Welt integriert.