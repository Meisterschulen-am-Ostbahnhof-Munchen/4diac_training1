# Uebung_010a: SoftKey_F1/_F2 auf DigitalOutput_Q1/_Q2

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die grundlegende Verknüpfung von Softkey-Eingängen mit digitalen Ausgängen in der 4diac-IDE. Die Übung zeigt, wie Tastendrücke auf virtuelle Softkeys (F1 und F2) direkt auf entsprechende digitale Ausgänge (Q1 und Q2) abgebildet werden.

## Verwendete Funktionsbausteine (FBs)

### Softkey_IX
- **Typ**: Eingangsbaustein für Softkey-Bedienung
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = DefaultPool::SoftKey_F1 bzw. DefaultPool::SoftKey_F2 (identifiziert den spezifischen Softkey)
- **Ereignisausgang**: IND (zeigt Tastendruck an)
- **Dateneingang**: IN (überträgt den Tastenstatus)

### logiBUS_QX
- **Typ**: Ausgangsbaustein für digitale Signale
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - Output = logiBUS_DO::Output_Q1 bzw. logiBUS_DO::Output_Q2 (definiert den physikalischen Ausgang)
- **Ereigniseingang**: REQ (fordert Ausgangsaktualisierung an)
- **Datenausgang**: OUT (liefert den aktuellen Ausgangszustand)

## Programmablauf und Verbindungen

Die Übung verwendet zwei unabhängige Signalpfade:

1. **Pfad 1 (SoftKey_F1 → DigitalOutput_Q1)**:
   - Ereignisverbindung: SoftKey_F1.IND → DigitalOutput_Q1.REQ
   - Datenverbindung: SoftKey_F1.IN → DigitalOutput_Q1.OUT

2. **Pfad 2 (SoftKey_F2 → DigitalOutput_Q2)**:
   - Ereignisverbindung: SoftKey_F2.IND → DigitalOutput_Q2.REQ
   - Datenverbindung: SoftKey_F2.IN → DigitalOutput_Q2.OUT

**Lernziele**:
- Verständnis der grundlegenden Event- und Datenverbindungen
- Kennenlernen von Eingangs- und Ausgangsbausteinen
- Umsetzung von Softkey-Eingängen auf digitale Ausgänge

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**:
- Grundlagen der 4diac-IDE
- Verständnis von Funktionsbausteinen
- Basiswissen über Event-basierte Programmierung

**Starten der Übung**:
1. Die SubApp in der 4diac-IDE öffnen
2. Auf Start klicken, um die Ausführung zu beginnen
3. Softkeys F1 und F2 im HMI bedienen, um die entsprechenden Ausgänge Q1 und Q2 zu schalten

## Zusammenfassung
Diese einfache Übung vermittelt die grundlegende Verknüpfung von Eingangs- und Ausgangsbausteinen in 4diac. Sie zeigt das Prinzip der direkten Signalweiterleitung von Softkey-Eingängen zu digitalen Ausgängen und bildet damit eine Basis für komplexere Steuerungsaufgaben. Die parallele Anordnung der beiden unabhängigen Signalpfade demonstriert zudem die Modularität und Skalierbarkeit von IEC 61499-basierten Steuerungssystemen.