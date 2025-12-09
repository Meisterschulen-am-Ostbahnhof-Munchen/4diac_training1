# Uebung_010c: SoftKey_F1 auf DigitalOutput_Q1 mit GreenWhiteBackground

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verknüpfung einer Softkey-Funktion mit einem digitalen Ausgang und einer Hintergrundfarbsteuerung. Die Übung zeigt, wie ein einzelner Softkey-Event mehrere Aktionen gleichzeitig auslösen kann.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **SoftKey_F1** (Typ: Softkey_IX)
- **DigitalOutput_Q1** (Typ: logiBUS_QX)
- **GreenWhiteBackground** (Typ: SubApp)

### Sub-Bausteine: GreenWhiteBackground
- **Typ**: SubApp
- **Verwendete interne FBs**: Keine spezifiziert in den bereitgestellten Dateien
- **Funktionsweise**: Dieser Sub-App-Baustein steuert die Hintergrundfarbe basierend auf dem Softkey-Status und zeigt sie in Grün/Weiß an.

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_F1.IND → DigitalOutput_Q1.REQ
- SoftKey_F1.IND → GreenWhiteBackground.REQ

**Datenverbindungen:**
- SoftKey_F1.IN → DigitalOutput_Q1.OUT
- SoftKey_F1.IN → GreenWhiteBackground.DI1

**Parameterkonfiguration:**
- DigitalOutput_Q1: QI=TRUE, Output=logiBUS_DO::Output_Q1
- SoftKey_F1: QI=TRUE, u16ObjId=DefaultPool::SoftKey_F1
- GreenWhiteBackground: u16ObjId=DefaultPool::SoftKey_F1

**Besonderheit:** Der Parameter "DefaultPool::SoftKey_F1" muss zweimal angegeben werden (für SoftKey_F1 und GreenWhiteBackground), was als Nachteil in einem Kommentar vermerkt ist.

**Lernziele:**
- Verknüpfung von Softkey-Eingaben mit Aktoren
- Parallele Steuerung mehrerer Komponenten durch ein Ereignis
- Verwendung von Sub-Apps für erweiterte Funktionalität
- Parametrierung von logiBUS-Komponenten

**Schwierigkeitsgrad:** Einfach
**Benötigte Vorkenntnisse:** Grundlagen der 4diac-IDE, Verständnis von Ereignis- und Datenverbindungen

## Zusammenfassung
Diese Übung zeigt eine grundlegende Softkey-Implementierung, bei der ein Tastendruck (F1) gleichzeitig einen digitalen Ausgang (Q1) schaltet und eine Hintergrundfarbänderung auslöst. Die Übung demonstriert effektiv die parallele Verarbeitung von Ereignissen und die Wiederverwendung von Objekt-IDs in verschiedenen Komponenten eines 4diac-Systems.