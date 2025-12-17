Hier ist die Dokumentation für die Übung **Uebung_121**, basierend auf den bereitgestellten Daten.

# Uebung_121

![Uebung_121](Uebung_121.png)

* * * * * * * * * *

## Einleitung
Die Übung **Uebung_121** befasst sich mit der Handhabung des ISOBUS-Namens (NAME) gemäß ISO 11783. Sie demonstriert, wie die Namensfelder in Strukturen verpackt, in den 64-Bit ISOBUS-Namen konvertiert und wieder zurückgewandelt werden. Zusätzlich zeigt die Übung, wie Informationen über Steuergeräte (Control Functions, CF) aus dem Netzwerk abgerufen und analysiert werden können.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden verschiedene Bausteine zur Strukturkonvertierung und ISOBUS-spezifische Bausteine verwendet.

### Sub-Bausteine: Struktur-Konverter
Diese Bausteine dienen dem Zusammenfügen (MUX) und Zerlegen (DEMUX) von komplexen Datentypen.

- **Typ**: `eclipse4diac::convert::STRUCT_MUX` und `eclipse4diac::convert::STRUCT_DEMUX`
- **Verwendete Instanzen**:
    - **STRUCT_MUX** & **STRUCT_MUX_1**:
        - Attribut `StructuredType`: `isobus::pgn::NAMEFIELD_T` (Struktur für die einzelnen Felder des ISOBUS-Namens).
    - **STRUCT_DEMUX** & **STRUCT_DEMUX_1**:
        - Attribut `StructuredType`: `isobus::pgn::NAMEFIELD_T`.
    - **STRUCT_DEMUX_2**:
        - Attribut `StructuredType`: `isobus::pgn::CF_INFO_T` (Informationen über eine Control Function).
    - **STRUCT_DEMUX_3**:
        - Attribut `StructuredType`: `isobus::pgn::ISONETEVENT_T` (ISOBUS Netzwerk-Ereignisse).

### Sub-Bausteine: ISOBUS Namens-Handling
Bausteine zur Verarbeitung des 64-Bit Namens.

- **Typ**: `isobus::pgn::NmSetName`
- **Funktionsweise**: Erstellt aus den einzelnen Namensfeldern (übergeben als Struktur) den 64-Bit ISOBUS-Namen.

- **Typ**: `isobus::pgn::NmSetNameField`
- **Funktionsweise**: Nimmt einen 64-Bit ISOBUS-Namen entgegen und extrahiert daraus die einzelnen Felder in eine Struktur.

### Sub-Bausteine: ISOBUS Netzwerk-Informationen
- **Typ**: `isobus::pgn::NmGetCfInfo`
- **Funktionsweise**: Überwacht das Netzwerk auf Informationen zu Control Functions.
- **Parameter**:
    - `u8CanIdx` = `NODE1` (Der verwendete CAN-Knoten).
    - `member` = `thisMember` (Mitgliedsidentifikation).
    - `address` = `FLT_ALL_PASS` (Filter für Adressen, hier: alle passieren lassen).
    - `mask` = `FLT_ALL_PASS` (Maske für den Filter).

## Programmablauf und Verbindungen

Das Netzwerk der Übung ist in drei logische Bereiche unterteilt, die unterschiedliche Aspekte der ISOBUS-Kommunikation behandeln:

1.  **Einfache Struktur-Prüfung (Oben links):**
    *   Ein `STRUCT_MUX` Baustein erstellt eine `NAMEFIELD_T` Struktur.
    *   Diese wird direkt an einen `STRUCT_DEMUX` Baustein weitergegeben. Dies dient vermutlich dazu, die Datenkonsistenz der Struktur zu prüfen oder Signale durchzuschleifen.

2.  **Namens-Konvertierungskette (Mitte/Unten):**
    *   Ein `STRUCT_MUX_1` erstellt eine `NAMEFIELD_T` Struktur aus Einzelwerten.
    *   Der Baustein `NmSetName` konvertiert diese Struktur (`psNameField`) in einen rohen ISOBUS-Namen (Array of Byte / 64-Bit Repräsentation).
    *   Dieses Ergebnis (`au8IsoName`) wird direkt an `NmSetNameField` weitergegeben.
    *   `NmSetNameField` macht den Vorgang rückgängig und zerlegt den Namen wieder in seine Felder.
    *   Abschließend zerlegt `STRUCT_DEMUX_1` die resultierende Struktur wieder in Einzelvariablen. Dieser Ablauf validiert die korrekte Kodierung und Dekodierung des ISOBUS-Namens.

3.  **Netzwerk-Überwachung (Unten):**
    *   Der Baustein `NmGetCfInfo` ist so konfiguriert, dass er Informationen vom CAN-Knoten `NODE1` empfängt.
    *   Wenn ein Ereignis eintritt (`IND`), werden zwei Datenströme ausgegeben:
        *   `sNetEv`: Enthält Netzwerkereignisse (z.B. Adressclaim). Diese werden im `STRUCT_DEMUX_3` (`ISONETEVENT_T`) aufgeschlüsselt.
        *   `sCfInfo`: Enthält spezifische Informationen zur Control Function. Diese werden im `STRUCT_DEMUX_2` (`CF_INFO_T`) aufgeschlüsselt.

## Zusammenfassung
Die Übung 121 vermittelt fundierte Kenntnisse über den Aufbau des ISOBUS-Namens und dessen Verarbeitung innerhalb der IEC 61499 Umgebung. Durch die Konvertierungsketten wird sichergestellt, dass der Anwender versteht, wie aus den einzelnen Parametern (wie Hersteller-Code, Funktions-Instanz etc.) der eindeutige Name generiert wird. Zusätzlich bietet die Übung einen Einblick in das Monitoring des ISOBUS-Netzwerks durch das Auslesen von Control-Function-Informationen.