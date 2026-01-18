# Uebung_010b2: Softkey-Release als Auslöser

```{index} single: Uebung_010b2: Softkey-Release als Auslöser
```

[Uebung_010b2](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010b2.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010b2`.

## 📺 Video

* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)

----

![](Uebung_010b2.png)

## Ziel der Übung

Verwendung spezialisierter ISOBUS-Ereignisse zur Steuerung von Software-Flip-Flops.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010b2.SUB` nutzt ein Flip-Flop, das durch das Loslassen eines Softkeys getriggert wird[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_UP_F1`**: Typ `isobus::UT::io::Softkey::Softkey_IE`. Er ist auf das Ereignis `SK_RELEASED` konfiguriert.
  * **`E_T_FF`**: Toggle-Flip-Flop.

-----

## Funktionsweise

Das Ereignis `IND` wird erst gefeuert, wenn der Nutzer den Finger vom Softkey nimmt. Dies entspricht dem intuitiven Klick-Verhalten. Jeder vollständige Tastendruck (Drücken + Loslassen) schaltet das Licht um.