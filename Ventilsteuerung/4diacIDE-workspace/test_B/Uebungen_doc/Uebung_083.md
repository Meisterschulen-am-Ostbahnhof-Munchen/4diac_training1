# Uebung_083: Präzisions-Zähler (UDINT)

```{index} single: Uebung_083: Präzisions-Zähler (UDINT)
```

[Uebung_083](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_083.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_083`.


## 📺 Video

* [Zusätzlich: Uebung_083: Aufwärts/Abwärts zählen: E_CTUD_UDINT Datentyp UDINT; mit Anzeige am VT.](https://www.youtube.com/watch?v=oTPDtsw5eAw)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [E_CTD: Ereignisgesteuerter Abwärtszähler nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTD-Ereignisgesteuerter-Abwrtszhler-nach-IEC-61499-e368lli)
* [E_CTUD: Bidirektionaler Zähler in IEC 61499 Systemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTUD-Bidirektionaler-Zhler-in-IEC-61499-Systemen-e368lmb)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
* [Löt-Meisterklasse Profi-Tricks für Präzisionselektronik](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Lt-Meisterklasse-Profi-Tricks-fr-Przisionselektronik-e3augdi)
* [Open Circuits: Die verborgene Schönheit und Ingenieurskunst im Inneren unserer Elektronik – Präzisionsarbeit, Katzenhaar und Fokus-Stapelung](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Open-Circuits-Die-verborgene-Schnheit-und-Ingenieurskunst-im-Inneren-unserer-Elektronik--Przisionsarbeit--Katzenhaar-und-Fokus-Stapelung-e3a9r77)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_083.png)


## Übersicht

[cite_start]Diese Übung verwendet den Baustein `E_CTUD_UDINT`[cite: 1]. Im Gegensatz zum Standard-Zähler (der meist nur bis 65.535 zählt) nutzt dieser Typ den Datentyp `UDINT` (Unsigned Double Integer). Damit können Ereignisse bis zu einem Wert von über 4 Milliarden gezählt werden.
Zusätzlich zur Ansteuerung der Lampen `Q1` und `Q2` wird der aktuelle Zählerstand (`CV`) direkt an eine numerische Anzeige am ISOBUS-Terminal gesendet. Dies ermöglicht eine genaue Beobachtung des Zählvorgangs in Echtzeit.