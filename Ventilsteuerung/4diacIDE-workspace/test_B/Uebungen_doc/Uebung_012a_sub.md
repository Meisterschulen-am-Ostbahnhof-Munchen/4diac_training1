# Uebung_012a_sub: Persistenter Einstellwert (SubApp)

```{index} single: Uebung_012a_sub: Persistenter Einstellwert (SubApp)
```

[Uebung_012a_sub](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_012a_sub.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## 📺 Video

* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-04-06 19-43-11 Slurry Tanker und Subapps und Groups erklärt](https://www.youtube.com/watch?v=EYsZXyRwfps)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)

## Übersicht

[cite_start]Dieser Baustein dient als universelle Schnittstelle für Benutzereingaben, die dauerhaft im NVS (Non Volatile Storage) gespeichert werden sollen[cite: 1].
Er bündelt folgende Funktionen:
1.  **Eingabe**: Einlesen eines Werts vom Terminal (`NumericValue_ID`).
2.  **Speichern**: Automatisches Ablegen im Flash-Speicher unter einem wählbaren Schlüssel (`KEY`).
3.  **Laden**: Automatisches Auslesen des Werts beim Systemstart (`INITO -> GET`).
4.  **Rückmeldung**: Senden des (geladenen oder geänderten) Werts an die Anzeige am Terminal.
Zusätzlich bietet der Baustein einen Eingang `REQ`, um den Anzeige-Refresh extern (z.B. bei Terminal-Neuverbindung) anzustoßen.