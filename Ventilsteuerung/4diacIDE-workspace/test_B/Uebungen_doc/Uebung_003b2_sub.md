Hier ist die Dokumentation für die Übung basierend auf der bereitgestellten `Uebung_003b2_sub` Datei.

# Uebung_003b2_sub

![Bild der Übung, falls vorhanden](path_to_image_placeholder.png)

* * * * * * * * * *

## Einleitung
Die Sub-Applikation **Uebung_003b2_sub** implementiert eine generische Weiterleitung eines digitalen Eingangssignals auf einen digitalen Ausgang. Sie dient dazu, hardware-spezifische Eingangs- und Ausgangsdefinitionen zu kapseln und eine direkte logische Verbindung zwischen ihnen herzustellen ("IX auf QX"). Der Baustein fungiert als Brücke, um den Status eines physikalischen Eingangs direkt auf einen physikalischen Ausgang zu spiegeln.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden spezifische IO-Bausteine verwendet, um die Hardware-Schnittstellen anzusprechen.

### Sub-Bausteine: Uebung_003b2_sub
- **Typ**: SubAppType
- **Beschreibung**: Kapselung der Logik zur Verbindung eines `Funk_DI` Eingangs mit einem `DataPanel_MI_DO` Ausgang.
- **Verwendete interne FBs**:

    - **IX**: `Funk::io::DI::Funk_IX`
        - **Parameter**:
            - `QI` = `TRUE` (Baustein ist permanent aktiviert)
            - `PARAMS` = "" (Leerstring)
        - **Dateneingang**:
            - `Input`: Verbunden mit der SubApp-Schnittstelle `Input` (Typ: `Funk_DI_S`). Dies definiert, welcher physikalische Eingang gelesen wird.
        - **Ereignisausgang**: `IND` (Indication - signalisiert neuen Datenwert)
        - **Datenausgang**: `IN` (Der aktuelle Wert des Eingangs)

    - **QX**: `DataPanel::io::MI::DQ::DataPanel_MI_QX`
        - **Parameter**:
            - `QI` = `TRUE` (Baustein ist permanent aktiviert)
        - **Dateneingang**:
            - `u8SAMember`: Verbunden mit der SubApp-Schnittstelle `u8SAMember` (Knotenadresse).
            - `Output`: Verbunden mit der SubApp-Schnittstelle `Output` (Typ: `DataPanel_MI_DO_S`). Dies definiert, welcher physikalische Ausgang geschaltet wird.
            - `OUT`: Empfängt das Signal vom Datenausgang `IN` des Bausteins `IX`.
        - **Ereigniseingang**: `REQ` (Request - fordert das Schreiben des Ausgangs an)

- **Funktionsweise**:
    Der Sub-Baustein nimmt Konfigurationsvariablen für Eingang (`Input`) und Ausgang (`Output`, `u8SAMember`) entgegen und leitet diese an die internen IO-Bausteine weiter. Die logische Verknüpfung erfolgt direkt intern: Sobald der Eingangbaustein `IX` eine Änderung feststellt, triggert er den Ausgangsbaustein `QX` und übergibt den neuen Status (`TRUE` oder `FALSE`).

## Programmablauf und Verbindungen

Der Ablauf innerhalb dieser Sub-Applikation ist ereignisgesteuert und linear:

1.  **Initialisierung**: Die Schnittstellenvariablen (`Input`, `u8SAMember`, `Output`) konfigurieren die internen Bausteine `IX` und `QX` beim Start, um festzulegen, welche Hardware-Pins angesprochen werden sollen.
2.  **Signalerfassung**: Der Baustein `IX` überwacht den definierten digitalen Eingang.
3.  **Signalweiterleitung (Event)**: Wenn der Baustein `IX` ein Ereignis generiert (`IND`), wird dieses direkt an den `REQ`-Eingang des Bausteins `QX` weitergeleitet.
4.  **Datenweiterleitung**: Gleichzeitig wird der logische Zustand des Eingangs (`IX.IN`) an den Ausgangswert (`QX.OUT`) übergeben.
5.  **Aktion**: Der Baustein `QX` schreibt den empfangenen Wert auf den konfigurierten physikalischen Ausgang.

**Lernziele:**
*   Verständnis von Sub-Applikationen zur Kapselung von Logik.
*   Umgang mit hardwarenahen IO-Bausteinen (`IX` für Inputs, `QX` für Outputs).
*   Realisierung einer direkten Durchleitung (Mapping) von Signalen in 4diac.

## Zusammenfassung
Die `Uebung_003b2_sub` ist ein kompakter Baustein zur direkten Kopplung eines Eingangs mit einem Ausgang. Durch die Verwendung generischer Datentypen an den Schnittstellen (`Funk_DI_S` und `DataPanel_MI_DO_S`) ist dieser Baustein wiederverwendbar, um verschiedene Eingangs-Ausgangs-Paare zu verknüpfen, ohne die interne Logik neu programmieren zu müssen. Er stellt eine elementare Funktion der Steuerungstechnik dar: Das direkte Schalten eines Ausgangs basierend auf einem Eingangssignal.