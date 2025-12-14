# Uebung_020h: DigitalInput_I1 auf DigitalOutput_Q1; E_PULSE; Impulsformend

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung von Impulsformern in der Automatisierungstechnik. Ein digitaler Eingang wird über einen E_PULSE-Baustein verarbeitet, um einen zeitlich begrenzten Ausgangsimpuls zu erzeugen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK
- **Funktion**: Erfasst digitale Eingangssignale und erkennt spezifische Ereignisse wie Tastenklicks

### E_PULSE
- **Typ**: E_PULSE
- **Parameter**:
  - PT = T#5S (5 Sekunden Impulsdauer)
- **Funktion**: Erzeugt einen Impuls mit definierter Zeitdauer bei Auslösung

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE
  - Output = logiBUS_DO::Output_Q1
- **Funktion**: Steuert digitale Ausgänge an

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I1.IND → E_PULSE.REQ
- E_PULSE.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_PULSE.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Bei einem Tastenklick an Eingang I1 wird das IND-Ereignis ausgelöst
2. Dies startet den E_PULSE-Baustein über REQ
3. E_PULSE erzeugt einen 5-Sekunden-Impuls an seinem Q-Ausgang
4. Der Impuls wird an den Digitalausgang Q1 weitergeleitet
5. Der Ausgang Q1 bleibt für genau 5 Sekunden aktiv

**Lernziele:**
- Verwendung von Impulsformern (E_PULSE)
- Ereignisgesteuerte Programmabläufe
- Zeitgesteuerte Ausgangssteuerung
- Verbindung von digitalen Ein- und Ausgängen

**Schwierigkeitsgrad**: Einfach
**Vorkenntnisse**: Grundlagen der 4diac-IDE und digitale Ein-/Ausgänge

## Zusammenfassung
Die Übung zeigt eine grundlegende Impulsformer-Schaltung, bei der ein Tastendruck an Eingang I1 einen genau 5 Sekunden langen Impuls an Ausgang Q1 erzeugt. Dies ist eine typische Anwendung für zeitgesteuerte Steuerungsaufgaben in der Automatisierungstechnik.