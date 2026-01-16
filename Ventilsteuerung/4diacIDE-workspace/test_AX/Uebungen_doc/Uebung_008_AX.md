# Uebung_008_AX: Autonomer Blinker-Baustein

[Uebung_008_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_008_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_008_AX`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_008_AX.png)


## Ziel der Übung

Implementierung eines dauerhaft laufenden Blinkers als Basis-Baustein.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_008_AX.SUB` ist eine Variante von `Uebung_007a3_AX`, jedoch ohne externe Start/Stop-Eingänge[cite: 1].

Der `E_CYCLE` läuft dauerhaft (oder wird einmalig initialisiert). Die Logik mit `E_SWITCH` und `AX_SR` sorgt für das Toggeln. Da keine externen Eingriffe vorgesehen sind, blinkt dieser Ausgang permanent, solange die Steuerung läuft.

-----

## Anwendungsbeispiel

**Lebenszeichen (Heartbeat)**: Eine LED, die auf der Platine oder am Schaltschrank blinkt, um anzuzeigen: "Die CPU lebt noch und das Programm läuft".
