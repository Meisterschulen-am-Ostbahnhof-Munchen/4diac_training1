# Uebung_011_AUDI: Numerische Eingabe mit Adaptern

```{index} single: Uebung_011_AUDI: Numerische Eingabe mit Adaptern
```

[Uebung_011_AUDI](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_011_AUDI.html)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_011_AUDI`. Sie ist die adapterbasierte Variante der Übung 011 und zeigt, wie numerische Werte effizient und übersichtlich verarbeitet werden.

## 🎧 Podcast

* [Code-Renovierung mit AX-Adaptern: Wie Eclipse 4diac™ durch Signal-Bündelung Komplexität besiegt](https://podcasters.spotify.com/pod/show/logibus/episodes/Code-Renovierung-mit-AX-Adaptern-Wie-Eclipse-4diac-durch-Signal-Bndelung-Komplexitt-besiegt-e3ahcd1)

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

----

![](Uebung_011_AUDI.png)

## Ziel der Übung

Erlernen der modernen, adapterbasierten Verarbeitung von ISOBUS-Terminal-Eingaben. Durch die Verwendung von Adaptern wird das Baustein-Netzwerk kompakter und die Trennung von Ereignis- und Datenfluss erfolgt implizit innerhalb der Adapter-Struktur.

-----

## Beschreibung und Komponenten

Die Subapplikation `Uebung_011_AUDI.SUB` nutzt einen adapterbasierten Eingabe-Baustein.

### Funktionsbausteine (FBs)

  * **`InputNumber_I1`**: Typ `NumericValue_IDA`. Dieser Baustein stellt ein numerisches Eingabefeld auf dem ISOBUS-Terminal dar. Im Gegensatz zur Standard-Variante (`_ID`) nutzt dieser Baustein einen AX-basierten Adapter-Ausgang (`IN`), der sowohl das Ereignis als auch den DWORD-Wert bündelt.
  * **`F_DWORD_TO_UDINT`**: Hier wird der neue Bausteintyp `AD_TO_AUDI` verwendet. Er nimmt den `AD`-Adapter entgegen und gibt einen `AUDI`-Adapter aus, der den Wert als `UDINT` führt.

-----

## Funktionsweise

Die Verbindung zwischen Eingabe und Konvertierung erfolgt ausschließlich über eine Adapter-Linie:

```xml
<AdapterConnections>
    <Connection Source="InputNumber_I1.IN" Destination="F_DWORD_TO_UDINT.AD_IN"/>
</AdapterConnections>
```

1.  Der Nutzer gibt am Terminal einen Wert ein (z. B. "100").
2.  Nach der Bestätigung sendet der Baustein `InputNumber_I1` das Update über den Adapter-Plug.
3.  Der Konverter `AD_TO_AUDI` (instanziiert als `F_DWORD_TO_UDINT`) empfängt dieses Paket, wandelt den Typ und stellt das Ergebnis am `AUDI`-Plug für die restliche Logik bereit.

-----

## Fazit

Die Übung verdeutlicht den Vorteil von Adaptern: Anstatt separate Linien für Ereignisse (`REQ`/`CNF`) und Daten (`IN`/`OUT`) ziehen zu müssen, reicht eine einzige Adapter-Verbindung aus. Dies reduziert die Fehleranfälligkeit und erhöht die Lesbarkeit des Programms erheblich.