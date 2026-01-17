# Uebung_020e2: Zyklischer TOF-Timer (FB_TOF)

[Uebung_020e2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020e2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020e2`. Hier wird der klassische IEC 61131-3 Timer-Baustein `FB_TOF` verwendet, der eine regelmäßige Triggerung (Takt) benötigt.

**Wichtiger Hinweis: Dieser Baustein funktioniert nur korrekt, wenn er zyklisch aufgerufen wird.**


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020e2.png)


## Übersicht

Demonstration des klassischen `FB_TOF` Bausteins. Da dieser Baustein zyklische Abfragen benötigt, wird er wie in Übung 020c3 über einen `E_CYCLE` (hier 500ms) angetrieben. Zusätzlich sorgt ein zweiter `E_SWITCH` am Ausgang dafür, dass der Taktgeber `E_CYCLE` gestoppt wird, sobald die Nachlaufzeit beendet ist.
