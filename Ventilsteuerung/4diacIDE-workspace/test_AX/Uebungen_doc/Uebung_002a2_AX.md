# Uebung_002a2_AX: UND-Verknüpfung mit Signalwandlung

```{index} single: Uebung_002a2_AX: UND-Verknüpfung mit Signalwandlung
```

[Uebung_002a2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_002a2_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_002a2_AX`. Hier wird gezeigt, wie Adapter-Signale in boolesche Werte gewandelt werden, um sie mit Standard-Logikbausteinen zu verarbeiten.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-03-30 16-59-57 Verknüpfung von Object ID und Objektname](https://www.youtube.com/watch?v=FuZTizT48JU)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_002a2_AX.png)


## Ziel der Übung

Das Hauptziel ist die Demonstration der Interoperabilität. Während spezialisierte Bausteine wie `AX_AND_2` direkt auf Adaptern arbeiten, benötigen viele Standard-Bibliotheken (wie die bitweisen Operatoren der IEC 61131) elementare Datentypen (BOOL). Diese Übung zeigt den Weg von der Hardware-Abstraktion zur klassischen Logik und zurück.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_002a2_AX.SUB` nutzt Konvertierungsbausteine, um zwei Eingangs-Adapter für ein UND-Gatter aufzubereiten[cite: 1].

### Funktionsbausteine (FBs)

  * **`AX_X_TO_BOOL_1` & `_2`**: Wandeln das Adapter-Signal (`Event + Data`) in ein explizites Ereignis `CNF` und einen booleschen Wert `IN` um.
  * **`F_AND`**: Ein klassisches bitweises UND-Gatter aus der IEC 61131 Bibliothek.
  * **`AX_BOOL_TO_X`**: Wandelt das Ergebnis der Logik wieder in ein Adapter-Signal um.
  * **`DigitalInput_I1` & `I2`**: Eingänge.
  * **`DigitalOutput_Q1`**: Ausgang.

-----

## Funktionsweise

1.  **Erfassung**: Die Adapter-Eingänge liefern bei jeder Änderung ein Signal.
2.  **Wandlung**: Die `TO_BOOL` Bausteine extrahieren den Zustand.
3.  **Verarbeitung**: Das `F_AND` Gatter prüft: Sind beide Eingänge `TRUE`?
4.  **Rückwandlung**: Das Ergebnis wird wieder in die Adapter-Struktur verpackt.
5.  **Ausgabe**: Der Ausgang `Q1` schaltet entsprechend.

Diese Methode ist zwar aufwendiger als die Nutzung von `AX_AND_2`, ermöglicht aber den Einsatz jeder beliebigen Logikbibliothek.

-----

## Anwendungsbeispiel

**Zustandsüberwachung mit Standard-FBs**: Wenn Sie komplexe mathematische oder logische Funktionen nutzen möchten, die nur für `BOOL` oder `INT` Datentypen existieren, ist diese Form der Wandlung der Standardweg.