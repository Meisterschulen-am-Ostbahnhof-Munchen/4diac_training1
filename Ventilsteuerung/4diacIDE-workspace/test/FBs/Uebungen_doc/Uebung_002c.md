# Uebung_002c

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verarbeitung digitaler Eingangssignale und deren Ausgabe über einen digitalen Ausgang unter Verwendung von logischen Verknüpfungen und einem D-Flip-Flop. Die Schaltung kombiniert AND- und OR-Verknüpfungen mit einer Speicherfunktion.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_I1**, **DigitalInput_I2**, **DigitalInput_I3** (Typ: logiBUS_IX)
- **DigitalOutput_Q1** (Typ: logiBUS_QX)
- **AND_2** (Typ: AND_2)
- **OR_2** (Typ: OR_2)
- **BOOL2BOOL** (Typ: BOOL2BOOL)
- **E_D_FF** (Typ: E_D_FF)

### Sub-Bausteine: Keine Sub-Bausteine vorhanden

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- DigitalInput_I1.IND → AND_2.REQ
- DigitalInput_I2.IND → AND_2.REQ
- AND_2.CNF → BOOL2BOOL.REQ
- BOOL2BOOL.CNF → OR_2.REQ
- DigitalInput_I3.IND → OR_2.REQ
- OR_2.CNF → E_D_FF.CLK
- E_D_FF.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- DigitalInput_I1.IN → AND_2.IN1
- DigitalInput_I2.IN → AND_2.IN2
- AND_2.OUT → BOOL2BOOL.IN
- BOOL2BOOL.OUT → OR_2.IN1
- DigitalInput_I3.IN → OR_2.IN2
- OR_2.OUT → E_D_FF.D
- E_D_FF.Q → DigitalOutput_Q1.OUT

**Programmablauf:**
1. Die Eingänge I1 und I2 werden über eine AND-Verknüpfung verarbeitet
2. Das Ergebnis wird durch BOOL2BOOL geleitet
3. Das Signal von I3 und das AND-Ergebnis werden über eine OR-Verknüpfung kombiniert
4. Das OR-Ergebnis triggert den D-Flip-Flop (E_D_FF) als Takt-Signal
5. Der Ausgang Q des D-Flip-Flops steuert den digitalen Ausgang Q1

**Lernziele:**
- Verständnis logischer Verknüpfungen (AND, OR)
- Anwendung von D-Flip-Flops in Steuerungen
- Signalverarbeitung mit Zwischenspeicherung
- Umgang mit digitalen Ein- und Ausgängen

**Schwierigkeitsgrad:** Mittel
**Benötigte Vorkenntnisse:** Grundlagen der digitalen Logik, Basiswissen 4diac-IDE

**Starten der Übung:**
- Die Übung kann direkt in der 4diac-IDE geladen werden
- Alle Bausteine sind bereits korrekt parametriert (QI = TRUE)
- Die Hardware-Adressen sind für logiBUS-Systeme vorkonfiguriert

## Zusammenfassung
Diese Übung zeigt eine praktische Anwendung digitaler Logik mit Speicherfunktion. Durch die Kombination von Grundgattern und einem D-Flip-Flop wird demonstriert, wie Eingangssignale verarbeitet und mit Speicherverhalten ausgegeben werden können. Die Schaltung eignet sich gut zum Verständnis grundlegender Steuerungstechnik-Konzepte.