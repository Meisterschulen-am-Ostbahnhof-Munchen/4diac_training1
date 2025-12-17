Hier ist die Dokumentation für die Übung `Uebung_020c2_sub` basierend auf dem bereitgestellten XML-Code.

# Uebung_020c2_sub

*(Hier Platzhalter für ein Bild der Übung einfügen)*

* * * * * * * * * *

## Einleitung
Die Sub-Applikation `Uebung_020c2_sub` dient der Verwaltung eines numerischen Eingabewertes. Sie realisiert eine Schnittstelle zwischen einem grafischen Eingabeelement (Universal Terminal / ISOBUS), einer Typkonvertierung und einem persistenten Speicher (NVS). Das Ziel ist es, eine eingegebene Zeit (oder einen anderen numerischen Wert) entgegenzunehmen, in ein passendes Format zu konvertieren, dauerhaft zu speichern und den aktuellen Wert zur Anzeige zurückzumelden.

## Verwendete Funktionsbausteine (FBs)

Diese Übung ist selbst als Sub-Applikation (`SubAppType`) definiert und kapselt die Logik für die persistente Dateneingabe.

### Sub-Bausteine: Uebung_020c2_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:

    - **InputNumber_I1**: `isobus::UT::io::NumericValue::NumericValue_ID`
        - **Parameter**: 
            - `QI` = TRUE
            - `u16ObjId` = InputNumber_I1
        - **Beschreibung**: Dient als Schnittstelle zum Eingabefeld auf dem Universal Terminal (UT). Er empfängt Benutzereingaben.

    - **F_DWORD_TO_UDINT**: `iec61131::conversion::F_DWORD_TO_UDINT`
        - **Parameter**: Keine statischen Parameter definiert.
        - **Beschreibung**: Konvertiert den Datentyp DWORD (vom Eingabefeld) in UDINT (für die Weiterverarbeitung und Speicherung).

    - **NVS**: `logiBUS::storage::esp32_nvs::NVS`
        - **Parameter**: 
            - `QI` = TRUE
            - `DEFAULT_VALUE` = UDINT#0
        - **Dateneingang**: `KEY` (von außen übergeben), `VALUE` (vom Konverter)
        - **Datenausgang**: `VALUEO`
        - **Beschreibung**: Baustein für den "Non-Volatile Storage" (nicht-flüchtiger Speicher). Er speichert Werte dauerhaft auf dem Controller (z.B. ESP32), sodass sie auch nach einem Neustart erhalten bleiben.

    - **Q_NumericValue**: `isobus::UT::Q::Q_NumericValue`
        - **Dateneingang**: `u16ObjId` (von außen übergeben), `u32NewValue` (vom NVS)
        - **Beschreibung**: Aktualisiert den auf dem Display angezeigten numerischen Wert.

- **Funktionsweise**:
    Die Sub-Applikation verbindet die Eingabe, Speicherung und Anzeige eines Wertes.
    1.  **Initialisierung**: Sobald der NVS-Baustein initialisiert ist (`INITO`), fordert er den gespeicherten Wert an (`GET`).
    2.  **Eingabe**: Bei einer Änderung am `InputNumber_I1` wird der Wert konvertiert (`F_DWORD_TO_UDINT`).
    3.  **Speichern**: Der konvertierte Wert wird an den `NVS` gesendet und dort unter dem Schlüssel `KEY` gespeichert (`SET`).
    4.  **Anzeige**: Der gespeicherte oder abgerufene Wert (`VALUEO` vom NVS) wird an `Q_NumericValue` gesendet, um die Anzeige zu aktualisieren, und steht gleichzeitig am Ausgang `VALUEO` der Sub-Applikation zur Verfügung.

## Programmablauf und Verbindungen

Der Ablauf innerhalb dieser Sub-Applikation gewährleistet, dass Benutzereingaben nicht verloren gehen und das System stets mit dem aktuell gespeicherten Wert arbeitet.

1.  **Startvorgang**: 
    - Der `NVS` Baustein triggert über `INITO` sofort seinen eigenen `GET` Eingang. Dies lädt den zuletzt gespeicherten Wert aus dem Speicher.
    - Über `GETO` (Get Output) wird dieser Wert an `Q_NumericValue` weitergegeben, um das Display zu aktualisieren.

2.  **Benutzerinteraktion**:
    - Wenn der Benutzer einen Wert am Terminal ändert, sendet `InputNumber_I1` ein `IND` Event.
    - Die Daten fließen von `InputNumber_I1.IN` zum Konverter `F_DWORD_TO_UDINT`.

3.  **Datenverarbeitung und Speicherung**:
    - Nach der Konvertierung triggert das `CNF` Event des Konverters den `SET` Eingang des `NVS`.
    - Der Wert wird unter dem Variablennamen gespeichert, der am Eingang `KEY` der Sub-Applikation anliegt.

4.  **Rückmeldung**:
    - Sowohl nach dem Speichern (`SETO`) als auch nach dem Laden (`GETO`) wird das Event `IND` der Sub-Applikation ausgelöst, um übergeordnete Bausteine zu informieren.
    - Parallel dazu wird `Q_NumericValue` getriggert, um sicherzustellen, dass das UI den tatsächlich gespeicherten Wert anzeigt.

**Wichtige Verbindungen:**
- Der Eingang `KEY` der Sub-App bestimmt, unter welchem Namen der Wert im Speicher abgelegt wird.
- Der Eingang `u16ObjId` bestimmt, welches UI-Element aktualisiert wird.

## Zusammenfassung
Die Sub-Applikation `Uebung_020c2_sub` ist ein robuster Baustein zur Parameterverwaltung. Sie kombiniert UI-Interaktion mit persistenter Datenspeicherung. Dies ist essenziell für Einstellungen wie Einschaltverzögerungen oder Sollwerte, die auch nach einem Stromausfall der Steuerung erhalten bleiben sollen. Durch die Kapselung in einer Sub-Applikation kann diese Logik einfach für verschiedene Parameter wiederverwendet werden, indem lediglich der `KEY` und die `u16ObjId` angepasst werden.