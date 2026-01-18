# Uebung_008: Autonomer Blinker-Baustein

```{index} single: Uebung_008: Autonomer Blinker-Baustein
```

[Uebung_008](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_008.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_008`. Hier wird die Logik eines dauerhaft laufenden Taktgebers mit internem Speicherzustand gezeigt.


## 📺 Video

* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)
* [Aufwärts/Abwärts zählen Baustein E_CTUD aus der IEC 61499 (Übung 82)](https://www.youtube.com/watch?v=H_MRtaMiaU8)
* [Herunterzählen Baustein E_CTD aus der IEC 61499 (Übung 81)](https://www.youtube.com/watch?v=NgLWcVhgRqk)
* [RS-Flip-Flop Baustein E_RS aus der IEC 61499 (Übung 006b)](https://www.youtube.com/watch?v=GXOe8K7Jgr0)
* [SR-Flip-Flop Baustein E_SR aus der IEC 61499 (Übung 006)](https://www.youtube.com/watch?v=6nGmGX7gwAE)

## Podcast
* [Der E_CTU-Baustein: Ereignisgesteuertes Hochzählen in der Industrie nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_CTU-Baustein-Ereignisgesteuertes-Hochzhlen-in-der-Industrie-nach-IEC-61499-e36846t)
* [Der E_PERMIT-Baustein: Der "Türsteher" für Ereignisse in IEC 61499-Systemen entschlüsselt](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_PERMIT-Baustein-Der-Trsteher-fr-Ereignisse-in-IEC-61499-Systemen-entschlsselt-e3681m5)
* [Der E_T_FF_SR-Baustein: Herzstück der IEC 61499 – Speichern, Umschalten, Reagieren](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Der-E_T_FF_SR-Baustein-Herzstck-der-IEC-61499--Speichern--Umschalten--Reagieren-e3682dm)
* [DIN EN 61499-1 Entmystifiziert: Funktionsbausteine, Objektorientierung und verteilte Systeme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entmystifiziert-Funktionsbausteine--Objektorientierung-und-verteilte-Systeme-e37229b)
* [DIN EN 61499-1: Bauklötze für die Industrie 4.0 – So revolutionieren Funktionsbausteine die Automatisierung](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Baukltze-fr-die-Industrie-4-0--So-revolutionieren-Funktionsbausteine-die-Automatisierung-e3681j7)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_008.png)


## Ziel der Übung

Implementierung eines autarken Blink-Schaltkreises.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_008.SUB` nutzt die Kombination aus `E_CYCLE`, `E_SWITCH` und `E_SR` ohne externe Steuereingänge[cite: 1].

Der Taktgeber `E_CYCLE` läuft (nach einmaliger Initialisierung durch das System) permanent durch. Die Logik sorgt dafür, dass der Ausgang `Q1` im Sekundentakt zwischen `TRUE` und `FALSE` wechselt. Da keine Stopp-Logik vorhanden ist, dient dieser Aufbau als permanenter Herzschlag des Programms.

-----

## Anwendungsbeispiel

**Status-LED (Heartbeat)**:
Eine LED direkt auf der CPU-Platine, die ständig blinkt, solange die Versorgungsspannung anliegt und das Steuerungsprogramm ("Task") fehlerfrei abgearbeitet wird. Hört die LED auf zu blinken, weiß der Techniker sofort, dass die Steuerung abgestürzt ist oder im Stopp-Zustand verharrt.