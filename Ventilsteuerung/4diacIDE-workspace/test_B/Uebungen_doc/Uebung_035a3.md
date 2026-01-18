# Uebung_035a3: Ampelschaltung (Variante)

```{index} single: Uebung_035a3: Ampelschaltung (Variante)
```

[Uebung_035a3](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_035a3.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

## 🎧 Podcast

* [Schutzbeschaltung: Varianten und Grundlagen der Spannungsbegrenzung](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Schutzbeschaltung-Varianten-und-Grundlagen-der-Spannungsbegrenzung-e368jq3)

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Übersicht

[cite_start]Strukturelle Variante der Übung 035a2[cite: 1]. Anstelle des `E_TRAIN` Bausteins wird hier der spezialisierte `E_BLINK_TRAIN` genutzt, um die Grün-Blinkphase noch präziser zu steuern. Die Logik der Zustandsüberlappung (Rot-Gelb) wird weiterhin über Sub-Applikations-ODER-Gatter realisiert.