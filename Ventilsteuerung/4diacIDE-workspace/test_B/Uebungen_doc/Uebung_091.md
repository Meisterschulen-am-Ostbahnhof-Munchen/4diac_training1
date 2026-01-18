# Uebung_091: Ereignis-Salve (E_TRAIN)

```{index} single: Uebung_091: Ereignis-Salve (E_TRAIN)
```

[Uebung_091](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_091.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_091`. Hier wird die automatische Erzeugung einer festen Anzahl von Ereignissen demonstriert.


## 📺 Video

* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Ereignisschalter E_SWITCH aus der IEC 61499 (Übung 86)](https://www.youtube.com/watch?v=Gev-kGR4-Tc)
* [Gesteuerte Verbreitung eines Ereignisses E_PERMIT aus der IEC 61499 (Übung 94)](https://www.youtube.com/watch?v=ry5LTRd9H3M)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)

## Podcast
* [Der E_CTU in der IEC 61499: Ereignisgesteuertes Zählen und warum der Minimalist im Maschinenbau überzeugt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-in-der-IEC-61499-Ereignisgesteuertes-Zhlen-und-warum-der-Minimalist-im-Maschinenbau-berzeugt-e3a9qnq)
* [Der E_CTU-Baustein: Ereignisgesteuertes Hochzählen in der Industrie nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-Baustein-Ereignisgesteuertes-Hochzhlen-in-der-Industrie-nach-IEC-61499-e36846t)
* [Der E_PERMIT-Baustein: Der "Türsteher" für Ereignisse in IEC 61499-Systemen entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_PERMIT-Baustein-Der-Trsteher-fr-Ereignisse-in-IEC-61499-Systemen-entschlsselt-e3681m5)
* [DIN EN 61499-1: Die Lego-Steine für flexible und ereignisgesteuerte Industriesteuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Die-Lego-Steine-fr-flexible-und-ereignisgesteuerte-Industriesteuerungen-e3681o1)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_091.png)


## Ziel der Übung

Verwendung des Bausteins `E_TRAIN`. Ziel ist es, nach einem einzelnen Start-Impuls eine definierte Folge von Ereignissen auszulösen.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_091.SUB` wird ein Ereignis-Zug (Train) zur Steuerung eines Flip-Flops genutzt[cite: 1].

### Funktionsweise

1.  Der Nutzer klickt einmal auf Taster **I1**.
2.  Der Baustein `E_TRAIN` startet seine Arbeit.
3.  Laut Parameter `N=8` und `DT=1s` sendet der Baustein nun exakt **8 Ereignisse** im Abstand von jeweils einer Sekunde aus.
4.  Diese Ereignisse gelangen an das Toggle-Flip-Flop.
5.  Die Lampe an `Q1` blinkt daraufhin genau viermal (4 x An, 4 x Aus) und bleibt dann in der letzten Position stehen.

-----

## Anwendungsbeispiel

**Automatisches Abkippen**:
Ein Hydraulikzylinder soll zum Lockern von Material dreimal kurz ruckeln. Ein Tastendruck löst die Salve von 6 Steuerbefehlen (Ausfahren-Einfahren x 3) aus, woraufhin die Steuerung den Vorgang selbstständig beendet.