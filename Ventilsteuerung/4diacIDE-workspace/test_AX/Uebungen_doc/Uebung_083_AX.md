# Uebung_083_AX: Präzisions-Zähler (AUDI) mit Adaptern

```{index} single: Uebung_083_AX: Präzisions-Zähler (AUDI) mit Adaptern
```

[Uebung_083_AX](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_083_AX.html)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_083_AX`. Sie ist die adapterbasierte Variante der Übung 083 und demonstriert einen Auf-/Abwärtszähler (`AUDI_CTUD_UDINT`) für vorzeichenlose 32-Bit-Ganzzahlen in einer AX-Umgebung.

## 🎧 Podcast

* [E_CTD: Ereignisgesteuerter Abwärtszähler nach IEC 61499](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTD-Ereignisgesteuerter-Abwrtszhler-nach-IEC-61499-e368lli)
* [E_CTUD: Bidirektionaler Zähler in IEC 61499 Systemen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/E_CTUD-Bidirektionaler-Zhler-in-IEC-61499-Systemen-e368lmb)
* [Meisterwissen 61499: Der Ereignisgesteuerte Aufwärtszähler (E_CTU) – Robustes Zählen in Landmaschinen-Steuerungen](https://podcasters.spotify.com/pod/show/iec-61499-grundkurs-de/episodes/Meisterwissen-61499-Der-Ereignisgesteuerte-Aufwrtszhler-E_CTU--Robustes-Zhlen-in-Landmaschinen-Steuerungen-e3a9q5n)
* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)
* [Löt-Meisterklasse Profi-Tricks für Präzisionselektronik](https://podcasters.spotify.com/pod/show/ms-muc-lama/episodes/Lt-Meisterklasse-Profi-Tricks-fr-Przisionselektronik-e3augdi)

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

----

![](Uebung_083_AX.png)

## Ziel der Übung

Erlernen der adapterbasierten Steuerung eines Hochleistungs-Zählers und der Anzeige des Zählwerts auf einem ISOBUS-Terminal. Die Übung zeigt die Nutzung von AX-Adaptern für die Eingänge (`CU`, `CD`, `R`, `LD`) und den Zählwert (`CV`) sowie für die Ansteuerung der numerischen Anzeige.

-----

## Beschreibung und Komponenten

Die Subapplikation `Uebung_083_AX.SUB` nutzt folgende adapterbasierte Funktionsbausteine:

### Funktionsbausteine (FBs)

  * **`DigitalInput_CLK_I1` bis `I4`**: Eingangsbausteine vom Typ `logiBUS::io::DI::logiBUS_IXA`. Sie liefern über einen AX-Adapter ein Ereignis und ein Bool-Signal bei Tasterdruck.
  * **`AUDI_CTUD_UDINT`**: Der adapterbasierte Auf-/Abwärtszähler. Er erwartet Events an `CU`, `CD`, `R` und einen `AUDI`-Adapter an `PV` sowie gibt den Zählwert über den `CV`-Adapter aus.
  * **`DigitalOutput_Q1` & `Q2`**: Ausgangsbausteine vom Typ `logiBUS::io::DQ::logiBUS_QXA` für die Anzeige des Zählerstatus (`QU`, `QD`).
  * **`Q_NumericValue_AUDI`**: ISOBUS-Ausgangsbaustein für die numerische Anzeige am Terminal, empfängt den Wert über einen `AUDI`-Adapter.
  * **`AUDI_UDINT_TO_UDI`**: Konvertierungsbaustein, der einen `UDINT`-Literal (`UDINT#5`) in einen `AUDI`-Adapter umwandelt, um den `PV`-Eingang des Zählers zu versorgen.

-----

## Funktionsweise

1.  **Zählen**: `DigitalInput_CLK_I1.OUT` (Taster I1) triggert `AUDI_CTUD_UDINT.CU` (Zähler hoch). `DigitalInput_CLK_I2.OUT` (Taster I2) triggert `AUDI_CTUD_UDINT.CD` (Zähler runter).
2.  **Reset/Load**: `DigitalInput_CLK_I3.OUT` (Taster I3) triggert `AUDI_CTUD_UDINT.R` (Reset). `DigitalInput_CLK_I4.IND` triggert `AUDI_UDINT_TO_UDI.REQ`, der den Wert `UDINT#5` an `AUDI_CTUD_UDINT.PV` übergibt und damit den Zähler lädt.
3.  **Anzeige**: Der Zählerstatus `QU` und `QD` steuert `DigitalOutput_Q1.OUT` und `DigitalOutput_Q2.OUT`. Der aktuelle Zählerwert (`AUDI_CTUD_UDINT.CV`) wird an `Q_NumericValue_AUDI.u32NewValue` gesendet und am ISOBUS-Terminal angezeigt.

-----

## Hinweise zur Implementierung

*   **Eingangstypen**: Die `DigitalInput_CLK_I` Bausteine sind vom Typ `logiBUS_IE`, obwohl `logiBUS_IXA` die Adapter-Variante wäre. Deren `InputEvent`-Parameter sind in einem AX-Kontext redundant und könnten entfernt werden, wenn `logiBUS_IXA` verwendet wird.
*   **PV-Initialisierung**: Die direkte Zuweisung eines `PV`-Parameters (`UINT#5`) an `AUDI_CTUD_UDINT` ist nicht adaptergerecht. Die aktuelle Lösung über den Konverter `AUDI_UDINT_TO_UDI` ist funktional, aber etwas umständlich.