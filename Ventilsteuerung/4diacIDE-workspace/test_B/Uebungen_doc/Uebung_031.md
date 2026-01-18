# Uebung_031: RGB-LED Strip (HSV-Steuerung)

```{index} single: Uebung_031: RGB-LED Strip (HSV-Steuerung)
```

[Uebung_031](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_031.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_031`. Hier steuern wir adressierbare RGB-LEDs (z.B. WS2812) über das komfortable HSV-Farbmodell an.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Eclipse 4diac FORTE: IEC 61499 verstehen – Der LEGO®-Baukasten für Ihre Industrie 4.0 Steuerung](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-FORTE-IEC-61499-verstehen--Der-LEGO-Baukasten-fr-Ihre-Industrie-4-0-Steuerung-e3682kc)
* [Eclipse 4diac: Open Source als Game Changer für industrielle Steuerungen?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Open-Source-als-Game-Changer-fr-industrielle-Steuerungen-e372eru)
* [DIN EN 61499-1 Entschlüsselt: Der Bauplan für modulare, verteilte Steuerungssysteme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entschlsselt-Der-Bauplan-fr-modulare--verteilte-Steuerungssysteme-e367nmj)
* [DIN EN 61499-1: Die Lego-Steine für flexible und ereignisgesteuerte Industriesteuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Die-Lego-Steine-fr-flexible-und-ereignisgesteuerte-Industriesteuerungen-e3681o1)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_031.png)


## Ziel der Übung

Verwendung der RGB-Bibliothek für den ESP32. Es wird demonstriert, wie man Farben nicht über Rot-Grün-Blau-Werte (RGB), sondern über Farbwert (Hue), Sättigung (Saturation) und Helligkeit (Value) definiert und an einen LED-Streifen sendet.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_031.SUB` nutzt einen Konvertierungsbaustein und einen Streifen-Treiber[cite: 1].

### Funktionsbausteine (FBs)

  * **`hsv2rgb`**: Rechnet die intuitiven HSV-Werte in die von der Hardware benötigten RGB-Werte um.
  * **`strip_set_pixel`**: Überträgt die Farbwerte an eine spezifische LED im Streifen.
  * **`I1` (Set)**: Klick löst das Setzen der Farbe aus.
  * **`I2` (Clear)**: Klick löscht die Anzeige (LED aus).

-----

## Funktionsweise

1.  Der Nutzer klickt auf **I1**. Das Event triggert die Konvertierung.
2.  Der `hsv2rgb` Baustein nimmt die voreingestellten Werte (z.B. Hue=100) und liefert die Anteile für Rot, Grün und Blau.
3.  Das `CNF`-Event des Konverters startet den Hardware-Transfer über `strip_set_pixel`.
4.  Die erste LED am Streifen leuchtet in der gewählten Farbe.

-----

## Anwendungsbeispiel

**Individuelle Design-Beleuchtung**:
In einer Kabine soll die Ambiente-Beleuchtung einstellbar sein. Über ein Drehrad (Poti) wird der `Hue`-Wert verändert. Das Programm rechnet dies permanent um, sodass der Fahrer stufenlos durch den gesamten Regenbogen navigieren kann.