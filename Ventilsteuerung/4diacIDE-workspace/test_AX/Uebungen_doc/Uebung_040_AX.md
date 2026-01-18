# Uebung_040_AX: Lauflicht (Event-Gesteuert / Manuell)

```{index} single: Uebung_040_AX: Lauflicht (Event-Gesteuert / Manuell)
```

[Uebung_040_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_040_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_040_AX`. Im Gegensatz zu Übung 038 schaltet diese Schrittkette nicht automatisch weiter, sondern wartet auf Ereignisse.


## 📺 Video

* [D-Flip-Flop: E_D_FF aus der IEC 61499 (Übung 002c) als "Eventbremse"](https://www.youtube.com/watch?v=yGSx_0ggveE)
* [Gesteuerte Verbreitung eines Ereignisses E_PERMIT aus der IEC 61499 (Übung 94)](https://www.youtube.com/watch?v=ry5LTRd9H3M)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)

## Podcast
* [IEC 61499: Revolution der Automatisierung – Event-gesteuerte FBs und verteilte Systeme erklärt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Automatisierung--Event-gesteuerte-FBs-und-verteilte-Systeme-erklrt-e3671vb)
* [Der E_CTU in der IEC 61499: Ereignisgesteuertes Zählen und warum der Minimalist im Maschinenbau überzeugt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-in-der-IEC-61499-Ereignisgesteuertes-Zhlen-und-warum-der-Minimalist-im-Maschinenbau-berzeugt-e3a9qnq)
* [Der E_CTU-Baustein: Ereignisgesteuertes Hochzählen in der Industrie nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-Baustein-Ereignisgesteuertes-Hochzhlen-in-der-Industrie-nach-IEC-61499-e36846t)
* [DIN EN 61499-1: Die Lego-Steine für flexible und ereignisgesteuerte Industriesteuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Die-Lego-Steine-fr-flexible-und-ereignisgesteuerte-Industriesteuerungen-e3681o1)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_040_AX.png)


## Ziel der Übung

Manuelles Weiterschalten einer Schrittkette.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_040_AX.SUB` nutzt `sequence_E_08_loop_AX`. Hier sind die Eingänge für die Transitionen (`S1_S2`, `S2_S3`, ...) als Event-Inputs herausgeführt[cite: 1].

### Logik zum Weiterschalten

Um nicht 8 Taster zu benötigen, wurde eine Logik mit Zählern (`E_CTU`) und Demultiplexern (`E_DEMUX`) gebaut:
*   **Taster `I2`**: Steuert die Schritte 1-4. Jeder Klick erhöht den Zähler `E_CTU_0`. Der Demultiplexer leitet das Event dann an den korrekten Transitions-Eingang (`S1_S2`, `S2_S3`...).
*   **Taster `I3`**: Steuert analog die Schritte 5-8.

-----

## Funktionsweise

1.  Start mit `I1` -> Schritt 1 aktiv.
2.  Druck auf `I2` -> Zählerstand 1 -> Demux Ausgang 0 -> Event an `S1_S2` -> Wechsel zu Schritt 2.
3.  Druck auf `I2` -> Zählerstand 2 -> Demux Ausgang 1 -> Event an `S2_S3` -> Wechsel zu Schritt 3.
4.  ...

Dies simuliert eine Maschine, bei der der Bediener jeden Schritt manuell freigeben muss ("Schrittbetrieb").

-----

## Anwendungsbeispiel

**Inbetriebnahme oder Wartung**: Der Techniker schaltet die Maschine Schritt für Schritt weiter, um zu prüfen, ob jeder Teilprozess korrekt funktioniert, bevor er auf Automatik umschaltet.