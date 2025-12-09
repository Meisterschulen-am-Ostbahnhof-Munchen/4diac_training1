# Uebung_010c3: SoftKey_F1 auf DigitalOutput_Q1 mit GreenWhiteBackground mit Typed Subapp

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung einer typisierten Subapplikation zur Steuerung eines digitalen Ausgangs über eine Softkey-Funktion. Die Anwendung verbindet einen Softkey mit einem digitalen Ausgang und einem Hintergrundanzeigeelement.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_010c3_sub
- **Typ**: Uebung_010c3_sub
- **Verwendete interne FBs**:
    - **SoftKey_F1**: Softkey_IX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: IND → REQ (DigitalOutput_Q1, GreenWhiteBackground)
        - Datenausgang/-eingang: IN → OUT (DigitalOutput_Q1), IN → DI1 (GreenWhiteBackground)
    
    - **DigitalOutput_Q1**: logiBUS_QX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: REQ (von SoftKey_F1.IND)
        - Datenausgang/-eingang: OUT (von SoftKey_F1.IN)
    
    - **GreenWhiteBackground**: GreenWhiteBackground
        - Parameter: Keine
        - Ereignisausgang/-eingang: REQ (von SoftKey_F1.IND)
        - Datenausgang/-eingang: DI1 (von SoftKey_F1.IN)

- **Funktionsweise**: Die Subapplikation empfängt die Objekt-ID und Ausgangskonfiguration als Eingangsparameter. Bei Betätigung des Softkeys F1 wird sowohl der digitale Ausgang Q1 als auch die Hintergrundanzeige angesteuert.

## Programmablauf und Verbindungen

**Lernziele:**
- Verwendung typisierter Subapplikationen
- Parametrierung von Funktionsbausteinen
- Ereignis- und Datenverbindungen zwischen FBs
- Integration von Softkey- und Ausgangssteuerung

**Schwierigkeitsgrad:** Einfach

**Benötigte Vorkenntnisse:**
- Grundkenntnisse der 4diac-IDE
- Verständnis von Funktionsbausteinen und Subapplikationen
- Kenntnisse über Ereignis- und Datenverbindungen

**Start der Übung:**
Die Übung wird durch die Haupt-Subapplikation Uebung_010c3 gestartet, welche die parametrierte Subapplikation Uebung_010c3_sub instanziiert. Die Parameterübergabe erfolgt mit:
- u16ObjId: "DefaultPool::SoftKey_F1"
- Output: "logiBUS_DO::Output_Q1"

**Verbindungen:**
- SoftKey_F1.IND → DigitalOutput_Q1.REQ (Ereignisverbindung)
- SoftKey_F1.IND → GreenWhiteBackground.REQ (Ereignisverbindung)
- SoftKey_F1.IN → DigitalOutput_Q1.OUT (Datenverbindung)
- SoftKey_F1.IN → GreenWhiteBackground.DI1 (Datenverbindung)
- Eingangsparameter werden an die entsprechenden FBs weitergeleitet

## Zusammenfassung
Diese Übung zeigt eine typische Anwendung zur Softkey-Steuerung mit paralleler Ausgangs- und Anzeigeaktivierung. Die Verwendung einer typisierten Subapplikation ermöglicht eine klare Strukturierung und Wiederverwendbarkeit der Funktionalität. Die Parametrierung über die übergeordnete Applikation macht die Subapplikation flexibel einsetzbar für verschiedene Softkey- und Ausgangskonfigurationen.