# Uebung_011a2: Dynamische Anzeige (Long Press Release)

```{index} single: Uebung_011a2: Dynamische Anzeige (Long Press Release)
```

[Uebung_011a2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_011a2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_011a2`.


## 📺 Video

* [Zusätzlich: Uebung_083: Aufwärts/Abwärts zählen: E_CTUD_UDINT Datentyp UDINT; mit Anzeige am VT.](https://www.youtube.com/watch?v=oTPDtsw5eAw)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-02-02 18-56-54 DI_LONG_PRESS_HOLD (Teil 1)](https://www.youtube.com/watch?v=8pkKq_8HAIQ)
* [2025-02-02 19-11-57 DI_LONG_PRESS_HOLD (Teil 2)](https://www.youtube.com/watch?v=vpA6dfZDwh0)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)

## Podcast
* [ISOBUS Output Meter: Dynamische Anzeigen meistern – vom Zeiger bis zur Visualisierung auf dem VT](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Output-Meter-Dynamische-Anzeigen-meistern--vom-Zeiger-bis-zur-Visualisierung-auf-dem-VT-e36t2tp)
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
* [ISOBUS-Bedienoberflächen: Wenn Tasten und Hauptanzeige unterschiedlich skalieren – ISO 11783-6 entschlüsselt](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Bedienoberflchen-Wenn-Tasten-und-Hauptanzeige-unterschiedlich-skalieren--ISO-11783-6-entschlsselt-e36a8n8)
* [ISOBUS-Container: Dynamische Bedienfelder für klare Sicht und mehr Effizienz](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Container-Dynamische-Bedienfelder-fr-klare-Sicht-und-mehr-Effizienz-e36alr9)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_011a2.png)


## Übersicht

[cite_start]Strukturell identisch mit `Uebung_011a`, verwendet diese Variante das Ereignis `BUTTON_LONG_PRESS_UP` am Eingangsbaustein `logiBUS_ID`[cite: 1]. Die Anzeige auf dem Terminal wird hier erst dann aktualisiert, wenn ein zuvor erkannter langer Tastendruck durch Loslassen beendet wurde. Dies demonstriert eine weitere Variante der Interaktions-Bestätigung für numerische Werte.