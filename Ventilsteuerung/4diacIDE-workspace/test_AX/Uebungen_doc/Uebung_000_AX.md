# Uebung_000_AX: Einfache Addition

```{index} single: Uebung_000_AX: Einfache Addition
```

[Uebung_000_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_000_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_000_AX`, das absolute Basisbeispiel für Berechnungen.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [logiBUS®: Revolutioniert die Agrarmechatronik – ISOBUS einfacher, offener, smarter](https://podcasters.spotify.com/pod/show/logibus/episodes/logiBUS-Revolutioniert-die-Agrarmechatronik--ISOBUS-einfacher--offener--smarter-e38b4kp)
* [Schalterlogik verstehen: So funktioniert ein Toggle Flip-Flop mit logiBUS® – einfache Steuerung in der Landtechnik](https://podcasters.spotify.com/pod/show/logibus/episodes/Schalterlogik-verstehen-So-funktioniert-ein-Toggle-Flip-Flop-mit-logiBUS--einfache-Steuerung-in-der-Landtechnik-e36vjo1)
* [Amazon Pizza-Regel bis IKEA-Effekt: 12 verblüffend einfache Ideen hinter riesigem Geschäftserfolg](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Amazon-Pizza-Regel-bis-IKEA-Effekt-12-verblffend-einfache-Ideen-hinter-riesigem-Geschftserfolg-e39kmmc)
* [Bulldog Legende: Wie der einfache LANZ-Traktor die Landwirtschaft revolutionierte und zum Duden-Eint](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Bulldog-Legende-Wie-der-einfache-LANZ-Traktor-die-Landwirtschaft-revolutionierte-und-zum-Duden-Eint-e39kif6)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_000_AX.png)


## Ziel der Übung

Das Ziel ist die Platzierung und Parametrierung eines Standard-Bausteins der IEC 61131-Bibliothek innerhalb eines IEC 61499 Netzwerks.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_000_AX.SUB` enthält lediglich einen Rechenbaustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`ADD_2`**: Typ `iec61131::arithmetic::ADD_2`. [cite_start]Addiert zwei Ganzzahlen (`IN1` und `IN2`)[cite: 1].

-----

## Funktionsweise

Der Baustein ist fest mit den Werten 5 und 3 beschaltet. Das Ergebnis (8) liegt am Ausgang `OUT` an. Da es sich um einen reinen Datenbaustein ohne Event-Eingang handelt (Simple FB), wird das Ergebnis berechnet, sobald sich die Eingangsdaten ändern.

-----

## Anwendungsbeispiel

Grundlage für jede Form von **Zählern, Offsets oder Skalierungen** in einer Steuerung.