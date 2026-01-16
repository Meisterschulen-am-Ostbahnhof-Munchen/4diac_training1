# Uebung_140: Betriebsstundenzähler (SYS_ONTIME)

[Uebung_140](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_140.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_140`. Hier wird die Erfassung der Systemlaufzeit demonstriert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_140.png)


## Ziel der Übung

Verwendung des Bausteins `SYS_ONTIME`. Ziel ist es, die kumulierte Zeit zu erfassen, in der die Steuerung eingeschaltet und aktiv ist.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_140.SUB` nutzt einen speziellen Messbaustein zur Zeitüberwachung[cite: 1].

### Funktionsbausteine (FBs)

  * **`SYS_ONTIME`**: Typ `logiBUS::signalprocessing::measurement::SYS_ONTIME`. [cite_start]Dieser Baustein misst die Zeit seit dem letzten Systemstart oder die kumulierte Gesamtzeit (je nach Implementierung)[cite: 1].

-----

## Funktionsweise

Der Baustein läuft im Hintergrund mit. Er bietet typischerweise Ausgänge für Sekunden, Minuten und Stunden. Diese Daten können dann dauerhaft gespeichert (NVS) oder auf dem Service-Menü des Terminals angezeigt werden.

-----

## Anwendungsbeispiel

**Wartungsintervalle**:
Die Steuerung zählt die Betriebsstunden der Maschine. Sobald ein Grenzwert (z.B. 500 Stunden) erreicht ist, wird dem Bediener am Terminal eine Meldung angezeigt: "Ölwechsel erforderlich". Dies garantiert die Einhaltung von Wartungsplänen und erhöht die Lebensdauer der Maschine.
