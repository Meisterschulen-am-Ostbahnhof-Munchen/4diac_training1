# Uebung_020e2: Zyklischer TOF-Timer (FB_TOF)

```{index} single: Uebung_020e2: Zyklischer TOF-Timer (FB_TOF)
```

[Uebung_020e2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020e2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020e2`. Hier wird der klassische IEC 61131-3 Timer-Baustein `FB_TOF` verwendet, der eine regelmäßige Triggerung (Takt) benötigt.

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

![](Uebung_020e2.png)


## Übersicht

Demonstration des klassischen `FB_TOF` Bausteins. Da dieser Baustein zyklische Abfragen benötigt, wird er wie in Übung 020c3 über einen `E_CYCLE` (hier 500ms) angetrieben. Zusätzlich sorgt ein zweiter `E_SWITCH` am Ausgang dafür, dass der Taktgeber `E_CYCLE` gestoppt wird, sobald die Nachlaufzeit beendet ist.