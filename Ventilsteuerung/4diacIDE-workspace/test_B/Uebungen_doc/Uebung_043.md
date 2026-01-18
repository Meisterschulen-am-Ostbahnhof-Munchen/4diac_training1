# Uebung_043: Skalierung mit Grenzwerten (SCALE_LIM)

```{index} single: Uebung_043: Skalierung mit Grenzwerten (SCALE_LIM)
```

[Uebung_043](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_043.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_043`. Dies ist eine Erweiterung der Skalierung um Sicherheitsgrenzen.

## 📺 Video

* [2025-02-21 13-04-43 aktueller Stand logiBUS® Eclipse 4diac™ IDE](https://www.youtube.com/watch?v=OMNP9p12mAw)
* [2025-02-23 11-43-44 Fusion 360 Übersicht Tutorials](https://www.youtube.com/watch?v=djM9ndIfp-0)
* [2025-03-11 16-53-43 Watch über App, nicht über Ressource](https://www.youtube.com/watch?v=bGwFMVQBj3k)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)

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