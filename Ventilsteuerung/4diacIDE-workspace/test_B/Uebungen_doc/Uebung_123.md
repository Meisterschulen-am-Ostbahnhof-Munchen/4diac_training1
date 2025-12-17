Hier ist die Dokumentationsseite für die Übung `Uebung_123` basierend auf den bereitgestellten Daten.

# Uebung_123

![Bild der Übung, falls vorhanden](Uebung_123.png)

* * * * * * * * * *

## Einleitung
Die **Uebung_123** beschäftigt sich mit der Analyse und Verarbeitung von ISOBUS-Namen und Control Function (CF) Informationen. Ziel der Übung ist es, Identifikationsdaten sowohl vom eigenen Gerät ("thisMember") als auch von anderen Netzwerkteilnehmern (spezifisch einem Virtual Terminal) auszulesen und diese komplexen Datenstrukturen in ihre Einzelteile zu zerlegen, um sie lesbar zu machen.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden Instanzen von `NmGetCfInfo` zur Datenbeschaffung und `STRUCT_DEMUX` zur Datenaufbereitung verwendet.

### Sub-Bausteine: NmGetCfInfo (Instanz 1)
Dieser Baustein wird verwendet, um Informationen über den lokalen Teilnehmer abzurufen.

- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Verwendete Parameter**:
    - **u8CanIdx** = `NODE1` (CAN-Knoten Index)
    - **member** = `thisMember` (Abfrage des eigenen Members/Geräts)
    - **address** = `FLT_ALL_PASS` (Kein Adressfilter)
    - **mask** = `FLT_ALL_PASS` (Keine Maskierung)
- **Funktionsweise**: 
  Dieser Baustein überwacht und liefert die Netzwerkinformationen, CF-Infos und das NAME-Feld des eigenen Geräts.

### Sub-Bausteine: NmGetCfInfo_1 (Instanz 2)
Dieser Baustein wird verwendet, um spezifische Netzwerkteilnehmer zu finden (hier vermutlich ein Virtual Terminal).

- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Verwendete Parameter**:
    - **u8CanIdx** = `NODE1`
    - **member** = `network` (Suche im Netzwerk)
    - **address** = `VT_ADD` (Spezifische Adresse/Filterwert für VT)
    - **mask** = `VT_FLT` (Filtermaske für VT)
- **Funktionsweise**: 
  Im Gegensatz zur ersten Instanz filtert dieser Baustein den CAN-Bus-Verkehr gezielt nach einem Teilnehmer, der durch die Konstanten `VT_ADD` und `VT_FLT` definiert ist (üblicherweise ein Virtual Terminal).

### Sub-Bausteine: STRUCT_DEMUX (Diverse Instanzen)
Mehrere Instanzen dieses Konvertierungsbausteins werden genutzt, um strukturierte Datentypen in ihre Einzelwerte aufzuschlüsseln.

- **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
- **Konfigurationen (StructuredType)**:
    - `isobus::pgn::ISONETEVENT_T`: Zerlegt Netzwerk-Ereignisdaten.
    - `isobus::pgn::CF_INFO_T`: Zerlegt Control Function Informationen.
    - `isobus::pgn::NAMEFIELD_T`: Zerlegt das 64-Bit ISOBUS NAME-Feld (Hersteller, Funktion, Instanz, etc.).
- **Funktionsweise**: 
  Diese Bausteine nehmen die komplexen Ausgänge der `NmGetCfInfo`-Bausteine entgegen und stellen die enthaltenen Datenfelder als einzelne Signale zur Verfügung.

## Programmablauf und Verbindungen

Der Ablauf der Übung teilt sich in zwei parallele Stränge:

1.  **Analyse des eigenen Geräts (Obere Hälfte):**
    *   Der Baustein `NmGetCfInfo` (oben links) liefert Daten über `thisMember`.
    *   Sobald ein Ereignis (`IND`) eintritt, werden die Daten an drei `STRUCT_DEMUX`-Bausteine weitergeleitet.
    *   Hierbei werden die Netzwerkereignisse (`sNetEv`), die CF-Informationen (`sCfInfo`) und das Namensfeld (`sNameField`) detailliert aufgeschlüsselt.

2.  **Analyse eines Netzwerk-Teilnehmers / VT (Untere Hälfte):**
    *   Der Baustein `NmGetCfInfo_1` (unten links) sucht im Netzwerk (`network`) nach einem Gerät, das auf den VT-Filter passt.
    *   Auch hier löst der `IND`-Ausgang die Verarbeitung durch drei weitere `STRUCT_DEMUX`-Bausteine aus.
    *   Dies ermöglicht den direkten Vergleich der Datenstrukturen zwischen dem eigenen Gerät und einem externen ISOBUS-Teilnehmer.

**Lernziele:**
*   Verständnis des ISOBUS NAME-Feldes und der CF-Informationen.
*   Umgang mit komplexen Datentypen (STRUCTs) in 4diac.
*   Einsatz von Filtern (`mask` und `address`) beim Scannen des ISOBUS-Netzwerks.

**Hinweis:** Die verwendeten Konstanten (`FLT_ALL_PASS`, `VT_ADD`, `VT_FLT`) stammen aus einer globalen Konstantenbibliothek (`Uebung_120_129::Filter`).

## Zusammenfassung
Die `Uebung_123` demonstriert die Identifikation von ISOBUS-Geräten. Durch die parallele Abfrage des eigenen Gerätes und eines gefilterten Netzwerkteilnehmers (Virtual Terminal) sowie die anschließende Demultiplexierung der Datenstrukturen, bietet diese Übung eine tiefe Einsicht in die ISOBUS-Kommunikationsparameter und die Struktur des NAME-Feldes nach ISO 11783.