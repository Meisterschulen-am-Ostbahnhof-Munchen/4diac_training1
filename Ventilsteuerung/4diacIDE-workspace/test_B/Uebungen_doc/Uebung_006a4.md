# Uebung_006a4: SR und T-Flip-Flop mit 3x IE

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Anwendung von SR- und T-Flip-Flop-Funktionalität mit drei Eingängen. Die Übung zeigt die Steuerung einer Links-/Rechtslauf-Steuerung unter Verwendung von logiBUS-Komponenten für Ein- und Ausgänge.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_CLK_I1**, **DigitalInput_CLK_I2**, **DigitalInput_CLK_I3** (Typ: logiBUS_IE)
- **E_T_FF_SR** (Typ: E_T_FF_SR)
- **LinksRechts** (Typ: LinksRechts)
- **Rechtslauf**, **Linkslauf** (Typ: logiBUS_QX)

### Sub-Bausteine: LinksRechts
- **Typ**: LinksRechts
- **Verwendete interne FBs**: Nicht in der bereitgestellten XML definiert
- **Funktionsweise**: Steuert die Richtungsauswahl zwischen Links- und Rechtslauf basierend auf dem Eingangssignal

## Programmablauf und Verbindungen

### Ereignisverbindungen:
- DigitalInput_CLK_I1.IND → E_T_FF_SR.S (Set-Eingang)
- DigitalInput_CLK_I2.IND → E_T_FF_SR.R (Reset-Eingang)
- DigitalInput_CLK_I3.IND → E_T_FF_SR.CLK (Takt-Eingang)
- E_T_FF_SR.EO → LinksRechts.EI_ON (Einschaltereignis)
- LinksRechts.EO → Rechtslauf.REQ und Linkslauf.REQ (Aktivierung der Ausgänge)

### Datenverbindungen:
- LinksRechts.Rechts → Rechtslauf.OUT (Rechtslauf-Steuerung)
- E_T_FF_SR.Q → LinksRechts.EIN (Eingangssignal)
- LinksRechts.Links → Linkslauf.OUT (Linkslauf-Steuerung)

### Eingangskonfiguration:
- I1: Direkter Eingang (EType := 255)
- I2 und I3: Einzelklick-Button-Ereignisse

### Lernziele:
- Verständnis von SR- und T-Flip-Flop-Verhalten
- Umgang mit Ereignisgesteuerten Eingängen
- Steuerung von Richtungsauswahl mit Flip-Flops
- Anwendung von logiBUS-IE und logiBUS-QX Komponenten

### Schwierigkeitsgrad: Mittel
### Benötigte Vorkenntnisse: Grundlagen der Flip-Flop-Schaltungen, Ereignissteuerung in IEC 61499

## Zusammenfassung
Diese Übung verbindet Flip-Flop-Grundlagen mit praktischer Anwendung in einer Richtungssteuerung. Die Kombination aus SR- und T-Flip-Flop-Eigenschaften mit drei unabhängigen Eingängen ermöglicht ein umfassendes Verständnis von sequentiellen Schaltungen und deren Anwendung in steuerungstechnischen Aufgaben. Die Übung zeigt zudem die Integration von Hardware-Ein-/Ausgängen über das logiBUS-System.