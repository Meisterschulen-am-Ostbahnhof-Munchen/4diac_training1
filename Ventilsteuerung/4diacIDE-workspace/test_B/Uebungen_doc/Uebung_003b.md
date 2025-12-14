# Uebung_003b: DigitalInput_I1-2-3-4 auf DigitalOutput_Q1-2-3-4

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung von digitalen Eingängen mit digitalen Ausgängen in einer 4diac-IDE Anwendung. Es werden vier unabhängige Signalwege von Eingängen I1-I4 zu Ausgängen Q1-Q4 realisiert, wobei jeder Signalweg durch einen eigenen Sub-App-Baustein abgebildet wird.

## Verwendete Funktionsbausteine (FBs)

### Hauptbaustein: Uebung_003b
- **Typ**: SubAppType
- **Funktion**: Enthält vier Instanzen des Sub-Bausteins Uebung_003b_sub, die jeweils einen Eingang mit einem Ausgang verbinden

### Sub-Bausteine: Uebung_003b_sub
- **Typ**: SubAppType
- **Verwendete interne FBs**:
  - **logiBUS_IX**: Digitaler Eingangsbaustein
    - Parameter: QI = TRUE (aktiviert)
    - Ereignisausgang: IND (Input Data Change)
    - Datenausgang: IN (Eingangswert)
  
  - **logiBUS_QX**: Digitaler Ausgangsbaustein
    - Parameter: QI = TRUE (aktiviert)
    - Ereigniseingang: REQ (Request to update output)
    - Dateneingang: OUT (Ausgangswert)

- **Funktionsweise**: 
  - Der IX-Baustein überwacht den digitalen Eingang
  - Bei Zustandsänderung am Eingang (IND-Event) wird der QX-Baustein aktiviert (REQ-Event)
  - Der Eingangswert wird direkt an den Ausgang weitergeleitet

## Programmablauf und Verbindungen

**Signalwege:**
- F1: Input_I1 → Output_Q1
- F2: Input_I2 → Output_Q2  
- F3: Input_I3 → Output_Q3
- F4: Input_I4 → Output_Q4

**Ereignisverbindungen:**
- IX.IND → QX.REQ (bei Zustandsänderung am Eingang wird Ausgang aktualisiert)

**Datenverbindungen:**
- IX.IN → QX.OUT (direkte Wertübertragung)
- Input-Parameter → IX.Input (Eingangskonfiguration)
- Output-Parameter → QX.Output (Ausgangskonfiguration)

**Lernziele:**
- Verständnis der grundlegenden E/A-Verknüpfung
- Arbeit mit logiBUS-Schnittstellenbausteinen
- Parametrierung von Sub-App-Bausteinen
- Aufbau modularer Applikationen mit wiederverwendbaren Komponenten

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis digitaler Ein- und Ausgänge

**Starten der Übung**: Nach dem Laden der Applikation in der 4diac-IDE kann diese auf ein kompatibles Steuerungssystem deployed werden. Die digitalen Eingänge I1-I4 steuern direkt die entsprechenden Ausgänge Q1-Q4.

## Zusammenfassung
Diese Übung vermittelt die grundlegende Prinzipien der Signalverarbeitung in 4diac-IDE durch direkte Verknüpfung von digitalen Eingängen mit Ausgängen. Die modulare Struktur mit wiederverwendbaren Sub-Bausteinen zeigt best practices für skalierbare Applikationsentwicklung. Jeder der vier identischen Signalwege demonstriert die unabhängige Verarbeitung paralleler E/A-Kanäle.