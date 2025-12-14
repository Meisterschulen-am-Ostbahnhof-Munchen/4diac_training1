# Uebung_026: Spiegelabfolge (6)

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Spiegelabfolge-Steuerung für zwei Zylinder (Cyl_1 und Cyl_2). Die Steuerung ermöglicht das sequenzielle Ausfahren und Einfahren der Zylinder mit Zeitverzögerung und Endlagenerkennung. Die Abfolge wird über Softkeys gesteuert und folgt einem spezifischen Spiegelmuster.

## Verwendete Funktionsbausteine (FBs)

### Haupt-FBs:
- **Softkey_IE**: Softkey-Eingabebausteine für F1, F2, F3, F8, F9
- **E_REND**: Endlagenerkennungsbausteine für verschiedene Zylinderpositionen
- **E_DELAY**: Zeitverzögerungsbaustein (2 Sekunden)
- **Uebung_026_sub**: Sub-Applikation für Ausgabesteuerung (Q1-Q4)

### Sub-Bausteine: Uebung_026_sub

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **E_SR**: Set-Reset-Flipflop
        - Parameter: keine spezifischen Parameter
        - Ereigniseingänge: S (Set), R (Reset)
        - Ereignisausgang: EO
        - Datenausgang: Q (BOOL)
    - **logiBUS_QX**: Ausgabebaustein für logiBUS
        - Parameter: QI = TRUE
        - Ereigniseingang: REQ
        - Dateneingang: OUT (BOOL)
        - Dateneingang: Output (logiBUS_DO_S)
    - **E_SWITCH**: Ereignis-Schalter
        - Parameter: keine spezifischen Parameter
        - Ereigniseingänge: EI, G (BOOL)
        - Ereignisausgänge: EO1, EO2

- **Funktionsweise**: 
  Die Sub-Applikation realisiert eine Set-Reset-Funktionalität mit Ausgabesteuerung. Bei SET-Ereignis wird der Ausgang aktiviert, bei RESET-Ereignis deaktiviert. Der E_SWITCH-Baustein leitet das Ereignis weiter, wenn der Ausgangszustand Q aktiv ist.

## Programmablauf und Verbindungen

**Steuerungsablauf:**
1. **Start**: SoftKey F1 (Released) initiiert Ausfahren Cyl_1
2. **Sequenz**: 
   - Cyl_1 fährt aus → Endlage erreicht
   - SoftKey F2 (Pressed) startet Ausfahren Cyl_2
   - Cyl_2 fährt aus → Endlage erreicht
   - 2 Sekunden Verzögerung (E_DELAY)
   - Cyl_2 fährt ein → Endlage erreicht
   - SoftKey F8 (Pressed) bestätigt Einfahren Cyl_2
   - Cyl_1 fährt ein → Endlage erreicht
   - SoftKey F9 (Pressed) bestätigt Einfahren Cyl_1

**Ausgangszuordnung:**
- Q1: Steuerung Ausfahren Cyl_1
- Q2: Steuerung Ausfahren Cyl_2  
- Q3: Zeitgesteuerte Einfahrsteuerung
- Q4: Steuerung Einfahren Cyl_1

**Lernziele:**
- Verständnis von Spiegelabfolgen in pneumatischen Steuerungen
- Implementierung von Zeitverzögerungen
- Endlagenerkennung und -bestätigung
- Softkey-gesteuerte Ablaufsteuerung
- Sub-Applikationen und deren Wiederverwendung

**Schwierigkeitsgrad**: Mittel
**Benötigte Vorkenntnisse**: Grundlagen 4diac-IDE, Ereignissteuerung, logiBUS-Anbindung

**Start der Übung**: 
Die Übung wird durch Betätigen der Softkeys F1 (Start) gestartet. Die weiteren Schritte folgen der oben beschriebenen Sequenz.

## Zusammenfassung
Diese Übung demonstriert eine komplexe Spiegelabfolge-Steuerung für zwei Zylinder mit Zeitverzögerung und Endlagenerkennung. Durch die Verwendung von Sub-Applikationen wird eine modulare und wiederverwendbare Struktur erreicht. Die Steuerung kombiniere Ereignisverarbeitung, Zeitsteuerung und Ausgabekontrolle in einer praxisnahen Anwendung.