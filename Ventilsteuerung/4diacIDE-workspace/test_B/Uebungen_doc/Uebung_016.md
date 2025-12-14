# Uebung_016: Background Colour umschalten

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung der Hintergrundfarbe eines HMI-Elements durch Softkey-Bedienung. Mittels zweier Funktionstasten kann zwischen zwei verschiedenen Hintergrundfarben umgeschaltet werden.

## Verwendete Funktionsbausteine (FBs)

### Softkey_IE
- **Typ**: Eingabebaustein für Softkeys
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::SoftKey_F1/F2 (definiert die verwendeten Softkeys)
  - InputEvent = SoftKeyActivationCode::SK_RELEASED (reagiert auf Tastenloslassen)

### E_SR
- **Typ**: Set-Reset-Flipflop
- **Funktionsweise**: Speichert den Zustand und gibt ihn über den Q-Ausgang aus

### F_SEL
- **Typ**: Multiplexer/Selektor
- **Parameter**:
  - IN0 = colours::COLOR_WHITE
  - IN1 = colours::COLOR_GREEN
- **Funktionsweise**: Wählt zwischen zwei Eingangswerten basierend auf dem Steuersignal G

### Q_BackgroundColour
- **Typ**: Ausgabebaustein für Hintergrundfarbe
- **Parameter**:
  - u16ObjId = DefaultPool::SoftKey_F7 (definiert das zu beeinflussende HMI-Element)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → E_SR.S (Setzt das Flipflop)
- SoftKey_UP_F2.IND → E_SR.R (Rücksetzt das Flipflop)
- E_SR.EO → F_SEL.REQ (Trigger für Selektor)
- F_SEL.CNF → Q_BackgroundColour.REQ (Trigger für Farbausgabe)

**Datenverbindungen:**
- E_SR.Q → F_SEL.G (Steuersignal für Selektor)
- F_SEL.OUT → Q_BackgroundColour.u8Colour (Farbwert an Ausgabebaustein)

**Programmablauf:**
1. Drücken und Loslassen von F1 setzt das Flipflop (E_SR.Q = TRUE)
2. Drücken und Loslassen von F2 resetet das Flipflop (E_SR.Q = FALSE)
3. Der Flipflop-Zustand steuert den F_SEL-Baustein
4. Bei TRUE wird GRÜN, bei FALSE wird WEISS ausgewählt
5. Die gewählte Farbe wird an den Hintergrund des definierten HMI-Elements ausgegeben

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der HMI-Steuerung in 4diac, insbesondere die Verwendung von Softkeys zur Zustandssteuerung und die dynamische Änderung von Anzeigeeigenschaften. Sie zeigt die Kombination von Flipflops, Selektoren und Ausgabebausteinen für einfache Benutzerinteraktionen.