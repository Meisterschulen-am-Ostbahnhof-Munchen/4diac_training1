Hier ist die Dokumentation für die Übung `Uebung_003c_sub` basierend auf den bereitgestellten XML-Daten.

# Uebung_003c_sub

<Bild der Übung, falls vorhanden>

* * * * * * * * * *

## Einleitung
Die Sub-Application **Uebung_003c_sub** dient als generischer Baustein, um digitale Eingangssignale (Input IX) auf entsprechende Auxiliary-Ausgänge (QX) zu mappen. Sie fungiert als Brücke zwischen der LogiBUS-Eingangslogik und der ISOBUS-Ausgabelogik. Der Hauptzweck ist die Weiterleitung eines digitalen Zustands von einer Hardware-Eingangsquelle an eine definierte Hilfsfunktion (Auxiliary Function).

## Verwendete Funktionsbausteine (FBs)

Diese Sub-Application nutzt intern spezifische Bausteine zur Signalverarbeitung und Weiterleitung.

### Sub-Bausteine: Interne Logik
Da es sich hierbei um einen `SubAppType` handelt, besteht das Netzwerk aus verschalteten Basis-Funktionsbausteinen.

- **Typ**: Sub-Application Netzwerk
- **Verwendete interne FBs**:

    - **IX**: `logiBUS::io::DI::logiBUS_IX`
        - **Beschreibung**: Dieser Baustein extrahiert ein einzelnes digitales Signal aus dem LogiBUS-Eingangsstrom.
        - **Parameter**: 
            - `QI` = `TRUE` (Baustein ist standardmäßig aktiviert)
            - `PARAMS` = "" (Leer/Unsichtbar)
        - **Dateneingang**: 
            - `Input` (Verbunden mit dem externen Eingang `Input`)
        - **Datenausgang**: 
            - `IN` (Der aktuelle Zustand des Eingangs)
        - **Ereignisausgang**: 
            - `IND` (Indication - signalisiert eine Änderung oder Aktualisierung des Wertes)

    - **QX**: `isobus::UT::io::Auxiliary::OUT::Aux_QX`
        - **Beschreibung**: Dieser Baustein ist für die Ansteuerung eines Auxiliary-Ausgangs im ISOBUS-System zuständig.
        - **Parameter**: 
            - `QI` = `TRUE`
        - **Dateneingang**: 
            - `OUT` (Der zu schreibende Wert, kommt von `IX.IN`)
            - `iInpNr` (Nummer des Auxiliary-Arrays, verbunden mit dem externen Eingang `iInpNr`)
        - **Ereigniseingang**: 
            - `REQ` (Request - fordert das Schreiben des Ausgangs an)

## Programmablauf und Verbindungen

Der Ablauf innerhalb dieser Sub-Application ist ereignisgesteuert und linear:

1.  **Initialisierung**: Beide internen Bausteine (`IX` und `QX`) sind durch den Parameter `QI = TRUE` dauerhaft aktiviert.
2.  **Signaleingang**: Über die Schnittstelle der Sub-Application wird eine `Input`-Variable (Typ `logiBUS_DI_S`) an den Baustein **IX** übergeben. Zusätzlich wird über `iInpNr` festgelegt, welcher Auxiliary-Ausgang angesprochen werden soll.
3.  **Verarbeitung**:
    - Der Baustein **IX** liest den Zustand des Eingangs.
    - Sobald **IX** ein Signal verarbeitet hat, löst er das Ereignis `IND` aus.
    - Der digitale Zustand (TRUE/FALSE) wird am Ausgang `IN` von **IX** bereitgestellt.
4.  **Signalweiterleitung**:
    - Das Ereignis `IND` von **IX** ist direkt mit dem Ereignis `REQ` von **QX** verbunden. Das bedeutet, jede Aktualisierung des Eingangs triggert sofort den Ausgangsbaustein.
    - Die Datenverbindung leitet den Wert von `IX.IN` direkt an `QX.OUT` weiter.
5.  **Ausgabe**: Der Baustein **QX** schreibt den empfangenen Wert auf den durch `iInpNr` definierten Auxiliary-Ausgang.

**Anwendungsbereich:**
Diese Übung demonstriert die Kapselung von Logik. Anstatt `IX` und `QX` jedes Mal manuell zu verbinden, kann dieser Sub-App-Baustein instanziiert werden, um schnell einen Eingang auf einen Ausgang zu routen.

## Zusammenfassung
Die `Uebung_003c_sub` ist ein modularer Baustein zur direkten Durchleitung eines digitalen LogiBUS-Eingangs auf einen ISOBUS-Auxiliary-Ausgang. Durch die Parametrierung über `iInpNr` ist der Baustein flexibel für verschiedene Ausgänge wiederverwendbar.