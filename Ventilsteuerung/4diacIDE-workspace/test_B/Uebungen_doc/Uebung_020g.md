# Uebung_020g: DigitalInput_I1 auf DigitalOutput_Q1; E_TONOF; Ein-/Ausschaltverzögert

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines ein-/ausschaltverzögerten Zeitglieds (E_TONOF) zur Steuerung eines digitalen Ausgangs basierend auf einem digitalen Eingangssignal. Der Funktionsbaustein E_TONOF sorgt dafür, dass das Ausgangssignal sowohl beim Einschalten als auch beim Ausschalten mit einer definierten Zeitverzögerung reagiert.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Funktionsweise**: Liest den Zustand eines digitalen Eingangs (Input_I1) vom logiBUS-System ein und stellt diesen als Daten- und Ereignissignal zur Verfügung.

### E_TONOF
- **Typ**: E_TONOF
- **Parameter**:
  - PT_ON: T#5S (Einschaltverzögerung: 5 Sekunden)
  - PT_OFF: T#5S (Ausschaltverzögerung: 5 Sekunden)
- **Funktionsweise**: Verzögert sowohl das Einschalten als auch das Ausschalten des Ausgangssignals um jeweils 5 Sekunden. Bei einer positiven Flanke am Eingang startet die Einschaltverzögerung, bei einer negativen Flanke die Ausschaltverzögerung.

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - Output: logiBUS_DO::Output_Q1
- **Funktionsweise**: Schreibt den empfangenen Signalzustand auf den digitalen Ausgang Q1 des logiBUS-Systems.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → E_TONOF.REQ
- E_TONOF.CNF → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → E_TONOF.IN
- E_TONOF.Q → DigitalOutput_Q1.OUT

**Ablauf:**
1. Beim Betätigen des Eingangs I1 wird ein Ereignis an E_TONOF gesendet
2. E_TONOF startet die Einschaltverzögerung von 5 Sekunden
3. Nach Ablauf der Verzögerung wird der Ausgang Q1 aktiviert
4. Beim Loslassen von I1 startet die Ausschaltverzögerung von 5 Sekunden
5. Nach Ablauf dieser Verzögerung wird Q1 deaktiviert

**Lernziele:**
- Verständnis von ein-/ausschaltverzögerten Zeitgliedern
- Umgang mit Zeitparametern in 4diac
- Verbindung von digitalen Ein- und Ausgängen über Zeitfunktionen

**Schwierigkeitsgrad**: Einsteiger

**Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von digitalen Ein-/Ausgängen

## Zusammenfassung
Diese Übung zeigt die praktische Anwendung des E_TONOF-Funktionsbausteins zur Realisierung von Ein- und Ausschaltverzögerungen. Durch die Konfiguration von jeweils 5 Sekunden Verzögerungszeit wird demonstriert, wie zeitgesteuerte Abläufe in Automatisierungsanwendungen implementiert werden können. Die Übung verbindet hardwarenahe Ein-/Ausgänge mit zeitbasierten Steuerungsfunktionen.