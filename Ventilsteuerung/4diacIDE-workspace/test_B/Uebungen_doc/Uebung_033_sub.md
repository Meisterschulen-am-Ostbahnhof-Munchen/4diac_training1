# Uebung_033_sub: Modularer RGB-Kanal (SubApp)

```{index} single: Uebung_033_sub: Modularer RGB-Kanal (SubApp)
```

[Uebung_033_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_033_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt den Sub-App-Typ `Uebung_033_sub`. Er dient als wiederverwendbares Modul zur Steuerung von farbigen LED-Anzeigen.

----

## Übersicht

[cite_start]Dieser Baustein bündelt einen digitalen Eingangsbaustein (`IX`) und einen spezialisierten RGB-Streifen-Ausgang (`logiBUS_LED_strip_QX`)[cite: 1].
Er stellt Parameter für die Wahl des Eingangs-Buttons (`Input`), der Farbe (`Colour`) und des Ausgangs-Kanals (`Output`) bereit. Intern ist er auf eine feste Blinkfrequenz von 1 Hz voreingestellt. Durch die Kapselung dieser komplexen Treiber-Logik können farbige Status-Anzeigen in Projekten sehr einfach durch Parametrierung statt durch aufwendige Einzelverdrahtung realisiert werden.