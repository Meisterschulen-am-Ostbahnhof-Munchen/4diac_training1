Hier ist die Dokumentation für die Übung `Uebung_003a_sub` basierend auf den bereitgestellten XML-Daten.

# Uebung_003a_sub

![Bild der Übung, falls vorhanden](uebung_003a_sub_screenshot.png)

* * * * * * * * * *

## Einleitung
Die Sub-Applikation **Uebung_003a_sub** stellt eine generische Verbindung zwischen einem Eingang und einem Ausgang her. Sie dient dazu, den Status eines digitalen Eingangs (IX) direkt auf einen digitalen Ausgang (QX) zu spiegeln. Dieser Baustein ist so konzipiert, dass er parametrierbar ist und somit verschiedene Hardware-Eingänge auf Hardware-Ausgänge mappen kann (logiBUS System).

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Applikation werden spezifische Bausteine zur Interaktion mit dem logiBUS E/A-System verwendet.

### Sub-Bausteine: Uebung_003a_sub (Internes Netzwerk)

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **Bausteinname**: IX
        - **Typ**: `logiBUS::io::DI::logiBUS_IX`
        - **Parameter**: 
            - `QI` = TRUE
            - `PARAMS` = "" (leerer String)
        - **Dateneingang**: `Input` (Verbunden mit der externen Variable der SubApp zur Auswahl des Hardware-Eingangs)
    
    - **Bausteinname**: QX
        - **Typ**: `logiBUS::io::DQ::logiBUS_QX`
        - **Parameter**: 
            - `QI` = TRUE
            - `PARAMS` = "" (leerer String)
        - **Dateneingang**: `Output` (Verbunden mit der externen Variable der SubApp zur Auswahl des Hardware-Ausgangs)

- **Funktionsweise**: 
    Der interne Ablauf basiert auf zwei Hauptkomponenten: dem Eingangsbaustein `IX` und dem Ausgangsbaustein `QX`. 
    Der `IX`-Baustein liest den physikalischen Zustand des durch die Variable `Input` definierten Eingangs. Sobald dieser gelesen wurde, wird der Wert an den `QX`-Baustein weitergegeben, der diesen Zustand auf den durch die Variable `Output` definierten physikalischen Ausgang schreibt.

## Programmablauf und Verbindungen

Der Programmablauf innerhalb der Sub-Applikation ist ereignisgesteuert und folgt einer direkten Weiterleitungslogik:

1.  **Initialisierung**: Beide Bausteine (`IX` und `QX`) werden mit `QI = TRUE` initialisiert, was bedeutet, dass sie standardmäßig aktiviert sind.
2.  **Signalverarbeitung**:
    - **Ereignisverbindung**: Der Ausgang `IND` (Indication) des Bausteins `IX` ist mit dem Eingang `REQ` (Request) des Bausteins `QX` verbunden. Das bedeutet, sobald der Eingang ein neues Signal oder einen Statusupdate meldet, wird sofort die Anforderung an den Ausgang gesendet, diesen Status zu übernehmen.
    - **Datenverbindung**: Der Datenausgang `IN` (der aktuelle Wert des Eingangs) von `IX` ist direkt mit dem Dateneingang `OUT` (der zu setzende Wert des Ausgangs) von `QX` verbunden.

**Zusätzliche Informationen zur Nutzung:**
- **Schnittstellen**:
    - `Input`: Typ `logiBUS_DI_S` – Identifiziert den zu lesenden Hardware-Eingang (z.B. Input_I1..I8).
    - `Output`: Typ `logiBUS_DO_S` – Identifiziert den zu schreibenden Hardware-Ausgang (z.B. Output_Q1..Q8).
- **Lernziel**: Verständnis der direkten Kopplung von Prozessabbildern (Eingang auf Ausgang) innerhalb der IEC 61499 / 4diac Umgebung unter Verwendung proprietärer E/A-Bibliotheken (logiBUS).

## Zusammenfassung
Die `Uebung_003a_sub` ist ein grundlegender Baustein zur direkten Durchschaltung von Signalen. Sie abstrahiert die Logik "Lese Eingang X und schreibe auf Ausgang Y" in eine wiederverwendbare Sub-Applikation. Durch die Verbindung von `IX.IND` auf `QX.REQ` und `IX.IN` auf `QX.OUT` wird sichergestellt, dass jede Änderung am Eingang unmittelbar am Ausgang reflektiert wird.