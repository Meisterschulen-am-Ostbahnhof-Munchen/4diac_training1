Hier ist die Dokumentation für die Übung 127 basierend auf den bereitgestellten Daten.

# Uebung_127

![Uebung_127](Uebung_127.png)

* * * * * * * * * *

## Einleitung

Diese Übung demonstriert die Implementierung einer zyklischen ISOBUS-Nachrichtenübertragung (ISOBUS Send Message Cyclic) ohne die Verwendung eines spezifischen Callback-Bausteins (CB). Der Fokus liegt auf der Identifikation eines Netzwerkteilnehmers (z.B. eines Virtual Terminals) und dem anschließenden zyklischen Senden von statischen Daten an diesen Teilnehmer. Zusätzlich wird ein Hardware-Eingang (Button) verwendet, um Aktualisierungen auszulösen.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden verschiedene Funktionsbausteine verwendet, um die Netzwerkkommunikation, Datenaufbereitung und Hardware-Interaktion zu steuern.

### Haupt-Bausteine

*   **NmGetCfInfo_1** (`isobus::pgn::NmGetCfInfo`)
    *   Dieser Baustein ist für das Netzwerkmanagement zuständig. Er sucht auf dem ISOBUS-Netzwerk nach Informationen über Control Functions (CF).
    *   **Parameter:**
        *   `u8CanIdx`: `NODE1` (CAN-Knoten)
        *   `member`: `network`
        *   `address`: `VT_ADD` (Filter-Adresse, wahrscheinlich für ein Virtual Terminal)
        *   `mask`: `VT_FLT` (Filter-Maske)

*   **AlPgnTxNew8Bcycl** (`isobus::pgn::tx::AlPgnTxNew8Bcycl`)
    *   Dieser Baustein verwaltet das zyklische Senden einer neuen 8-Byte Parameter Group Number (PGN).
    *   **Parameter:**
        *   `u32Pgn`: `61184` (Die zu sendende PGN)
        *   `u16DaSize`: `8` (Datengröße in Bytes)
        *   `u8Priority`: `3` (Priorität der Nachricht)
        *   `u16DefRepRate`: `500` (Wiederholrate in Millisekunden)
        *   `Data`: `[16#FA, 16#FB, 16#FC, 16#FD, 16#FE, 16#FF, 16#F1, 16#F2]` (Statisches Daten-Array)

*   **DigitalInput_CLK_I1** (`logiBUS::io::DI::logiBUS_IE`)
    *   Ein Baustein zur Erfassung von digitalen Eingangsereignissen.
    *   **Parameter:**
        *   `QI`: `TRUE`
        *   `Input`: `Input_I1` (Hardware-Eingang)
        *   `InputEvent`: `BUTTON_SINGLE_CLICK` (Ereignistyp)

*   **STRUCT_DEMUX** (`eclipse4diac::convert::STRUCT_DEMUX`)
    *   Mehrfach verwendeter Konvertierungsbaustein, um komplexe Datentypen (`isobus::pgn::NAMEFIELD_T`, `isobus::pgn::CF_INFO_T`, `isobus::pgn::ISONETEVENT_T`) in ihre Bestandteile zu zerlegen. Dies dient oft Debugging- oder Visualisierungszwecken.

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in die Initialisierung des Netzwerks, das Starten der zyklischen Übertragung und die Verarbeitung von Benutzereingaben unterteilen.

1.  **Netzwerkerkennung:**
    *   Der Baustein `NmGetCfInfo_1` überwacht den Bus auf Teilnehmer, die den Filterkriterien (`VT_ADD`, `VT_FLT`) entsprechen.
    *   Sobald Informationen verfügbar sind, wird das Event `IND` ausgelöst.
    *   Die ermittelten Daten (`sNameField`, `sCfInfo`, `sNetEv`) werden an die entsprechenden `STRUCT_DEMUX` Bausteine weitergeleitet, um die Strukturen aufzuschlüsseln.

2.  **Installation der Übertragung:**
    *   Das `IND`-Event von `NmGetCfInfo_1` triggert den Eingang `install` des Sendebausteins `AlPgnTxNew8Bcycl`.
    *   Gleichzeitig werden die Netzwerkinformationen (`sNetEv`) an den Eingang `NmDestin` des Sendebausteins übergeben. Damit weiß der Sendebaustein, an welches Ziel die Nachrichten gerichtet werden sollen.

3.  **Zyklisches Senden:**
    *   Nach der Installation beginnt `AlPgnTxNew8Bcycl` mit dem Senden der PGN 61184.
    *   Die Übertragung erfolgt alle 500 ms (definiert durch `u16DefRepRate`).
    *   Der Inhalt der Nachricht besteht aus den statisch definierten Hexadezimalwerten (FA, FB, FC, ...).

4.  **Hardware-Interaktion:**
    *   Der Baustein `DigitalInput_CLK_I1` wartet auf einen Einzelklick (`BUTTON_SINGLE_CLICK`) am Eingang `Input_I1`.
    *   Bei Betätigung wird das Event `IND` ausgelöst, welches mit dem Eingang `UPD` (Update) am `AlPgnTxNew8Bcycl` verbunden ist. Dies dient dazu, den Sendeprozess zu aktualisieren oder eine sofortige Verarbeitung anzustoßen.

## Zusammenfassung

Die Übung `Uebung_127` zeigt exemplarisch, wie man eine feste ISOBUS-Kommunikation zu einem spezifischen Partner (z.B. einem Terminal) aufbaut. Kernpunkte sind das Filtern des Netzwerks nach dem Zielgerät, die Konfiguration eines zyklischen Senders mit fester Wiederholrate und festen Daten, sowie die Einbindung einer manuellen Trigger-Möglichkeit über einen digitalen Eingang. Die zusätzlichen Demultiplexer-Bausteine ermöglichen einen Einblick in die internen Datenstrukturen des ISOBUS-Protokolls.