# Uebung_010c_AX: Softkey Feedback (Visuell)

```{index} single: Uebung_010c_AX: Softkey Feedback (Visuell)
```

[Uebung_010c_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010c_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010c_AX`. Bisher haben die Tasten nur geschaltet. Jetzt sollen sie auch leuchten.


## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
* [ISO 11783-6: Softkeys und das Virtual Terminal verstehen – Dein Schlüssel zur Landmaschinen-Mechatronik](https://podcasters.spotify.com/pod/show/isobus-vt-objects/episodes/ISO-11783-6-Softkeys-und-das-Virtual-Terminal-verstehen--Dein-Schlssel-zur-Landmaschinen-Mechatronik-e36a8b0)
* [Das URI-Dreieck: Dein visueller Spickzettel für das Ohmsche Gesetz – Meistere die Elektrizität!](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Das-URI-Dreieck-Dein-visueller-Spickzettel-fr-das-Ohmsche-Gesetz--Meistere-die-Elektrizitt-e38dksp)
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010c_AX.png)


## Ziel der Übung

Rückmeldung an den Bediener (Farbumschlag).

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010c_AX.SUB` erweitert die einfache Softkey-Schaltung um einen Feedback-Baustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_F1`**: Eingabe.
  * **`DigitalOutput_Q1`**: Ausgabe (Lampe).
  * **`GreenWhiteBackground_AX`**: Eine SubApp aus der Bibliothek `MyLib::sys`. Diese steuert das Aussehen des Softkeys auf dem Terminal (Grün = Aktiv, Weiß = Inaktiv).
  * **`AX_SPLIT_2`**: Verteilt das Signal vom Softkey sowohl an den Ausgang `Q1` als auch an den Feedback-Baustein.

-----

## Funktionsweise

Wenn der Nutzer drückt, wird das Signal wahr.
1.  Der physische Ausgang geht an.
2.  Parallel dazu wird der Eingang `DI1` der Feedback-SubApp `TRUE`. Diese sendet ein ISOBUS-Kommando an das Terminal, um den Hintergrund des Softkeys `F1` auf Grün zu ändern.
3.  Beim Loslassen wird der Ausgang aus und der Softkey wieder Weiß.

Dies gibt dem Nutzer direktes visuelles Feedback auf dem Touchscreen.