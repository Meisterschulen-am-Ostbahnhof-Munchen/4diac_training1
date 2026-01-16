# Uebung_130: Custom PGN empfangen (Peer-to-Peer)

[Uebung_130](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_130.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_130`. Hier wird das Gegenstück zum Senden gezeigt: Das gezielte Empfangen von herstellerspezifischen Nachrichten.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_130.png)


## Ziel der Übung

Verwendung des Bausteins `AlPgnRxNew8B`. Es wird demonstriert, wie man auf eine spezifische Nachricht (PGN) eines bestimmten Partners lauscht und den Inhalt für das eigene Programm auswertet.

-----

## Beschreibung und Komponenten

[cite_start]In `Uebung_130.SUB` wird ein Empfangs-Filter für eine herstellerspezifische PGN konfiguriert[cite: 1].

### Funktionsbausteine (FBs)

  * **`NmGetCfInfo_1`**: Identifiziert den Absender der Nachricht (Source).
  * **`AlPgnRxNew8B`**: Der Empfangs-Baustein. Er filtert alle CAN-Nachrichten und lässt nur die passende PGN durch.
  * **`STRUCT_DEMUX`**: Zerlegt die empfangene 8-Byte Nachricht wieder in einzelne Signale.

-----

## Funktionsweise

1.  Der Baustein wird über `install` im System registriert und mit dem gewünschten Absender (`NmSource`) verknüpft.
2.  Sobald der Partner die passende Nachricht (PGN `61184`) sendet, erkennt dies der Baustein.
3.  Er feuert das Ereignis `IND` (Indication) ab und stellt das Datenpaket am Port `Data` bereit.
4.  Über den Demultiplexer kann das Programm nun auf den Inhalt der Nachricht reagieren.

Dies ermöglicht eine private Kommunikation zwischen zwei spezifischen Geräten am Bus, ohne andere Teilnehmer zu stören.
