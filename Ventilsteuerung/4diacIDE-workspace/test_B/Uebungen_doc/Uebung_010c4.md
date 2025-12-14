# Uebung_010c4: SoftKey_F1/_F2 auf DigitalOutput_Q1/_Q2 mit GreenWhiteBackground mit Typed Subapp

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von Softkeys (F1/F2) zur Steuerung digitaler Ausgänge (Q1/Q2) mit einer GreenWhiteBackground-Funktionalität unter Verwendung von typisierten Subapplikationen. Die Übung zeigt die Verknüpfung von Benutzereingaben über Softkeys mit physischen Ausgängen und visuellen Rückmeldungen.

## Verwendete Funktionsbausteine (FBs)

### Sub-Bausteine: Uebung_010c4_sub
- **Typ**: Uebung_010c4_sub
- **Verwendete interne FBs**:
    - **SoftKey_F1**: Softkey_IX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: IND → GreenWhiteBackground.REQ, DigitalOutput_Q1.REQ
        - Datenausgang/-eingang: IN → GreenWhiteBackground.DI1, DigitalOutput_Q1.OUT
    - **DigitalOutput_Q1**: logiBUS_QX
        - Parameter: QI = TRUE
        - Ereignisausgang/-eingang: REQ (von SoftKey_F1.IND)
        - Datenausgang/-eingang: OUT (von SoftKey_F1.IN)
    - **GreenWhiteBackground**: GreenWhiteBackground
        - Parameter: Keine
        - Ereignisausgang/-eingang: REQ (von SoftKey_F1.IND)
        - Datenausgang/-eingang: DI1 (von SoftKey_F1.IN)
- **Funktionsweise**: Der Sub-Baustein verbindet einen Softkey-Input mit einem digitalen Ausgang und einer Hintergrundvisualisierung. Bei Betätigung des Softkeys wird sowohl der digitale Ausgang geschaltet als auch eine visuelle Rückmeldung über den GreenWhiteBackground gegeben.

## Programmablauf und Verbindungen
Die Hauptapplikation verwendet zwei Instanzen des Sub-Bausteins Uebung_010c4_sub:
- Uebung_010c4_sub: Verknüpft SoftKey_F1 mit DigitalOutput_Q1
- Uebung_010c4_sub_1: Verknüpft SoftKey_F2 mit DigitalOutput_Q2

**Parameterkonfiguration:**
- u16ObjId-Parameter: Definiert die Objekt-ID (DefaultPool::SoftKey_F1 bzw. DefaultPool::SoftKey_F2)
- Output-Parameter: Spezifiziert den digitalen Ausgang (logiBUS_DO::Output_Q1 bzw. logiBUS_DO::Output_Q2)

**Ereignisverbindungen:**
- SoftKey_F1.IND → GreenWhiteBackground.REQ
- SoftKey_F1.IND → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- SoftKey_F1.IN → GreenWhiteBackground.DI1
- SoftKey_F1.IN → DigitalOutput_Q1.OUT
- u16ObjId → SoftKey_F1.u16ObjId
- u16ObjId → GreenWhiteBackground.u16ObjId
- Output → DigitalOutput_Q1.Output

**Lernziele:**
- Verwendung typisierter Subapplikationen
- Parametrierung von Funktionsbausteinen
- Verknüpfung von Softkeys mit digitalen Ausgängen
- Implementierung visueller Rückmeldungen
- Daten- und Ereignisverbindungen zwischen FBs

**Schwierigkeitsgrad**: Einsteiger

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Subapplikationen

**Starten der Übung**: Die Übung wird in der 4diac-IDE geladen und auf ein kompatibles Steuerungssystem deployt. Die Softkeys F1/F2 können über die Benutzeroberfläche betätigt werden.

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung zur Steuerung digitaler Ausgänge über Softkeys mit integrierter visueller Rückmeldung. Die Verwendung typisierter Subapplikationen ermöglicht eine wiederverwendbare und strukturierte Programmarchitektur. Die Übung vermittelt grundlegende Konzepte der Ereignisverarbeitung und Datenverbindungen in IEC 61499-basierten Steuerungssystemen.