# Uebung_019: Maskenumschaltung (Screen-Switch)

```{index} single: Uebung_019: Maskenumschaltung (Screen-Switch)
```

[Uebung_019](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_019.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_019`. Hier wird gezeigt, wie das Programm die aktive Anzeige (Data Mask) auf dem Terminal umschalten kann.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_019.png)


## Ziel der Übung

Verwendung des Bausteins `Q_ActiveMask` zur Navigation auf dem Terminal. Es wird demonstriert, wie physische Taster genutzt werden, um zwischen verschiedenen Bedien-Seiten zu blättern.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_019.SUB` nutzt zwei physische Taster, um zwischen zwei Arbeitsmasken zu wählen[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` & `I2`**: Physische Eingangs-Taster.
  * **`F_SEL_E_2`**: Ein Ereignis-Selektor. Er hat zwei `REQ`-Eingänge und gibt beim jeweiligen Trigger die zugeordnete Konstante am Datenausgang aus.
  * **`Q_ActiveMask`**: Der ISOBUS-Ausgangsbaustein. [cite_start]Er sendet den Befehl zum Wechseln der Maske an das Terminal[cite: 1].

-----

## Funktionsweise

*   Druck auf **Taster 1** ➡️ `F_SEL_E_2` liefert die ID von `DataMask_M1` ➡️ `Q_ActiveMask` schaltet das Terminal auf Seite 1.
*   Druck auf **Taster 2** ➡️ `F_SEL_E_2` liefert die ID von `DataMask_M2` ➡️ `Q_ActiveMask` schaltet das Terminal auf Seite 2.

Das System steuert hier also aktiv, was der Bediener sieht.

-----

## Anwendungsbeispiel

**Kontextabhängige Steuerung**:
Wenn der Fahrer am physischen Bedienpult den Schalter für "Pflugbetrieb" umlegt, wechselt das Terminal automatisch von der Straßenansicht zur Feldansicht mit allen relevanten Tiefeneinstellungen. Dies erspart dem Fahrer das manuelle Suchen der richtigen Seite am Touchscreen während der Fahrt.
