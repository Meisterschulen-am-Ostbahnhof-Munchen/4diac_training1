# Uebung_010c2: SoftKey_F1 auf DigitalOutput_Q1 mit GreenWhiteBackground mit Subapp

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verknüpfung einer Softkey-Funktion mit einer digitalen Ausgabe unter Verwendung einer Hintergrundsubapplikation. Die Übung zeigt, wie ein Tastendruck auf die F1-Taste sowohl eine digitale Ausgabe steuert als auch eine visuelle Rückmeldung auf der Benutzeroberfläche erzeugt.

## Verwendete Funktionsbausteine (FBs)

### Haupt-FBs:
- **SoftKey_F1** (Typ: Softkey_IX) - Erfasst den Tastendruck der F1-Taste
- **DigitalOutput_Q1** (Typ: logiBUS_QX) - Steuert den digitalen Ausgang Q1
- **GreenWhiteBackground** (Typ: GreenWhiteBackground) - Subapplikation für visuelle Hintergrunddarstellung

### Sub-Bausteine: GreenWhiteBackground
- **Typ**: GreenWhiteBackground
- **Verwendete interne FBs**: Keine weiteren internen FBs angegeben
- **Funktionsweise**: Diese Subapplikation dient zur visuellen Darstellung mit grün-weißem Hintergrund und empfängt Daten vom Softkey-Baustein zur Anzeige des Tastenzustands.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_F1.IND → GreenWhiteBackground.REQ
- SoftKey_F1.IND → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- SoftKey_F1.IN → GreenWhiteBackground.DI1
- SoftKey_F1.IN → DigitalOutput_Q1.OUT
- u16ObjId (Eingangsvariable) → SoftKey_F1.u16ObjId
- u16ObjId (Eingangsvariable) → GreenWhiteBackground.u16ObjId
- Output (Eingangsvariable) → DigitalOutput_Q1.Output

**Parameterkonfiguration:**
- Beide Haupt-FBs (SoftKey_F1 und DigitalOutput_Q1) haben QI-Parameter auf TRUE gesetzt
- Initialwerte: u16ObjId = SoftKey_F1, Output = Output_Q1

**Lernziele:**
- Verständnis der Ereignis- und Datenverbindungen zwischen Funktionsbausteinen
- Umgang mit Subapplikationen für visuelle Darstellung
- Steuerung digitaler Ausgänge über Softkey-Eingaben

**Schwierigkeitsgrad**: Einfach
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Verbindungen

## Zusammenfassung
Diese Übung verdeutlicht die grundlegende Verknüpfung von Eingabe-, Verarbeitungs- und Ausgabekomponenten in einem IEC 61499-System. Durch die parallele Ansteuerung einer digitalen Ausgabe und einer visuellen Subapplikation wird das Konzept der ereignisgesteuerten Automatisierung praxisnah demonstriert. Die Übung eignet sich ideal für den Einstieg in die Verwendung von Softkeys und digitalen Ausgängen in kombinierten Anwendungen.