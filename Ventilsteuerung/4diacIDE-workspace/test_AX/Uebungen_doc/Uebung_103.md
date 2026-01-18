# Uebung_103: Modus-Selektion (Multiplexer/Demultiplexer)

```{index} single: Uebung_103: Modus-Selektion (Multiplexer/Demultiplexer)
```

[Uebung_103](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_103.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_103`. Dies ist ein komplexes Beispiel, das zeigt, wie man den Signalpfad eines Tasters zur Laufzeit umschalten kann.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_103.png)


## Ziel der Übung

Dynamische Auswahl zwischen verschiedenen Verarbeitungslogiken (Tastend, Rastend, Verzögert) für denselben physikalischen Ein- und Ausgang.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_103.SUB` nutzt ein ISOBUS-Zahlenfeld, um zwischen drei Logik-Zweigen zu wählen[cite: 1].

### Funktionsbausteine (FBs)

  * **`InputNumber_I1`**: Ein Eingabefeld auf dem ISOBUS-Terminal. Der Nutzer gibt hier 1, 2 oder 3 ein.
  * **`AX_DEMUX_3`**: Verteilt das Signal vom Taster `I1` auf einen von drei Ausgängen.
  * **`AX_MUX_3`**: Sammelt das Ergebnis der drei Zweige wieder ein und gibt es an `Q1` weiter.
  * **Die drei Zweige**:
    1.  `tastend`: Direkte Weiterleitung (1:1).
    2.  `rastend`: Wandelt den Taster in einen Schalter (Toggle) um.
    3.  `tastend_TON_5s`: Leitet das Signal mit einer Einschaltverzögerung von 5s weiter.

-----

## Funktionsweise

1.  Der Nutzer gibt am Terminal den gewünschten Modus ein (z.B. "2" für Rastend).
2.  Die Zahl wird konvertiert und an die Selektoren (`K`) von MUX und DEMUX gesendet.
3.  Betätigt der Nutzer nun den physischen Taster `I1`, wird das Signal durch den `DEMUX` in den Zweig `rastend` geleitet.
4.  Dort wird es verarbeitet und vom `MUX` wieder auf den Ausgang `Q1` geführt.

Ändert der Nutzer die Zahl auf "1", verhält sich derselbe Taster plötzlich rein tastend.

-----

## Anwendungsbeispiel

**Multifunktions-Bedienelement**: Ein Joystick-Taster kann je nach gewählter Geräteeinstellung (Modus) eine andere Funktion haben oder ein anderes Zeitverhalten aufweisen.