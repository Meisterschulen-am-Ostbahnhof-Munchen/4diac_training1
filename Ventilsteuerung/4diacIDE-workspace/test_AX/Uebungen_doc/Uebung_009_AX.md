# Uebung_009_AX: Ereignis-Zähler (Ticker) mit Adaptern

```{index} single: Uebung_009_AX: Ereignis-Zähler (Ticker) mit Adaptern
```

[Uebung_009_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_009_AX.html)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_009_AX`. Hier wird die Funktionsweise eines ereignisbasierten Zählers und einer numerischen Anzeige über AX-Adapter demonstriert, was zu einer kompakteren und übersichtlicheren Verdrahtung führt.

## 🎧 Podcast

* [E_CTD: Ereignisgesteuerter Abwärtszähler nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTD-Ereignisgesteuerter-Abwrtszhler-nach-IEC-61499-e368lli)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
* [Der E_CTU in der IEC 61499: Ereignisgesteuertes Zählen und warum der Minimalist im Maschinenbau überzeugt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-in-der-IEC-61499-Ereignisgesteuertes-Zhlen-und-warum-der-Minimalist-im-Maschinenbau-berzeugt-e3a9qnq)
* [Der E_CTU-Baustein: Ereignisgesteuertes Hochzählen in der Industrie nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-Baustein-Ereignisgesteuertes-Hochzhlen-in-der-Industrie-nach-IEC-61499-e36846t)
* [Der E_PERMIT-Baustein: Der "Türsteher" für Ereignisse in IEC 61499-Systemen entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_PERMIT-Baustein-Der-Trsteher-fr-Ereignisse-in-IEC-61499-Systemen-entschlsselt-e3681m5)

## 📺 Video

* [Ereignisschalter E_SWITCH aus der IEC 61499 (Übung 86)](https://www.youtube.com/watch?v=Gev-kGR4-Tc)
* [Gesteuerte Verbreitung eines Ereignisses E_PERMIT aus der IEC 61499 (Übung 94)](https://www.youtube.com/watch?v=ry5LTRd9H3M)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmasch...](https://www.youtube.com/watch?v=qdlmZlcQir0)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)

----

![](Uebung_009_AX.png)

## Ziel der Übung

Erlernen der adapterbasierten Zählung (`AUDI_CTUD_UDINT`) und der Darstellung von Werten auf einem ISOBUS-Terminal (`Q_NumericValue_AUDI`). Der Fokus liegt auf der Nutzung von Adaptern zur Bündelung von Ereignis- und Datenfluss.

-----

## Beschreibung und Komponenten

Die Subapplikation `Uebung_009_AX.SUB` nutzt adapterbasierte Funktionsbausteine für den Taktgeber, den Zähler und die numerische Anzeige:

### Funktionsbausteine (FBs)

  * **`AE_CYCLE` & `AX_SR`**: Erzeugen einen permanenten Takt und steuern den Blinkerstatus über Adapter. Der `AX_SR` hat einen `AX`-Adapterausgang.
  * **`AX_SWITCH`**: Ein adapterbasierter Schalter, der den `AX`-Signalfluss basierend auf dem internen Blinker-Status umschaltet.
  * **`AX_PERMIT`**: Ein adapterbasiertes Ereignis-Gatter. Es lässt Ereignisse am Eingang `PERMIT.E1` nur dann zum Ausgang `EO` durch, wenn der Daten-Eingang `PERMIT.D1` auf `TRUE` steht.
  * **`AUDI_CTUD_UDINT`**: Ein adapterbasierter Vorwärts-/Rückwärtszähler. Er empfängt `CU`-Ereignisse und gibt den Zählerstand über einen `AUDI`-Adapter (`CV`) aus.
  * **`Q_NumericValue_AUDI`**: Ein ISOBUS-Ausgangsbaustein zur Anzeige einer Zahl auf dem Bildschirm. Er empfängt den Wert über einen `AUDI`-Adapter (`u32NewValue`).

-----

## Funktionsweise

1.  **Takt & Blinker**: `AE_CYCLE` erzeugt jede Sekunde ein `AE`-Ereignis. `AX_SR` toggelt seinen `AX`-Adapterausgang (`Q`) bei jedem Takt.
2.  **Konditionierung**: Der `AX_PERMIT` erhält das `AX`-Signal des `AX_SR`. Nur wenn der Blinker `TRUE` ist, wird ein Ereignis (`EO`) weitergeleitet.
3.  **Zählung**: Die durchgelassenen Events erreichen den `CU`-Eingang des `AUDI_CTUD_UDINT`. Der Zählerstand wird über den `CV`-Adapter ausgegeben.
4.  **Anzeige**: Bei jeder Änderung des Zählerstands (`AUDI_CTUD_UDINT.CO`) wird der Wert über den `u32NewValue`-Adapter an `Q_NumericValue_AUDI` gesendet.
5.  Auf dem ISOBUS-Terminal sieht der Nutzer eine Zahl, die stetig ansteigt.

-----

## Fazit

Diese Übung demonstriert die Vorteile einer konsequenten Adapter-basierten Entwicklung. Das Baustein-Netzwerk ist deutlich übersichtlicher, da Ereignis- und Datenflüsse in einer einzigen Verbindung gebündelt werden. Dies reduziert die Komplexität und Fehleranfälligkeit erheblich und erleichtert die Integration in verteilte Systeme.