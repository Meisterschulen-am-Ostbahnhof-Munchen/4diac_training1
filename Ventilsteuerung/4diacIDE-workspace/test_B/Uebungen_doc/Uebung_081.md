# Uebung_081: Beispiel für E_CTD

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_CTD-Funktionsbausteins (Counter Down) in einem 4diac-IDE-System. Die Übung implementiert einen Abwärtszähler mit Reset-Funktionalität und zeigt praktische Anwendungsmöglichkeiten für Zählfunktionen in der Automatisierungstechnik.

## Verwendete Funktionsbausteine (FBs)

### E_CTD (Counter Down)
- **Typ**: Standard IEC 61499-Funktionsbaustein
- **Parameter**: 
  - PV = UINT#5 (Voreinstellungswert auf 5)
- **Ereigniseingänge**: CD (Count Down), LD (Load)
- **Ereignisausgänge**: CDO (Count Down Output), LDO (Load Output)
- **Datenausgang**: Q (Ausgangswert)

### logiBUS_IE (Digital Input)
- **Typ**: logiBUS-Interface für digitale Eingänge
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_I1 bzw. Input_I2
  - InputEvent = BUTTON_SINGLE_CLICK
- **Ereignisausgang**: IND (Input Event)

### logiBUS_QX (Digital Output)
- **Typ**: logiBUS-Interface für digitale Ausgänge
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1
- **Ereigniseingang**: REQ (Request)
- **Dateneingang**: OUT (Output Value)

## Programmablauf und Verbindungen

Das Programm realisiert einen Abwärtszähler mit folgenden Funktionen:

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_CTD.CD (Zählereignis)
- DigitalInput_CLK_I2.IND → E_CTD.LD (Lade-/Reset-Ereignis)
- E_CTD.CDO → DigitalOutput_Q1.REQ (Zählerausgangsereignis)
- E_CTD.LDO → DigitalOutput_Q1.REQ (Ladeausgangsereignis)

**Datenverbindungen:**
- E_CTD.Q → DigitalOutput_Q1.OUT (Zählerwert zum Ausgang)

**Funktionsweise:**
- Bei Betätigung von Input_I1 wird der Zähler um 1 dekrementiert (CD-Eingang)
- Bei Betätigung von Input_I2 wird der Zähler auf den Voreinstellungswert 5 zurückgesetzt (LD-Eingang)
- Der aktuelle Zählerstand wird kontinuierlich an den digitalen Ausgang Q1 ausgegeben
- Der Zähler zählt von 5 abwärts bis 0

## Lernziele
- Verständnis des E_CTD-Funktionsbausteins
- Implementierung von Zählfunktionen in IEC 61499
- Verwendung von logiBUS-Schnittstellen für Ein-/Ausgänge
- Ereignisgesteuerte Programmierung

## Schwierigkeitsgrad
Einfach - geeignet für Einsteiger in die IEC 61499-Programmierung

## Vorkenntnisse
- Grundkenntnisse in 4diac-IDE
- Verständnis von Funktionsbausteinen und Ereignisverbindungen
- Basiswissen über digitale Ein-/Ausgänge

## Zusammenfassung
Diese Übung zeigt eine praktische Implementierung eines Abwärtszählers mit Reset-Funktion unter Verwendung des standardisierten E_CTD-Funktionsbausteins. Die Verbindung zwischen digitalen Eingängen, dem Zählerbaustein und dem digitalen Ausgang demonstriert grundlegende Prinzipien der ereignisgesteuerten Automatisierungstechnik nach IEC 61499.