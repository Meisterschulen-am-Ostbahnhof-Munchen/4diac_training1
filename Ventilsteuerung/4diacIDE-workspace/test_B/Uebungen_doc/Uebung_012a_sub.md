Hier ist die Dokumentation für die Übung `Uebung_012a_sub` basierend auf den bereitgestellten Daten.

# Uebung_012a_sub - Numeric Value Input und Speichern

*(Bild der Übung, falls vorhanden)*

* * * * * * * * * *

## Einleitung
Diese Übung behandelt einen Sub-Application-Baustein (`Uebung_012a_sub`), der dafür konzipiert ist, einen numerischen Wert über ein ISOBUS Virtual Terminal (UT) einzugeben, diesen persistent zu speichern und den aktuellen Wert auf dem Display zurückzuschreiben. Er verbindet die Eingabeschnittstelle mit einem nicht-flüchtigen Speicher (NVS) und sorgt für die korrekte Datentypkonvertierung.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_012a_sub
Dieser Baustein kapselt die Logik für die Eingabe und Speicherung.

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **ID**: isobus::UT::io::NumericValue::NumericValue_ID
        - Parameter: `QI` = `TRUE`
        - Dateneingang: `u16ObjId` (Objekt-ID des UI-Elements)
        - Datenausgang: `IN` (Der eingegebene Wert vom UT)
        - Ereignisausgang: `IND` (Signalisiert eine Eingabeänderung)
    
    - **F_DWORD_TO_UDINT**: iec61131::conversion::F_DWORD_TO_UDINT
        - Dateneingang: `IN`
        - Datenausgang: `OUT`
        - Funktion: Konvertiert den Datentyp DWORD in UDINT.

    - **NVS**: logiBUS::storage::esp32_nvs::NVS
        - Parameter: `QI` = `TRUE`
        - Parameter: `DEFAULT_VALUE` = `UDINT#0`
        - Dateneingang: `KEY` (Schlüssel für den Speicherort), `VALUE` (Zu speichernder Wert)
        - Datenausgang: `VALUEO` (Gelesener Wert)
        - Ereigniseingang: `SET` (Speichern), `GET` (Laden)
        - Ereignisausgang: `INITO` (Initialisierung fertig), `SETO` (Speichern bestätigt), `GETO` (Laden bestätigt)

    - **Q_NumericValue**: isobus::UT::Q::Q_NumericValue
        - Dateneingang: `u16ObjId`, `u32NewValue`
        - Ereigniseingang: `REQ` (Aktualisierung anfordern)

- **Funktionsweise**:
    Der Baustein reagiert auf Benutzereingaben vom Virtual Terminal (`ID`), konvertiert diese und speichert sie im permanenten Speicher (`NVS`). Gleichzeitig wird beim Start oder nach dem Speichern der Wert wieder aus dem Speicher gelesen und zur Anzeige an das Terminal zurückgesendet (`Q_NumericValue`), um die Anzeige synchron zu halten.

## Programmablauf und Verbindungen

Der Ablauf innerhalb der Sub-Application lässt sich in zwei Hauptpfade unterteilen: **Initialisierung/Laden** und **Eingabe/Speichern**.

1.  **Initialisierung und Laden:**
    *   Der `NVS`-Baustein signalisiert über `INITO`, dass er bereit ist. Dies triggert sofort den Eingang `GET` am selben Baustein, um den gespeicherten Wert zu laden.
    *   Sobald der Wert erfolgreich geladen wurde (`GETO`), wird dieser:
        *   An den Ausgang `VALUEO` der Sub-App übergeben.
        *   An den Baustein `Q_NumericValue` weitergeleitet (Eingang `u32NewValue`), welcher das UI-Element auf dem Virtual Terminal aktualisiert.
        *   Ein `IND`-Event am Ausgang der Sub-App ausgelöst.

2.  **Benutzereingabe und Speichern:**
    *   Wenn der Benutzer einen Wert am Terminal ändert, löst der Baustein `ID` das Event `IND` aus.
    *   Der Rohwert wird an `F_DWORD_TO_UDINT` übergeben, um das Format anzupassen.
    *   Nach der Konvertierung (`CNF`) wird das Event `SET` am `NVS`-Baustein ausgelöst, um den neuen Wert unter dem angegebenen `KEY` zu speichern.
    *   Nach erfolgreichem Speichern (`SETO`) wird das `IND`-Event der Sub-App ausgelöst, um den Vorgang nach außen zu bestätigen.

**Wichtige Datenverbindungen:**
*   **u16ObjId**: Verbindet den Eingang der Sub-App sowohl mit dem Eingabebaustein (`ID`) als auch mit dem Ausgabebaustein (`Q_NumericValue`), damit beide auf dasselbe UI-Element zugreifen.
*   **KEY**: Dient als eindeutiger Bezeichner für den Speicherort im NVS.

## Zusammenfassung
Die Übung `Uebung_012a_sub` demonstriert die Erstellung eines wiederverwendbaren Moduls zur Handhabung persistenter Daten in Verbindung mit einer ISOBUS-Benutzeroberfläche. Sie zeigt, wie man Eingabeereignisse verarbeitet, Datentypen konvertiert und Werte dauerhaft in einem ESP32-NVS-Speicher ablegt, während gleichzeitig die Anzeige auf dem Terminal konsistent gehalten wird.