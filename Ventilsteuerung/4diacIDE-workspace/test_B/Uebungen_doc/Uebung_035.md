# Uebung_035: Schrittketten-Steuerung (4 Phasen)

```{index} single: Uebung_035: Schrittketten-Steuerung (4 Phasen)
```

[Uebung_035](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_035.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_035`. Hier wird die Steuerung von komplexen Abläufen mittels eines Sequenzers (Schrittkette) demonstriert.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [Eclipse 4diac FORTE: IEC 61499 verstehen – Der LEGO®-Baukasten für Ihre Industrie 4.0 Steuerung](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-FORTE-IEC-61499-verstehen--Der-LEGO-Baukasten-fr-Ihre-Industrie-4-0-Steuerung-e3682kc)
* [Eclipse 4diac: Open Source als Game Changer für industrielle Steuerungen?](https://podcasters.spotify.com/pod/show/eclipse-4diac-de/episodes/Eclipse-4diac-Open-Source-als-Game-Changer-fr-industrielle-Steuerungen-e372eru)
* [DIN EN 61499-1 Entschlüsselt: Der Bauplan für modulare, verteilte Steuerungssysteme](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Entschlsselt-Der-Bauplan-fr-modulare--verteilte-Steuerungssysteme-e367nmj)
* [DIN EN 61499-1: Die Lego-Steine für flexible und ereignisgesteuerte Industriesteuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Die-Lego-Steine-fr-flexible-und-ereignisgesteuerte-Industriesteuerungen-e3681o1)
* [DIN EN 61499-1: Revolution in der Steuerungstechnik – Modulare, ereignisgesteuerte Systeme verstehen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/DIN-EN-61499-1-Revolution-in-der-Steuerungstechnik--Modulare--ereignisgesteuerte-Systeme-verstehen-e367nse)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_035.png)


## Ziel der Übung

Verwendung des Bausteins `sequence_ET_04`. Es wird gezeigt, wie ein Prozess in vier Phasen (`S1` bis `S4`) unterteilt wird, wobei die Übergänge sowohl durch Ereignisse (Events) als auch durch Zeit (Timer) ausgelöst werden können.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_035.SUB` steuert 4 Ausgänge in einer festen Reihenfolge[cite: 1].

### Funktionsbausteine (FBs)

  * **`sequence_04`**: Der Sequenzer-Baustein. Er verwaltet die Logik der Schritte.
  * **Parameter `DT_S1_S2` etc.**: Definieren die maximale Verweildauer in einem Schritt (hier jeweils 2 Sekunden).
  * **`Q_NumericValue`**: Zeigt den aktuellen Schritt (1-4) auf dem Terminal an.
  * **`E_TimeOut`**: Überwacht den Ablauf.

-----

## Funktionsweise

1.  **Start**: Taster **I1** triggert `START_S1`. Lampe `Q1` geht an.
2.  **Übergang**: Nach 2 Sekunden (oder durch ein Event am entsprechenden Port) springt der Sequenzer zu Schritt 2. `Q1` geht aus, `Q2` geht an.
3.  **Fortsetzung**: Der Prozess läuft bis Schritt 4 durch.
4.  **Reset**: Taster **I4** kann den Ablauf jederzeit abbrechen und alle Ausgänge deaktivieren.

-----

## Anwendungsbeispiel

**Automatischer Reinigungszyklus**:
Ein Knopfdruck startet das Programm: 1. Ventile spülen (2s), 2. Reinigungsmittel einlassen (2s), 3. Einwirken (2s), 4. Klarspülen (2s). Die Schrittkette garantiert, dass die Phasen exakt nacheinander und niemals gleichzeitig ablaufen.