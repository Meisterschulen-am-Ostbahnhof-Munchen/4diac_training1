# Uebung_020f2_AX: FB_TP mit Takteingang

[Uebung_020f2_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_020f2_AX.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/041f4df4-b729-484d-b786-b6dcdf151961)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_020f2_AX`. Hier wird der klassische Funktionsbaustein-Timer `FB_TP` verwendet, der eine regelmäßige Triggerung (Takt) benötigt.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/logiBUS-verstehen-Direkte-Signalweiterleitung--Das-Hallo-Welt-der-Automatisierung-e36vlfg/a-ac3vagq" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----

![](Uebung_020f2_AX.png)


## Ziel der Übung

Das Ziel ist es, die Brücke zwischen der klassischen SPS-Programmierung (zyklisch) und der IEC 61499 (ereignisbasiert) zu schlagen. Da ein `FB_TP` intern die Zeit zählt, muss sein `REQ`-Eingang regelmäßig mit Ereignissen versorgt werden, solange der Timer läuft.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_020f2_AX.SUB` nutzt einen `E_CYCLE` Baustein, um den Takt für den Timer zu generieren[cite: 1].

### Funktionsbausteine (FBs)

  * **`AX_X_TO_BOOL` & `AX_BOOL_TO_X`**: Wandeln zwischen der Adapter-Welt (AX) und der booleschen Welt der klassischen Timer um.
  * **`FB_TP`**: [cite_start]Der eigentliche Impuls-Timer. Er reagiert auf die steigende Flanke am Eingang `IN` und hält den Ausgang `Q` für die Zeit `PT` auf TRUE[cite: 1].
  * **`E_CYCLE`**: [cite_start]Erzeugt alle 500ms ein Ereignis, um den Timer zu aktualisieren[cite: 1].
  * **`AX_SWITCH_Q1`**: Überwacht das Ende des Impulses, um den Taktgeber wieder auszuschalten.

-----

## Funktionsweise

1.  **Start**: Beim Drücken des Tasters wird `AX_X_TO_BOOL.IN` wahr. Das dabei entstehende Ereignis `CNF` startet den `E_CYCLE`.
2.  **Taktung**: Der `E_CYCLE` sendet alle 500ms ein Event an `FB_TP.REQ`. Bei jedem Event prüft der Timer, wie viel Zeit vergangen ist und aktualisiert seinen Ausgang `Q`.
3.  **Impuls**: Solange der Impuls läuft, bleibt `Q` wahr und steuert über `AX_BOOL_TO_X` den Ausgang `Q1` an.
4.  **Stopp**: Sobald die 5 Sekunden abgelaufen sind, geht `FB_TP.Q` auf FALSE. Die Weiche `AX_SWITCH_Q1` erkennt diese fallende Flanke (`EO0`) und stoppt den `E_CYCLE`.

Dieses Beispiel zeigt, dass klassische Bausteine zwar verwendet werden können, aber einen höheren Aufwand für die Ereignisverwaltung erfordern als spezialisierte Adapter-Bausteine (wie `AX_TP`).

-----

## Anwendungsbeispiel

**Integration von Legacy-Code**: Wenn bereits fertige Bausteine aus der "alten" SPS-Welt übernommen werden sollen, die auf zyklische Abarbeitung angewiesen sind, ist dieses Takt-Muster unerlässlich.
