# Uebung_013: Softkey SR-Flip-Flop (Speicher)

[Uebung_013](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_013.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_013`. Hier wird eine Speicherfunktion realisiert, die vollständig über das ISOBUS-Terminal bedient wird.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_013.png)


## Ziel der Übung

Realisierung einer Ein/Aus-Schaltung mit getrennten virtuellen Tasten.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_013.SUB` nutzt zwei Softkeys zur Steuerung eines SR-Flip-Flops[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_UP_F1`**: Triggert beim Loslassen (Release) den Set-Eingang (`S`).
  * **`SoftKey_UP_F2`**: Triggert beim Loslassen (Release) den Reset-Eingang (`R`).
  * **`E_SR`**: Der Speicherbaustein.
  * **`DigitalOutput_Q1`**: Der Hardware-Ausgang.

-----

## Funktionsweise

*   Ein Klick auf **F1** schaltet die Funktion ein.
*   Ein Klick auf **F2** schaltet die Funktion aus.

Die Verwendung von `SK_RELEASED` sorgt für ein stabiles Bediengefühl am Touchscreen. Da zwei getrennte Tasten verwendet werden, ist der Zustand der Anlage für den Bediener immer eindeutig steuerbar.

-----

## Anwendungsbeispiel

**Zuschalten eines Anbaugeräts**:
Am Terminal gibt es zwei deutliche Symbole: Ein grüner Haken (`F1`) für "System Aktiv" und ein rotes Kreuz (`F2`) für "System Deaktiviert". Der Speicher in der Steuerung sorgt dafür, dass die gewählte Betriebsart erhalten bleibt, bis die jeweils andere Taste gedrückt wird.
