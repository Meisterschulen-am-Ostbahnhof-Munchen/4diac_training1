# Uebung_090a1: Daten-Auswahl (Multiplexer)

```{index} single: Uebung_090a1: Daten-Auswahl (Multiplexer)
```

[Uebung_090a1](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_090a1.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_090a1`. Hier wird die Auswahl eines Datenwertes basierend auf einer Adresse demonstriert.


## 📺 Video

* [Zusätzlich: Uebung_083: Aufwärts/Abwärts zählen: E_CTUD_UDINT Datentyp UDINT; mit Anzeige am VT.](https://www.youtube.com/watch?v=oTPDtsw5eAw)
* ["Store Version" – Dein Schlüssel zur Verwaltung von Objektdatenpools im nichtflüchtigen VT-Speich...](https://www.youtube.com/watch?v=eVseHOOO9qM)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)

## Podcast
* [Datenkommunikation in der Automatisierung: Die Geheimnisse der IEC 61499 Datentypen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Datenkommunikation-in-der-Automatisierung-Die-Geheimnisse-der-IEC-61499-Datentypen-e3672lj)
* [Datentypen der IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Datentypen-der-IEC-61499-e3672jf)
* [IEC 61499: Revolution der Automatisierung – Ereignisgesteuerte Systeme und intelligente Datenflüsse entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/IEC-61499-Revolution-der-Automatisierung--Ereignisgesteuerte-Systeme-und-intelligente-Datenflsse-entschlsselt-e375ghe)
* [SINT, INT, DINT: Warum die Wahl des Datentyps über Effizienz und Fehler entscheidet](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/SINT--INT--DINT-Warum-die-Wahl-des-Datentyps-ber-Effizienz-und-Fehler-entscheidet-e3673b8)
* [Universum der Datentypen, wie sie in der IEC 61131-3 und IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Universum-der-Datentypen--wie-sie-in-der-IEC-61131-3-und-IEC-61499-e3673kb)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_090a1.png)


## Ziel der Übung

Verwendung des Bausteins `F_MUX_2` (Multiplexer). Es wird gezeigt, wie man zwischen zwei Signalquellen umschaltet, um einen gemeinsamen Ausgang zu bedienen.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_090a1.SUB` wird ein binärer Wahlschalter genutzt, um zwischen zwei Eingängen umzuschalten[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` & `I2` (Sources)**: Die Datenquellen.
  * **`I4` (Selector)**: Bestimmt, welche Quelle durchgeschaltet wird.
  * **`F_MUX_2`**: Der Multiplexer-Baustein.

-----

## Funktionsweise

*   Ist Taster **I4** nicht gedrückt (K=0) ➡️ Der Zustand von **I1** wird an den Ausgang `Q1` weitergereicht.
*   Ist Taster **I4** gedrückt (K=1) ➡️ Der Zustand von **I2** wird an den Ausgang `Q1` weitergereicht.

Dies ermöglicht das Umschalten von Bedien-Zuständigkeiten (z.B. zwischen Lokal- und Fernsteuerung).