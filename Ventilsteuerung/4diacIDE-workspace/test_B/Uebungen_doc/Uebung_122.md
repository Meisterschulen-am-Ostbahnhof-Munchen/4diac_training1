Hier ist die Dokumentationsseite für die Übung **Uebung_122** basierend auf den bereitgestellten Daten.

# Uebung_122

![Bild der Übung, falls vorhanden](path/to/image_placeholder.png)

* * * * * * * * * *

## Einleitung
Diese Übung befasst sich mit der Analyse des **ISOBUS NAME**-Feldes. Ziel ist es, Informationen über Teilnehmer am CAN-Netzwerk (Control Functions) abzurufen und deren eindeutige 64-Bit-Kennung (den NAME nach ISO 11783-5) in ihre Bestandteile zu zerlegen. Dies ermöglicht die Identifikation von Hersteller, Geräteklasse, Funktion und Instanz der angeschlossenen Geräte.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden verschiedene Funktionsbausteine instanziiert, um die Netzwerkanalyse und Datenaufbereitung durchzuführen.

### Sub-Bausteine:

Da es sich bei `Uebung_122` um einen `SubAppType` handelt, besteht dieser aus einem Netzwerk von verschalteten Funktionsbausteinen. Hier sind die verwendeten Komponenten:

- **NmGetCfInfo**
    - **Typ**: `isobus::pgn::NmGetCfInfo`
    - **Beschreibung**: Dieser Baustein ruft Informationen über Control Functions (CF) im Netzwerk ab.
    - **Parameter**:
        - `u8CanIdx` = `NODE1` (Definiert den verwendeten CAN-Knoten)
        - `member` = `network`
        - `address` = `FLT_ALL_PASS` (Filter für alle Adressen)
        - `mask` = `FLT_ALL_PASS`

- **LOG_16**
    - **Typ**: `logiBUS::utils::logging::LOG_16`
    - **Beschreibung**: Ein Hilfsbaustein, der ein Array von Eingangsdaten (hier Netzwerkereignisse) auf bis zu 16 einzelne Ausgänge aufteilt, um diese parallel verarbeiten zu können.

- **STRUCT_DEMUX (SD_A_1 bis SD_A_16)**
    - **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
    - **Konfiguration**: `StructuredType` = `isobus::pgn::ISONETEVENT_T`
    - **Beschreibung**: Dient dazu, das komplexe Struktur-Signal `ISONETEVENT_T` (Netzwerkereignis) in seine Einzelteile zu zerlegen. Wichtig ist hier vor allem der Ausgang `cfName` (Control Function Name).

- **NmSetNameField (NmSetNF_1 bis NmSetNF_16)**
    - **Typ**: `isobus::pgn::NmSetNameField`
    - **Beschreibung**: Dieser Baustein nimmt einen 8-Byte ISOBUS-Namen (Array) entgegen und interpretiert die darin codierten Felder gemäß der Norm. Er bereitet die Struktur `NAMEFIELD_T` vor.

- **STRUCT_DEMUX (SD_C_1 bis SD_C_16)**
    - **Typ**: `eclipse4diac::convert::STRUCT_DEMUX`
    - **Konfiguration**: `StructuredType` = `isobus::pgn::NAMEFIELD_T`
    - **Beschreibung**: Zerlegt die vom `NmSetNameField` erzeugte Struktur, um Zugriff auf die einzelnen Parameter des Namens zu gewähren (z.B. Manufacturer Code, Device Class, Function, etc.).

## Programmablauf und Verbindungen

Der Ablauf der Übung ist als Pipeline zur Datenverarbeitung aufgebaut:

1.  **Datenerfassung**: Der Baustein `NmGetCfInfo` überwacht den CAN-Bus (`NODE1`) auf vorhandene Teilnehmer und deren Statusnachrichten.
2.  **Verteilung**: Die empfangenen Informationen (`sNetEv`) werden an den `LOG_16` Baustein weitergeleitet. Dieser verteilt die Liste der Netzwerkereignisse auf 16 einzelne Kanäle.
3.  **Verarbeitung (Parallel für 16 Kanäle)**:
    *   **Extraktion**: Für jeden Kanal (1 bis 16) zerlegt ein `STRUCT_DEMUX` (SD_A_x) das Netzwerkereignis.
    *   **Namens-Interpretation**: Das extrahierte `cfName`-Array (der 64-Bit Name) wird an den Baustein `NmSetNF_x` übergeben. Dieser Baustein "parst" die Bytes.
    *   **Detail-Anzeige**: Das Ergebnis der Interpretation wird durch einen weiteren `STRUCT_DEMUX` (SD_C_x) aufgeschlüsselt. Am Ende stehen die einzelnen Komponenten des ISOBUS-Namens zur Verfügung, wie zum Beispiel:
        *   *Self Configurable Address*
        *   *Industry Group*
        *   *Device Class*
        *   *Function*
        *   *Manufacturer Code*
        *   *Identity Number*

**Lernziele:**
*   Verständnis des Aufbaus eines ISOBUS Namens (64-Bit Identifier).
*   Umgang mit komplexen Datentypen (`STRUCT`) und deren Zerlegung (`DEMUX`) in 4diac.
*   Verwendung von Schleifen-ähnlichen Strukturen durch parallele Instanziierung (hier 16-fach) zur Verarbeitung von Listen.

## Zusammenfassung
Die Übung `Uebung_122` stellt ein Diagnose-Tool dar, das den ISOBUS scannt und die Identifikationsmerkmale (NAME-Feld) von bis zu 16 Geräten detailliert aufschlüsselt. Sie demonstriert die Kette von der Rohdatenerfassung auf dem CAN-Bus bis zur menschenlesbaren Interpretation der Geräteparameter.