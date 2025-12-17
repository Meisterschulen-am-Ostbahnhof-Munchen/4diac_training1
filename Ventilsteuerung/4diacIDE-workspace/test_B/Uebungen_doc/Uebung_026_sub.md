Hier ist die Dokumentation für die Übung basierend auf den bereitgestellten Daten.

# Uebung_026_sub - Spiegelabfolge (6)

![Bild der Übung, falls vorhanden](pfad/zum/bild.png)

* * * * * * * * * *

## Einleitung

Bei dieser Übung handelt es sich um eine Sub-Applikation (`SubAppType`), die als intelligenter Treiberbaustein für einen digitalen Ausgang fungiert. Der Baustein implementiert eine Speicherfunktion (Setzen/Rücksetzen) für einen Hardware-Ausgang und signalisiert über einen Event-Ausgang, wenn der Ausgang aktiviert wurde. Er dient der Kapselung von Logik zur Ansteuerung von Aktoren über den LogiBUS.

## Verwendete Funktionsbausteine (FBs)

Dieser Baustein ist als SubApp realisiert und enthält im internen Netzwerk verschiedene IEC 61499 Standard- und LogiBUS-Bausteine.

### Sub-Bausteine: Uebung_026_sub
- **Typ**: SubAppType
- **Beschreibung**: Steuerung eines Digitalausgangs mit Speicherverhalten und gefilterter Rückmeldung.
- **Verwendete interne FBs**:

    - **E_SR**: iec61499::events::E_SR
        - **Typ**: Bistabiles Element (Set/Reset-Flip-Flop)
        - **Parameter**: Keine statischen Parameter.
        - **Ereignisausgang/-eingang**: 
            - Eingänge `S` (Set), `R` (Reset) verbunden mit den SubApp-Eingängen `SET` und `RESET`.
            - Ausgang `EO` triggert den Hardware-Schreibvorgang und den Event-Switch.
        - **Datenausgang/-eingang**: 
            - `Q` speichert den aktuellen Status (Ein/Aus).

    - **QX**: logiBUS::io::DQ::logiBUS_QX
        - **Typ**: LogiBUS Digital Output Treiber
        - **Parameter**: `QI` = TRUE (Qualitätsindikator aktiviert)
        - **Ereignisausgang/-eingang**: 
            - `REQ` getriggert durch `E_SR.EO`.
        - **Datenausgang/-eingang**: 
            - `Output`: Erhält die Adresse/ID des Ausgangs vom SubApp-Eingang `Output`.
            - `OUT`: Erhält den Schaltzustand von `E_SR.Q`.

    - **E_SWITCH**: iec61499::events::E_SWITCH
        - **Typ**: Ereignis-Weiche (Switch)
        - **Parameter**: Keine.
        - **Ereignisausgang/-eingang**: 
            - `EI` (Event Input) verbunden mit `E_SR.EO`.
            - `EO1` (Event Output 1) verbunden mit dem SubApp-Ausgang `EO1`.
        - **Datenausgang/-eingang**: 
            - `G` (Gate) verbunden mit `E_SR.Q`.

- **Funktionsweise**:
    Der interne Ablauf koordiniert das Speichern des Zustands, das Schreiben auf die Hardware und das bedingte Weiterleiten eines Bestätigungs-Events.

## Programmablauf und Verbindungen

Der Baustein `Uebung_026_sub` verhält sich wie folgt:

1.  **Eingangsverarbeitung (SET/RESET)**:
    -   Das SubApp verfügt über zwei Ereigniseingänge: `SET` und `RESET`.
    -   Diese sind direkt mit dem internen `E_SR` Baustein verbunden. Ein `SET`-Event setzt den internen Zustand `Q` auf TRUE, ein `RESET`-Event setzt ihn auf FALSE.

2.  **Hardware-Ansteuerung**:
    -   Jede Änderung am `E_SR` Baustein (sowohl Setzen als auch Rücksetzen) löst ein Event (`EO`) aus.
    -   Dieses Event triggert den `QX` Baustein (`REQ`), welcher den aktuellen Zustand (`Q`) auf den physikalischen Ausgang schreibt.
    -   Der spezifische Hardware-Ausgang wird über die Datenvariable `Output` (Typ: `logiBUS_DO_S`) definiert, die von außen an die SubApp angelegt wird.

3.  **Ausgangs-Signalisierung (EO1)**:
    -   Parallel zur Hardware-Ansteuerung wird das Ereignis an den `E_SWITCH` geleitet.
    -   Der `E_SWITCH` prüft den aktuellen Zustand `Q` (Gate `G`).
    -   **Wenn Q = TRUE** (Ausgang wurde eingeschaltet): Das Event wird an `EO1` durchgeleitet. Dies signalisiert nach außen, dass der Aktor aktiviert wurde.
    -   **Wenn Q = FALSE** (Ausgang wurde ausgeschaltet): Das Event würde intern an `EO0` gehen, welcher jedoch nicht verbunden ist. Das bedeutet, das Ausschalten des Aktors erzeugt **kein** Event am Ausgang `EO1` der SubApp.

## Zusammenfassung

Die `Uebung_026_sub` ist ein gekapselter Funktionsblock zur Steuerung eines digitalen Ausgangs mit Speicherverhalten. Er vereinfacht die Ansteuerung, indem er die Hardware-Kommunikation (`QX`) und die Logik (`E_SR`) verbindet. Eine Besonderheit ist der Ausgang `EO1`, der nur dann feuert, wenn der Ausgang erfolgreich auf "Ein" (TRUE) gesetzt wurde, was ihn ideal für Ablaufketten macht, die auf die Aktivierung eines Aktors warten.