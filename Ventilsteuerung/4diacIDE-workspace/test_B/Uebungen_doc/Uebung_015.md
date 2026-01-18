# Uebung_015: Dynamische UI mit Object Pointern

```{index} single: Uebung_015: Dynamische UI mit Object Pointern
```

[Uebung_015](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_015.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_015`. Hier wird eine fortgeschrittene ISOBUS-Technik demonstriert: Das Umschalten von Object Pointern, um Bildschirminhalte dynamisch auszutauschen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-03-30 16-59-57 Verknüpfung von Object ID und Objektname](https://www.youtube.com/watch?v=FuZTizT48JU)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
* [ISOBUS Object Pointer: Das Geheimnis dynamischer Displays und effizienter Fehlerdiagnose](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Object-Pointer-Das-Geheimnis-dynamischer-Displays-und-effizienter-Fehlerdiagnose-e36bp75)
* [Decoding Industrial Control: Function Blocks, Object-Oriented Principles, and the Power of IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-prime-course-en/episodes/Decoding-Industrial-Control-Function-Blocks--Object-Oriented-Principles--and-the-Power-of-IEC-61499-e3722d5)
* [ISOBUS Output Meter: Dynamische Anzeigen meistern – vom Zeiger bis zur Visualisierung auf dem VT](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Output-Meter-Dynamische-Anzeigen-meistern--vom-Zeiger-bis-zur-Visualisierung-auf-dem-VT-e36t2tp)
* [ISOBUS-Container: Dynamische Bedienfelder für klare Sicht und mehr Effizienz](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Container-Dynamische-Bedienfelder-fr-klare-Sicht-und-mehr-Effizienz-e36alr9)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_015.png)


## Ziel der Übung

Erlernen der Verwendung von `Object Pointer` Objekten. Ein Pointer ist ein Platzhalter auf dem Bildschirm, dem zur Laufzeit die ID eines anderen Objekts zugewiesen werden kann. Dies ist effizienter als das Ausblenden vieler Einzelobjekte.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_015.SUB` wird ein Object Pointer (`ObjectPointer_P1`) zwischen einer Schaltfläche (`Button_A1`) und einem leeren Zustand (`ID_NULL`) umgeschaltet[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_UP_F1` & `F2`**: Steuern die Auswahl.
  * **`F_SEL`**: Ein Auswahl-Baustein (Selection). [cite_start]Je nach Eingang `G` (vom Speicher `E_SR`) gibt er entweder den Wert `ID_NULL` (0) oder die Objekt-ID von `Button_A1` aus[cite: 1].
  * **`Q_NumericValue`**: Wird hier zweckentfremdet, um die ID an den Pointer zu senden (da ein Pointer-Update technisch das Senden einer neuen ID an die Pointer-Objekt-ID ist).

-----

## Funktionsweise

1.  Nutzer drückt **F1** ➡️ Speicher wird `TRUE` ➡️ `F_SEL` schaltet `Button_A1` durch.
2.  Die ID von `Button_A1` wird an `ObjectPointer_P1` gesendet.
3.  Auf dem Bildschirm erscheint an der Position des Pointers plötzlich die Schaltfläche `A1`.
4.  Nutzer drückt **F2** ➡️ ID `0` wird gesendet ➡️ Die Stelle auf dem Bildschirm wird wieder leer.

-----

## Anwendungsbeispiel

**Kontextsensitive Buttons**:
Ein zentraler Platz auf dem Terminal soll je nach Arbeitsmodus unterschiedliche Funktionen anzeigen (z.B. im Modus "Transport" ein Straßensymbol, im Modus "Feld" ein Pflugsymbol). Anstatt zwei Buttons übereinander zu legen und zu verstecken, wird ein Pointer genutzt, der je nach Modus auf das eine oder andere Bild-Objekt verweist.