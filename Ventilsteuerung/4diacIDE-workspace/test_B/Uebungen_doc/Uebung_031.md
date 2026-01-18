# Uebung_031: RGB-LED Strip (HSV-Steuerung)

```{index} single: Uebung_031: RGB-LED Strip (HSV-Steuerung)
```

[Uebung_031](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_031.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_031`. Hier steuern wir adressierbare RGB-LEDs (z.B. WS2812) über das komfortable HSV-Farbmodell an.


## Podcast
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
