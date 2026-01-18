# Uebung_012b: Speichern in INI-Dateien

```{index} single: Uebung_012b: Speichern in INI-Dateien
```

[Uebung_012b](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_012b.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_012b`. Hier wird eine alternative Methode zur Speicherung von Daten vorgestellt: Die Verwendung von INI-Dateien.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_012b.png)


## Ziel der Übung

Verwendung des `INI` Bausteins zur strukturierten Datenspeicherung. Im Gegensatz zum einfachen NVS-Key-Value-Speicher erlaubt das INI-Format eine Gliederung in Sektionen und Schlüssel, was bei großen Datenmengen übersichtlicher ist.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_012b.SUB` nutzt einen INI-Speicher-Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`INI`**: Typ `eclipse4diac::storage::INI`. [cite_start]Dieser Baustein speichert Werte in einer dateibasierten Struktur ab[cite: 1]. Er benötigt zusätzlich zum `KEY` eine `SECTION`.
  * **Parameter**:
    * `SECTION`: "SECTION_I1_STORE"
    * `KEY`: "KEY_I1_STORE"
    * `DEFAULT_VALUE`: 55 (wird geladen, falls noch keine Datei existiert).

-----

## Funktionsweise

Die Logik entspricht ansonsten der Übung 012:
1.  **Schreiben**: `InputNumber -> REQ -> INI.SET`.
2.  **Lesen**: `INITO -> INI.GET -> Q_NumericValue`.
3.  **Refresh**: `CbVtStatus -> Q_NumericValue`.

INI-Dateien sind besonders nützlich, wenn Parameter extern (z.B. über einen PC oder Web-Interface) ausgelesen oder editiert werden sollen, da sie in einem für Menschen lesbaren Textformat vorliegen.