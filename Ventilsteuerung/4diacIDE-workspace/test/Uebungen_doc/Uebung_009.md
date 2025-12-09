# Uebung_009: Ticker

* * * * * * * * * *

## Einleitung
Diese Übung implementiert einen Ticker-Zähler, der periodisch ein Signal ausgibt und gleichzeitig einen Zählerstand anzeigt. Das System verwendet verschiedene Funktionsbausteine zur Ereignissteuerung und Datenverarbeitung.

## Verwendete Funktionsbausteine (FBs)

### E_CYCLE
- **Typ**: Zyklusgeber
- **Parameter**: DT = T#1s (Zykluszeit von 1 Sekunde)
- **Funktionsweise**: Generiert periodische Ereignisse im angegebenen Zeitintervall

### E_SWITCH
- **Typ**: Ereignis-Umschalter
- **Funktionsweise**: Leitet eingehende Ereignisse basierend auf dem Steuersignal G an EO0 oder EO1 weiter

### E_SR
- **Typ**: Set-Reset-Flipflop
- **Funktionsweise**: Speichert einen Zustand, der durch S-Ereignisse gesetzt und durch R-Ereignisse zurückgesetzt wird

### E_PERMIT
- **Typ**: Ereignis-Freigabe
- **Funktionsweise**: Gibt Ereignisse nur dann weiter, wenn das PERMIT-Signal TRUE ist

### E_CTUD_UDINT
- **Typ**: Hoch-/Runterzähler (unsigned double integer)
- **Parameter**: PV = 0 (Vorbelegungswert)
- **Funktionsweise**: Zählt bei jedem CU-Ereignis hoch

### DigitalOutput_Q1
- **Typ**: logiBUS_QX (digitale Ausgabe)
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Ausgangskanal)

### Q_NumericValue
- **Typ**: Numerischer Wert-Ausgabe
- **Parameter**: u16ObjId = DefaultPool::OutputNumber_N1 (Ausgabekennung)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- E_CYCLE.EO → E_SWITCH.EI (Zyklische Ereignisgenerierung)
- E_SWITCH.EO0 → E_SR.S (Setzen des Flipflops)
- E_SWITCH.EO1 → E_SR.R (Rücksetzen des Flipflops)
- E_SR.EO → DigitalOutput_Q1.REQ (Ausgabeanforderung)
- E_SR.EO → E_PERMIT.EI (Freigabe-Eingang)
- E_PERMIT.EO → E_CTUD_UDINT.CU (Zähler-Eingang)
- E_CTUD_UDINT.CO → Q_NumericValue.REQ (Wertausgabe-Anforderung)

**Datenverbindungen:**
- E_SR.Q → E_SWITCH.G (Rückkopplung für Umschaltung)
- E_SR.Q → DigitalOutput_Q1.OUT (Direkte Signalausgabe)
- E_SR.Q → E_PERMIT.PERMIT (Freigabe-Steuerung)
- E_CTUD_UDINT.CV → Q_NumericValue.u32NewValue (Zählerwert-Übertragung)

**Startbedingung:** In den Watch-Modus wechseln und bei START ein Event auslösen.

**Lernziele:**
- Verständnis von Ereignissteuerung und Datenfluss
- Umgang mit Flipflops und Zählern
- Implementierung von Rückkopplungsschleifen
- Verwendung von periodischen Signalen

**Schwierigkeitsgrad:** Mittel

**Benötigte Vorkenntnisse:**
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Kenntnisse über Ereignis- und Datenverbindungen

## Zusammenfassung
Diese Übung demonstriert ein komplexes Steuerungssystem mit periodischer Signalgenerierung, Zustandsspeicherung und Zählfunktionalität. Der Ticker arbeitet mit einer 1-Sekunden-Zykluszeit und zeigt sowohl eine digitale Ausgabe als auch einen numerischen Zählerstand an. Die Rückkopplung des Flipflop-Zustands auf den Ereignis-Umschalter ermöglicht einen automatischen Wechsel zwischen Set- und Reset-Zuständen.