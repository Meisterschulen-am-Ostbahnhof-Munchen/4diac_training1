# Uebung_020a: Manueller Speicher (Standard-Pins)

```{index} single: Uebung_020a: Manueller Speicher (Standard-Pins)
```

[Uebung_020a](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020a.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020a`. Hier wird die manuelle Erzeugung von Setz- und Rücksetz-Ereignissen aus einem Standard-Datensignal demonstriert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [4diac IDE: Wie der IEC 61499 Standard die Industrieautomatisierung revolutioniert](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/4diac-IDE-Wie-der-IEC-61499-Standard-die-Industrieautomatisierung-revolutioniert-e36756a)
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* [IEC 61499 vs. 61131: Brauchen wir einen neuen Standard für IIoT? Analyse einer hitzigen Debatte um Verteilte Intelligenz](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-vs--61131-Brauchen-wir-einen-neuen-Standard-fr-IIoT--Analyse-einer-hitzigen-Debatte-um-Verteilte-Intelligenz-e3ahc2r)
* [IEC 61499: Befreit der neue Standard die Industrieautomation? Ein Vergleich mit 61131 und die Brücke zwischen OT & IT.](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Befreit-der-neue-Standard-die-Industrieautomation--Ein-Vergleich-mit-61131-und-die-Brcke-zwischen-OT--IT-e368446)
* [IEC 61499: Revolution der Industrieautomation – Warum der neue Standard Ihre Systeme fit für die Zukunft macht](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Industrieautomation--Warum-der-neue-Standard-Ihre-Systeme-fit-fr-die-Zukunft-macht-e375evm)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_020a.png)


## Ziel der Übung

Verständnis der Flankenerkennung. Es wird gezeigt, wie man mit einer Ereignis-Weiche (`E_SWITCH`) und einem Speicher (`E_RS`) ein Verhalten realisiert, bei dem der Ausgang beim Drücken eines Tasters eingeschaltet und beim Loslassen ausgeschaltet wird (entspricht funktional einer direkten Leitung, aber mit expliziter Logik-Trennung).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020a.SUB` nutzt einen `logiBUS_IX` Eingang, um einen `E_RS` Speicher zu steuern[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1`**: Standard-Eingang. Liefert ein Event bei jeder Änderung.
  * **`E_SWITCH`**: Leitet das Event je nach Pegel an `S` oder `R` weiter.
  * **`E_RS`**: Der Ereignis-Speicher.

-----

## Funktionsweise

1.  **Drücken (TRUE)**: Das `IND`-Event geht zur Weiche. Da `G=TRUE`, feuert `EO1` ➡️ `E_RS.S` (Setzen).
2.  **Loslassen (FALSE)**: Das `IND`-Event geht zur Weiche. Da `G=FALSE`, feuert `EO0` ➡️ `E_RS.R` (Rücksetzen).

Obwohl das Ergebnis eine 1:1 Abbildung des Eingangs ist, zeigt diese Übung den inneren Mechanismus von speichernden Systemen.