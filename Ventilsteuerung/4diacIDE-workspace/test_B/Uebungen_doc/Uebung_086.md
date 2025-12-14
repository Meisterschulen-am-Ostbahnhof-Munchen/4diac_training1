# Uebung_086: Beispiel für E_SWITCH

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_SWITCH-Funktionsbausteins in einem 4diac-IDE Programm. Die Übung zeigt, wie ein digitaler Eingang mit einem Schalter-Baustein verbunden wird und dient als grundlegendes Beispiel für die Verwendung von Event-Steuerung in IEC 61499.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_I1
- **Typ**: logiBUS_IX
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
- **Funktionsweise**: Stellt einen digitalen Eingang für das logiBUS-System bereit und gibt den Eingangswert an den Datenausgang IN weiter.

### E_SWITCH
- **Typ**: E_SWITCH
- **Funktionsweise**: Ein Ereignis-Schalter, der basierend auf dem Eingangswert am Datenanschluss G entscheidet, ob ein eingehendes Ereignis weitergeleitet wird oder nicht.

## Programmablauf und Verbindungen

Das Programm besteht aus zwei Hauptkomponenten:

1. **Ereignisverbindung**: 
   - DigitalInput_I1.IND → E_SWITCH.EI
   - Überträgt das Indikator-Ereignis vom digitalen Eingang zum E_SWITCH

2. **Datenverbindung**:
   - DigitalInput_I1.IN → E_SWITCH.G
   - Überträgt den aktuellen Wert des digitalen Eingangs als Steuersignal zum E_SWITCH

**Lernziele**:
- Verständnis der E_SWITCH-Funktionalität
- Aufbau von Ereignis- und Datenverbindungen zwischen Funktionsbausteinen
- Arbeit mit digitalen Eingängen im logiBUS-System

**Schwierigkeitsgrad**: Einfach

**Benötigte Vorkenntnisse**:
- Grundlagen der IEC 61499
- Kenntnisse der 4diac-IDE Oberfläche
- Verständnis von Ereignis- und Datenflüssen

## Zusammenfassung
Diese Übung bietet eine einfache Einführung in die Verwendung des E_SWITCH-Bausteins und zeigt die grundlegende Verbindung zwischen einem digitalen Eingang und einem Schalter-Baustein. Das Beispiel verdeutlicht das Prinzip der ereignisgesteuerten Ausführung in IEC 61499-Systemen und bildet eine Basis für komplexere Steuerungsaufgaben.