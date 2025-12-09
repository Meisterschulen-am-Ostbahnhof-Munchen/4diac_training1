# Uebung_087: Beispiel für E_DEMUX

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des E_DEMUX-Funktionsbausteins zur Ereignisverteilung basierend auf einem Steuerwert. Das System zählt die Anzahl aktiver Eingänge und verteilt ein Taktereignis entsprechend auf verschiedene Ausgänge. Die Übung zeigt praktische Anwendungen von Multiplexing und T-Flip-Flop-Steuerung in verteilten Automatisierungssystemen.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **E_DEMUX**: Ereignis-Demultiplexer zur Verteilung von Ereignissen basierend auf einem Steuerwert
- **ADD_3**: Addierer für drei Eingangswerte
- **F_BOOL_TO_UINT**: Wandelt boolesche Werte in unsigned integer Werte um
- **E_T_FF**: Toggle-Flip-Flop mit Ereignissteuerung
- **logiBUS_IX**: Digitaler Eingang mit Ereignisausgang
- **logiBUS_QX**: Digitaler Ausgang

### Sub-Bausteine:
**logiBUS_IX** (Digital Input)
- **Typ**: logiBUS_IX
- **Parameter**: 
  - QI = TRUE (Qualified Input aktiviert)
  - Input = logiBUS_DI::Input_Ix (spezifischer Hardware-Eingang)
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK (nur bei CLK_I1)

**logiBUS_QX** (Digital Output)
- **Typ**: logiBUS_QX
- **Parameter**:
  - QI = TRUE (Qualified Input aktiviert)
  - Output = logiBUS_DO::Output_Qx (spezifischer Hardware-Ausgang)

## Programmablauf und Verbindungen

### Signalfluss:
1. **Eingangsverarbeitung**: 
   - Drei digitale Eingänge (I2, I3, I4) werden über logiBUS_IX-Bausteine erfasst
   - Die booleschen Werte werden mittels F_BOOL_TO_UINT in uint-Werte konvertiert

2. **Zählung aktiver Eingänge**:
   - ADD_3 summiert die drei uint-Werte (0 oder 1) zu einem Gesamtwert (0-3)
   - Dieser Wert bestimmt den Ausgangskanal des E_DEMUX

3. **Ereignisverteilung**:
   - Der Taktgeber (I1 mit BUTTON_SINGLE_CLICK) löst über E_DEMUX.EI ein Ereignis aus
   - E_DEMUX leitet das Ereignis basierend auf dem K-Wert (0-3) an einen der vier Ausgänge weiter

4. **Ausgangssteuerung**:
   - Vier E_T_FF-Bausteine schalten bei jedem empfangenen CLK-Ereignis ihren Zustand um
   - Die Ausgänge Q1-Q4 werden entsprechend über logiBUS_QX-Bausteine angesteuert

### Verhaltenslogik:
- **Keine Taste gedrückt** (K=0) → Q1 toggelt
- **Eine Taste gedrückt** (K=1) → Q2 toggelt  
- **Zwei Tasten gedrückt** (K=2) → Q3 toggelt
- **Drei Tasten gedrückt** (K=3) → Q4 toggelt

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Ereignisverteilung und Signalverarbeitung in IEC 61499-Systemen. Sie zeigt die praktische Anwendung von Demultiplexern, die Umwandlung von Datentypen und die Steuerung von Flip-Flops durch ereignisbasierte Architekturen. Die Übung eignet sich ideal zum Verständnis von Multiplexing-Techniken und deren Implementierung in verteilten Automatisierungssystemen.