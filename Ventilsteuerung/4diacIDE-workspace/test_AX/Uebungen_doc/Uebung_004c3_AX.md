# Uebung_004c3_AX: Langer Tastendruck (Loslassen)

[Uebung_004c3_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_004c3_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_004c3_AX`.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_004c3_AX.png)


## Ziel der Übung

Nutzung des Ereignisses `BUTTON_LONG_PRESS_UP`.

-----

## Funktionsweise

[cite_start]Der Baustein `DigitalInput_CLK_I1` in `Uebung_004c3_AX.SUB` ist auf `BUTTON_LONG_PRESS_UP` konfiguriert[cite: 1].

Das Event wird gefeuert, wenn der Taster losgelassen wird, *nachdem* er als "lang gedrückt" erkannt wurde. Ein kurzes Tippen löst dieses Event nicht aus (das wäre `SINGLE_CLICK`).

-----

## Anwendungsbeispiel

**Dimm-Vorgang beenden**: Wenn der Benutzer den Taster loslässt, soll das Dimmen stoppen und der aktuelle Helligkeitswert gespeichert werden.
