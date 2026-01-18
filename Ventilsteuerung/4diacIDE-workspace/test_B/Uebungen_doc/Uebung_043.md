# Uebung_043: Skalierung mit Grenzwerten (SCALE_LIM)

```{index} single: Uebung_043: Skalierung mit Grenzwerten (SCALE_LIM)
```

[Uebung_043](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_043.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_043`. Dies ist eine Erweiterung der Skalierung um Sicherheitsgrenzen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [ISOBUS Skalierung: Wenn der Ackerschlepper-Bildschirm nicht passt – Eine Einführung in ISO 11783-6](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISOBUS-Skalierung-Wenn-der-Ackerschlepper-Bildschirm-nicht-passt--Eine-Einfhrung-in-ISO-11783-6-e36a8q6)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_043.png)


## Ziel der Übung

Verwendung des Bausteins `SCALE_LIM`. Im Gegensatz zum einfachen `SCALE` bietet dieser Baustein zusätzliche Parameter, um das Ergebnis nach oben und unten zu begrenzen (Limiting), selbst wenn der Eingangswert den definierten Bereich verlässt.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_043.SUB` wird ein hochkomplexer Skalierungs-Szenario mit fixen Grenzen aufgebaut[cite: 1].

### Funktionsbausteine (FBs)

  * **`SCALE_LIM`**: Skalierung mit Sättigung.
  * **Parameter**:
    * `MIN_IN_LIM` / `MAX_IN_LIM`: Definieren den Bereich, in dem der Eingangswert "gültig" ist.
    * `MIN_OUT_FIX` / `MAX_OUT_FIX`: Harte Grenzwerte für den Ausgang. Egal was berechnet wird, der Ausgang wird diese Werte niemals unter- oder überschreiten.

-----

## Anwendungsbeispiel

**Überlaufschutz bei der Ventilsteuerung**:
Ein Regler berechnet die Öffnung eines Ventils basierend auf der Temperatur. Auch wenn der Regler aufgrund einer extremen Störung "150%" anfordert, sorgt `SCALE_LIM` dafür, dass der reale Ausgangswert bei 100% gekappt wird, um die Hardware nicht zu beschädigen. Ebenso kann eine Mindestöffnung (z.B. 5% zur Kühlung) fest als Untergrenze hinterlegt werden.