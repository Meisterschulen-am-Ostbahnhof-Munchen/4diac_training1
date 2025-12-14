# Uebung_004a8: mit E_SPLIT_2

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert den Einsatz von T-Flip-Flops in Verbindung mit einem Ereignisverteiler (E_SPLIT_2). Das System steuert zwei digitale Ausgänge basierend auf Taktimpulsen von einem digitalen Eingang.

## Verwendete Funktionsbausteine (FBs)

### Hauptbausteine:
- **DigitalInput_CLK_I1** (logiBUS_IE): Digitaler Eingang für Taktgeber
- **E_SPLIT_2**: Ereignisverteiler für zwei Ausgänge
- **E_T_FF_Q1** und **E_T_FF_Q2** (E_T_FF): T-Flip-Flops für Ausgangssteuerung
- **DigitalOutput_Q1** und **DigitalOutput_Q2** (logiBUS_QX): Digitale Ausgänge

### Sub-Bausteine: E_T_FF (T-Flip-Flop)
- **Typ**: E_T_FF
- **Verwendete interne FBs**: Keine weiteren internen FBs angegeben
- **Funktionsweise**: Der T-Flip-Flop ändert seinen Ausgangszustand bei jedem eingehenden Taktimpuls (CLK-Ereignis). Bei aktivem Takt wechselt der Q-Ausgang zwischen TRUE und FALSE.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_SPLIT_2.EI
- E_SPLIT_2.EO1 → E_T_FF_Q1.CLK
- E_SPLIT_2.EO2 → E_T_FF_Q2.CLK
- E_T_FF_Q1.EO → DigitalOutput_Q1.REQ
- E_T_FF_Q2.EO → DigitalOutput_Q2.REQ

**Datenverbindungen:**
- E_T_FF_Q1.Q → DigitalOutput_Q1.OUT
- E_T_FF_Q2.Q → DigitalOutput_Q2.OUT

**Parameterkonfiguration:**
- DigitalInput_CLK_I1: InputEvent = BUTTON_SINGLE_CLICK
- Beide DigitalOutput-FBs: QI = TRUE

**Lernziele:**
- Verständnis von T-Flip-Flop-Verhalten
- Einsatz von Ereignisverteilern (E_SPLIT)
- Steuerung mehrerer Ausgänge mit einem Eingangssignal
- Umgang mit digitalen Ein- und Ausgängen in 4diac

**Schwierigkeitsgrad**: Einsteiger
**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Flip-Flops

**Start der Übung**: Das Programm wird durch Betätigen des mit I1 verbundenen Tasters gestartet. Bei jedem Tastendruck (SINGLE_CLICK) werden beide T-Flip-Flops getaktet.

## Zusammenfassung
Diese Übung zeigt eine einfache Anwendung von T-Flip-Flops zur Steuerung zweier unabhängiger Ausgänge mit einem gemeinsamen Taktsignal. Durch den Einsatz des E_SPLIT_2-Bausteins wird das Eingangssignal parallel auf beide Flip-Flops verteilt, was eine synchrone Steuerung ermöglicht. Die Übung vermittelt grundlegende Konzepte der sequentiellen Logik und Ereignisverteilung in 4diac-Systemen.