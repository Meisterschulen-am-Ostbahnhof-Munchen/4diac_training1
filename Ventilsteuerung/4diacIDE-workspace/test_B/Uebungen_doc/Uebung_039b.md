# Uebung_039b: Ventil-Timing (Impulssteuerung)

```{index} single: Uebung_039b: Ventil-Timing (Impulssteuerung)
```

[Uebung_039b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_039b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## 🎧 Podcast

* [Das Ingenieurs-Datenblatt des VBCD Ventils entschlüsselt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-Ingenieurs-Datenblatt-des-VBCD-Ventils-entschlsselt-e3bgpd5)
* [Das VBCD DE A Ventil: Wie ein unsichtbarer Held Kräne, Bagger und Co. sicher steuert](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-VBCD-DE-A-Ventil-Wie-ein-unsichtbarer-Held-Krne--Bagger-und-Co--sicher-steuert-e373m6h)
* [Druckbegrenzungsventile: Lebensversicherung der Hydraulik – Arten, Funktion und Systemintegration](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Druckbegrenzungsventile-Lebensversicherung-der-Hydraulik--Arten--Funktion-und-Systemintegration-e373nal)
* [Magnetventile schützen: Dein Leitfaden gegen Spannungsspitzen in Land- und Baumaschinen](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Magnetventile-schtzen-Dein-Leitfaden-gegen-Spannungsspitzen-in-Land--und-Baumaschinen-e368l8m)

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Übersicht

[cite_start]In dieser Übung wird eine zeitgesteuerte Ventil-Abfolge unter Verwendung von Impulsgebern (`E_TP`) realisiert[cite: 1].
Ein Klick auf den Softkey **F1** startet eine Kette von Ereignissen:
1.  Ventil **Q1** wird für 8 Sekunden geöffnet.
2.  Nach einer Verzögerung von 2 Sekunden (`E_TON`) wird Ventil **Q2** für 4 Sekunden hinzugeschaltet.
Dies ermöglicht die Programmierung von festen hydraulischen Funktionszyklen (z.B. "Ballenauswurf"), bei denen mehrere Aktoren mit exaktem Zeitversatz arbeiten müssen.