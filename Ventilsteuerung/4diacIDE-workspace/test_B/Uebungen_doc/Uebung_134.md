# Uebung_134: Empfang von unbekannten Partnern

```{index} single: Uebung_134: Empfang von unbekannten Partnern
```

[Uebung_134](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_134.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_134`.


## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_134.png)


## Übersicht

[cite_start]In dieser Übung wird eine Lösung für die Kommunikation mit Geräten gezeigt, die kein standardkonformes ISOBUS-Management (Address Claiming) durchführen[cite: 1].
Unter Verwendung des Bausteins `BaseMemberExternAdd` wird manuell ein Kommunikations-Handle für eine feste Quelladresse (hier `u8SA = 55`) erstellt. Dieses Handle wird genutzt, um Nachrichten von einem "Unclaimed Partner" zu empfangen, der seine Identität nicht über die Namensverwaltung preisgibt. Dies ist oft bei der Integration von einfachen Sensoren oder Altgeräten notwendig.