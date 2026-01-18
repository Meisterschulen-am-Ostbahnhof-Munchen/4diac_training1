# Uebung_006d: Schutz vor versehentlichem Einschalten

```{index} single: Uebung_006d: Schutz vor versehentlichem Einschalten
```

[Uebung_006d](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_006d.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_006d`. Hier wird eine asymmetrische Bedienlogik zum Schutz der Anlage implementiert.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Das Relais im Detail: Schaltverstärker, Schutz und die Geheimnisse von A1/A2, 85/86 und der Hysterese](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-Relais-im-Detail-Schaltverstrker--Schutz-und-die-Geheimnisse-von-A1A2--8586-und-der-Hysterese-e3audsc)
* [Schutzbeschaltung: Varianten und Grundlagen der Spannungsbegrenzung](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Schutzbeschaltung-Varianten-und-Grundlagen-der-Spannungsbegrenzung-e368jq3)
* [Verpolungsschutz in der Elektronik: Warum die ideale Diode (LM74700) MOSFETs und Schottky-Dioden in Effizienz und Kosten schlägt](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Verpolungsschutz-in-der-Elektronik-Warum-die-ideale-Diode-LM74700-MOSFETs-und-Schottky-Dioden-in-Effizienz-und-Kosten-schlgt-e3a2487)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_006d.png)


## Ziel der Übung

Kombination von komplexen Eingangsereignissen (Doppelklick) mit Speicherbausteinen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_006d.SUB` realisiert eine Ein/Aus-Logik mit unterschiedlichen Hürden[cite: 1].

### Funktionsbausteine (FBs)

  * **`I1` (Set)**: Konfiguriert auf `BUTTON_DOUBLE_CLICK`.
  * **`I2` (Reset)**: Konfiguriert auf `BUTTON_SINGLE_CLICK`.
  * **`E_SR`**: Der Speicherbaustein.

-----

## Funktionsweise

*   **Einschalten**: Erfordert eine bewusste Handlung des Nutzers (Doppelklick auf `I1`). Ein einfaches Berühren reicht nicht aus.
*   **Ausschalten**: Muss im Bedarfsfall schnell und einfach gehen (einfacher Klick auf `I2`).

Das Flip-Flop speichert den Zustand zwischen diesen Ereignissen.

-----

## Anwendungsbeispiel

**Sicherheitsrelevante Hilfsantriebe**:
Eine hydraulische Pumpe oder ein Schneidwerk soll nicht durch ein versehentliches Anstoßen des Schalters in der Kabine starten. Der Nutzer muss durch den Doppelklick seine Absicht bestätigen. Das sofortige Ausschalten bei Gefahr muss jedoch durch einen einfachen Schlag auf den Aus-Taster gewährleistet sein.