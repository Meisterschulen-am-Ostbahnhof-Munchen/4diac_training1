# Uebung_039: Hydraulik-Ventilsteuerung

```{index} single: Uebung_039: Hydraulik-Ventilsteuerung
```

[Uebung_039](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_039.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_039`. Diese Übung ist speziell auf die Ansteuerung von hydraulischen oder pneumatischen Wegeventilen zugeschnitten.

## 📺 Video

* [2025-08-17 14-39-09 logiBUS® Umwandeln eines Projektes mit Mapping in eines ohne Mapping.](https://www.youtube.com/watch?v=w8nTLn8fQxQ)
* [Schulungsvideo logiBUS® CAN - SAE J1939 Kommunikation](https://www.youtube.com/watch?v=lA8lygx9598)

----

![](Uebung_039.png)

## Ziel der Übung

Realisierung einer komplexen Spiegelabfolge. Im Gegensatz zu einfachen Zylindern müssen bei Wegeventilen oft Zustände gehalten werden (Mittelstellung gesperrt), was eine präzise zeitliche und ereignisbasierte Steuerung der Spulen erfordert.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_039.SUB` nutzt einen 5-Schritt-Sequenzer (`sequence_ET_05`)[cite: 1].
Die Ansteuerung der Hardware erfolgt hier über typisierte Sub-Applikationen (`Uebung_039_sub_Outputs`), die den jeweiligen Ventilzustand auch visuell auf dem ISOBUS-Terminal durch Farbumschlag der zugehörigen Softkeys rückmelden.

-----

## Funktionsweise

Die Kette wird manuell durch physische Taster (`I1` bis `I4`) gesteuert, wobei ein zentraler Zeitschritt (5s bei `DT_S3_S4`) eine automatische Sicherheits- oder Wartephase einfügt. Dies zeigt die Kombination aus freier Bedienbarkeit und erzwungenen Prozesszeiten.