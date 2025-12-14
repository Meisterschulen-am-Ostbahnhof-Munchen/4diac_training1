# Uebung_010b9: Toggle Flip-Flop mit IE Button_A1 BT_STILL_HELD

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines Toggle-Flip-Flops (T-FF) in Verbindung mit einem Taster-Input-Event. Der Schwerpunkt liegt auf der Verwendung des speziellen Taster-Ereignisses "BT_STILL_HELD", das alle 200ms ausgelöst wird und einen Blinker mit 400ms-Periodendauer erzeugt.

## Verwendete Funktionsbausteine (FBs)

### Button_A1
- **Typ**: Button_IE
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::Button_A1 (Taster-Objekt-ID)
  - InputEvent = ButtonActivationCode::BT_STILL_HELD (Ereignis bei gedrückt gehaltenem Taster)

### E_T_FF
- **Typ**: E_T_FF (Toggle-Flip-Flop mit Ereignissteuerung)

### DigitalOutput_Q1
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 (Ausgangskanal für digitale Ausgabe)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- Button_A1.IND → E_T_FF.CLK (Taster-Ereignis triggert den Toggle-Flip-Flop)
- E_T_FF.EO → DigitalOutput_Q1.REQ (Flip-Flop-Ausgangsereignis aktiviert die Ausgabe)

**Datenverbindungen:**
- E_T_FF.Q → DigitalOutput_Q1.OUT (Flip-Flop-Zustand wird an den Ausgang weitergeleitet)

**Funktionsweise:**
Bei Betätigung des Tasters A1 wird das Ereignis "BT_STILL_HELD" alle 200ms ausgelöst. Jedes dieser Ereignisse toggelt den Zustand des Flip-Flops, was zu einem Ausgangssignal mit 400ms Periodendauer führt (200ms ein, 200ms aus).

**Lernziele:**
- Verständnis von Toggle-Flip-Flop-Funktionalität
- Umgang mit Taster-Input-Events
- Erzeugung von Blinkfunktionen durch Ereigniswiederholung
- Verbindung von Eingabe-, Verarbeitungs- und Ausgabebausteinen

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**: Grundlagen der 4diac-IDE, Verständnis von Funktionsbausteinen und Ereignisverbindungen

**Starten der Übung**: Die Übung wird durch Betätigen des Tasters A1 aktiviert. Der Ausgang Q1 beginnt sofort mit dem Blinken.

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung eines Toggle-Flip-Flops zur Erzeugung einer Blinkfunktion. Durch die Verwendung des "BT_STILL_HELD"-Events wird demonstriert, wie periodische Ereignisse zur Steuerung von Ausgabesignalen genutzt werden können. Die einfache Struktur macht die grundlegenden Prinzipien der ereignisgesteuerten Programmierung in 4diac deutlich.