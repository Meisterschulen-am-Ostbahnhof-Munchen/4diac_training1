# Uebung_003c: DigitalInput_I1-2-3-4 auf AUX

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale (I1-I4) auf Ausgänge des Auxiliary-Bereichs. Die Übung zeigt eine strukturierte Anwendung von Sub-Applikationen zur Signalverarbeitung in der 4diac-IDE.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_003c_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: logiBUS_IX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: IND → REQ (QX)
        - Datenausgang/-eingang: IN → OUT (QX), Input (extern) → Input (IX)
    - **QX**: Aux_QX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: REQ (von IX.IND)
        - Datenausgang/-eingang: OUT (von IX.IN), iInpNr (extern) → iInpNr (QX)
- **Funktionsweise**: Der Baustein verarbeitet ein digitales Eingangssignal über den IX-Baustein und leitet es an den entsprechenden Auxiliary-Ausgang (QX) weiter. Der Parameter iInpNr definiert die Nummer des Auxiliary-Ausgangs.

## Programmablauf und Verbindungen
Die Hauptapplikation besteht aus vier identischen Sub-Applikationen (F1-F4), die jeweils folgende Konfiguration aufweisen:

- **F1**: Verarbeitet Input_I1 auf Auxiliary-Ausgang 0 (iInpNr=0)
- **F2**: Verarbeitet Input_I2 auf Auxiliary-Ausgang 1 (iInpNr=1)
- **F3**: Verarbeitet Input_I3 auf Auxiliary-Ausgang 2 (iInpNr=2)
- **F4**: Verarbeitet Input_I4 auf Auxiliary-Ausgang 3 (iInpNr=3)

**Lernziele**:
- Verständnis der Signalverarbeitung von digitalen Eingängen zu Auxiliary-Ausgängen
- Arbeit mit parametrisierbaren Sub-Applikationen
- Umgang mit dem logiBUS-System in 4diac

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**:
- Grundlagen der 4diac-IDE
- Verständnis von digitalen Ein- und Ausgängen
- Basiswissen über Funktionsbausteine und Sub-Applikationen

**Starten der Übung**: Die Übung wird in der 4diac-IDE geladen und auf einen kompatiblen IEC 61499-Laufzeitcontainer deployed.

## Zusammenfassung
Diese Übung verdeutlicht eine grundlegende Signalverarbeitungskette von digitalen Eingängen zu Auxiliary-Ausgängen. Durch die Verwendung von parametrisierbaren Sub-Applikationen wird eine wiederverwendbare und skalierbare Lösung präsentiert, die das Verständnis für modulare Programmierung in IEC 61499 fördert.