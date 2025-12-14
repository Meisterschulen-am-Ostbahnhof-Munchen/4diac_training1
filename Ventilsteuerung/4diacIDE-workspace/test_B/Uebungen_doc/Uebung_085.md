# Uebung_085: Beispiel für E_D_FF

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines D-Flip-Flops (E_D_FF) in der 4diac-IDE. Der Schwerpunkt liegt auf der Verwendung eines taktgesteuerten Speicherelements, das Daten an einem Taktflankenwechsel übernimmt. Die Übung zeigt die praktische Anwendung digitaler Schaltungen mit Ein- und Ausgängen über logiBUS-Schnittstellen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Funktionsweise**: Liest den Zustand eines digitalen Eingangs (Input_I1) und stellt diesen als Datenwert zur Verfügung

### DigitalInput_CLK_I2  
- **Typ**: logiBUS_IE
- **Funktionsweise**: Erkennt Takt-Ereignisse (BUTTON_SINGLE_CLICK) am Eingang I2 und generiert entsprechende Ereignisausgänge

### E_D_FF
- **Typ**: E_D_FF
- **Funktionsweise**: D-Flip-Flop Baustein, der den Datenwert am Eingang D bei einer steigenden Taktflanke am CLK-Eingang übernimmt und am Ausgang Q ausgibt

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Funktionsweise**: Schreibt den empfangenen Datenwert auf den digitalen Ausgang Q1

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_CLK_I2.IND → E_D_FF.CLK (Takt-Signal)
- E_D_FF.EO → DigitalOutput_Q1.REQ (Ausgabeanforderung)

**Datenverbindungen:**
- DigitalInput_I1.IN → E_D_FF.D (Dateneingang)
- E_D_FF.Q → DigitalOutput_Q1.OUT (Datenausgang)

**Funktionsweise:**
Der Zustand des Eingangs I1 wird kontinuierlich am D-Eingang des Flip-Flops bereitgestellt. Bei jedem Takt-Event (Einzelklick auf I2) wird dieser Zustand in den Flip-Flop übernommen und am Ausgang Q1 ausgegeben. Der Ausgang behält seinen Zustand bei, bis der nächste Taktimpuls eintrifft.

**Lernziele:**
- Verständnis der Funktionsweise eines D-Flip-Flops
- Umgang mit taktgesteuerten Speicherelementen
- Anwendung von Ereignis- und Datenverbindungen
- Praxis mit logiBUS Ein-/Ausgabebausteinen

## Zusammenfassung
Diese Übung vermittelt grundlegende Kenntnisse über taktgesteuerte Speicherelemente in digitalen Schaltungen. Der D-Flip-Flop zeigt das Prinzip der Datenspeicherung bei Taktflanken und demonstriert die praktische Umsetzung mit realen Ein- und Ausgängen über die logiBUS-Schnittstelle.