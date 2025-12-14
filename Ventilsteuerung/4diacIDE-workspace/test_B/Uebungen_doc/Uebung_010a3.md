# Uebung_010a3: Button_L1 (Latching) auf DigitalOutput_Q1

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung eines Latching-Buttons (rastender Taster) zur Steuerung eines digitalen Ausgangs. Die Besonderheit dieser Implementierung ist, dass kein zusätzlicher T-Flipflop benötigt wird, da der Button selbst die Latching-Funktionalität bereitstellt.

## Verwendete Funktionsbausteine (FBs)

### Button_IX (Button_L1)
- **Typ**: Button_IX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - u16ObjId = DefaultPool::Button_L1 (Objekt-ID für Button-Konfiguration)
- **Ereignisausgang**: IND (Indication - Signalisiert Zustandsänderung)
- **Datenaustgang**: IN (Datenausgang mit aktuellem Button-Zustand)

### logiBUS_QX (DigitalOutput_Q1)
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Q1 (Zugeordneter Hardware-Ausgang)
- **Ereigniseingang**: REQ (Request - Auslöser für Ausgangsaktualisierung)
- **Dateneingang**: OUT (Datenwert für den Ausgang)

## Programmablauf und Verbindungen

**Ereignisverbindung:**
- Button_L1.IND → DigitalOutput_Q1.REQ

**Datenverbindung:**
- Button_L1.IN → DigitalOutput_Q1.OUT

**Funktionsweise:**
1. Beim Betätigen des Latching-Buttons sendet Button_L1 ein IND-Ereignis
2. Das IND-Ereignis löst über REQ die Aktualisierung des Digitalausgangs aus
3. Der aktuelle Button-Zustand (IN) wird an den Digitalausgang (OUT) weitergeleitet
4. Der Button behält seinen Zustand bei (Latching-Funktion) bis zur nächsten Betätigung

**Lernziele:**
- Verständnis von Latching-Buttons (rastenden Tastern)
- Direkte Verknüpfung von Eingängen und Ausgängen
- Verwendung von qualifizierten Ein- und Ausgängen (QI-Parameter)
- Hardware-Konfiguration über Objekt-IDs

**Schwierigkeitsgrad:** Einfach

**Benötigte Vorkenntnisse:**
- Grundverständnis von IEC 61499
- Kenntnisse über digitale Ein- und Ausgänge
- Basiswissen über Event- und Data-Connections

## Zusammenfassung
Diese Übung zeigt eine einfache aber effektive Implementierung eines Latching-Buttons zur Steuerung eines digitalen Ausgangs. Die Besonderheit liegt in der integrierten Latching-Funktionalität des Buttons, die den Einsatz zusätzlicher Logikbausteine überflüssig macht. Die direkte Verbindung zwischen Eingang und Ausgang demonstriert grundlegende Prinzipien der Steuerungstechnik in 4diac.