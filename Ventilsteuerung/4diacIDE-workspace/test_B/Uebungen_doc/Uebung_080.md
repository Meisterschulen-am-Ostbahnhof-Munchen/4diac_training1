# Uebung_080: Ereignis-Zähler (Up-Counter)

```{index} single: Uebung_080: Ereignis-Zähler (Up-Counter)
```

[Uebung_080](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_080.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_080`. Hier wird das grundlegende Prinzip des Zählens von Ereignissen vorgestellt.


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



![](Uebung_080.png)


## Ziel der Übung

Verwendung des Bausteins `E_CTU` (Event Count Up). Es wird gezeigt, wie man eine bestimmte Anzahl von Ereignissen (z.B. Tastendrücke) erfasst und beim Erreichen eines Grenzwerts eine Aktion auslöst.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_080.SUB` nutzt einen Zählerbaustein mit Set- und Reset-Logik[cite: 1].

### Funktionsbausteine (FBs)

  * **`DigitalInput_I1` (Count)**: Jeder Klick erhöht den Zähler.
  * **`DigitalInput_I2` (Reset)**: Setzt den Zählerstand auf Null zurück.
  * **`E_CTU`**: Der Zähler-Baustein. [cite_start]Der Parameter `PV` (Preset Value) ist auf 5 eingestellt[cite: 1].
  * **`DigitalOutput_Q1`**: Zeigt den Status des Zählers an.

-----

## Funktionsweise

1.  Der Nutzer klickt auf **I1**. Der Zählerstand (`CV`) erhöht sich bei jedem Event.
2.  Der Ausgang `Q` des Zählers wechselt auf `TRUE`, sobald der Zählerstand den Wert 5 erreicht oder überschreitet (`CV >= PV`).
3.  Die Lampe an **Q1** leuchtet auf.
4.  Durch Klick auf **I2** wird der Zähler gelöscht, `Q` wird wieder `FALSE` und die Lampe geht aus.

-----

## Anwendungsbeispiel

**Stückzähler**:
An einer Verpackungsmaschine werden die Kartons gezählt. Sobald 5 Kartons auf der Palette sind, wird ein Signal (`Q1`) gegeben, um die Palette automatisch auszufahren. Der Fahrer drückt nach dem Holen einer neuen Palette "Reset" (`I2`), um den nächsten Vorgang zu starten.