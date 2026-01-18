# Uebung_009: Ereignis-Zähler (Ticker)

```{index} single: Uebung_009: Ereignis-Zähler (Ticker)
```

[Uebung_009](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_009.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_009`. Hier verbinden wir die Zeitbasis mit einer Zählfunktion und einer numerischen Anzeige.


## 📺 Video

* [Ereignisschalter E_SWITCH aus der IEC 61499 (Übung 86)](https://www.youtube.com/watch?v=Gev-kGR4-Tc)
* [Gesteuerte Verbreitung eines Ereignisses E_PERMIT aus der IEC 61499 (Übung 94)](https://www.youtube.com/watch?v=ry5LTRd9H3M)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmasch...](https://www.youtube.com/watch?v=qdlmZlcQir0)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)

## Podcast
* [E_CTD: Ereignisgesteuerter Abwärtszähler nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTD-Ereignisgesteuerter-Abwrtszhler-nach-IEC-61499-e368lli)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
* [Der E_CTU in der IEC 61499: Ereignisgesteuertes Zählen und warum der Minimalist im Maschinenbau überzeugt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-in-der-IEC-61499-Ereignisgesteuertes-Zhlen-und-warum-der-Minimalist-im-Maschinenbau-berzeugt-e3a9qnq)
* [Der E_CTU-Baustein: Ereignisgesteuertes Hochzählen in der Industrie nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-Baustein-Ereignisgesteuertes-Hochzhlen-in-der-Industrie-nach-IEC-61499-e36846t)
* [Der E_PERMIT-Baustein: Der "Türsteher" für Ereignisse in IEC 61499-Systemen entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_PERMIT-Baustein-Der-Trsteher-fr-Ereignisse-in-IEC-61499-Systemen-entschlsselt-e3681m5)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_009.png)


## Ziel der Übung

Erlernen der ereignisbasierten Zählung (`E_CTUD`) und der Darstellung von Werten auf einem Terminal.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_009.SUB` wird ein Taktgeber genutzt, um einen Aufwärtszähler anzusteuern, dessen Wert an ein ISOBUS-Terminal gesendet wird[cite: 1].

### Funktionsbausteine (FBs)

  * **`E_CYCLE` & `E_SR`**: Erzeugen einen permanenten Takt (wie in Übung 008).
  * **`E_PERMIT`**: Ein Ereignis-Gatter. [cite_start]Es lässt Ereignisse am Eingang `EI` nur dann zum Ausgang `EO` durch, wenn der Dateneingang `PERMIT` auf `TRUE` steht[cite: 1].
  * **`E_CTUD_UDINT`**: Ein Vorwärts-/Rückwärtszähler für große Ganzzahlen.
  * **`Q_NumericValue`**: Ein ISOBUS-Ausgangsbaustein zur Anzeige einer Zahl auf dem Bildschirm.

-----

## Funktionsweise

1.  Der Blinker-Teil erzeugt jede Sekunde ein Ereignis.
2.  Dieses Ereignis wird durch `E_PERMIT` gefiltert. Da `PERMIT` mit dem blinkenden Ausgang verbunden ist, wird nur **jedes zweite** Ereignis (nämlich nur, wenn der Blinker gerade AN ist) durchgelassen.
3.  Die durchgelassenen Events erreichen den Eingang `CU` (Count Up) des Zählers.
4.  Der Zählerstand erhöht sich.
5.  Bei jeder Änderung (`CO` - Count Output) wird der neue Wert an `Q_NumericValue` gesendet.
6.  Auf dem ISOBUS-Terminal sieht der Nutzer eine Zahl, die stetig ansteigt.

-----

## Anwendungsbeispiel

**Betriebsstundenzähler**:
Die Steuerung zählt die Zeitintervalle, in denen eine bestimmte Bedingung (z.B. "Motor läuft") erfüllt ist. Der summierte Wert wird dauerhaft gespeichert und dem Bediener als Wartungsinformation am Terminal angezeigt.