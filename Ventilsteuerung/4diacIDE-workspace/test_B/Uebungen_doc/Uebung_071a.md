# Uebung_071a: Synchronisierte Schwellwert-Logik

```{index} single: Uebung_071a: Synchronisierte Schwellwert-Logik
```

[Uebung_071a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_071a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_071a`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
* [Digitale Logik Flip-Flops und Datentypen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Digitale-Logik-Flip-Flops-und-Datentypen-e3dic6t)
* [Wie simple Schalter "denken": Die Grundlagen der Digitaltechnik – Gatter, Logik und die Macht von 1 und 0](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Wie-simple-Schalter-denken-Die-Grundlagen-der-Digitaltechnik--Gatter--Logik-und-die-Macht-von-1-und-0-e3ae98g)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_071a.png)


## Übersicht

[cite_start]Diese Variante der Übung 071 nutzt ein D-Flip-Flop (`E_D_FF`) zur zeitlichen Synchronisation des Schaltsignals[cite: 1].
Das Ergebnis des Geschwindigkeitsvergleichs wird erst beim Eintreffen des Bestätigungs-Events am Takteingang des Flip-Flops fest übernommen und an den Ausgang `Q1` weitergegeben. Dies sorgt für ein stabileres Schaltverhalten in komplexeren Logik-Netzwerken, indem es sicherstellt, dass Daten und Ereignisse exakt im Gleichtakt verarbeitet werden.