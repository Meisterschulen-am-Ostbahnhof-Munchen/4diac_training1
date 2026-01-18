# Uebung_103: DigitalInput_I1 auf DigitalOutput_Q1, mit Plug and Socket und DEMUX

```{index} single: Uebung_103: DigitalInput_I1 auf DigitalOutput_Q1, mit Plug and Socket und DEMUX
```

* * * * * * * * * *

## 📺 Video

* [2025-02-02 18-21-50 Uebung_006c Funktion E_DEMUX8 und ..._DI_REPEAT](https://www.youtube.com/watch?v=fOSa4_A7-dE)
* [2025-03-30 16-40-13 Softkey Ansteuerung Übung 10b2](https://www.youtube.com/watch?v=RLUNzsGLVw8)
* [2025-03-30 16-47-54 Subapplications Übung 003a](https://www.youtube.com/watch?v=hKU6_d82lAE)
* [2025-12-14 20-03-27 Aufspielen Training 1 Übung 1 auf das Hutschienenmoped.](https://www.youtube.com/watch?v=6iog7-DZvW0)
* [Aufwärts zählen Baustein E_CTU aus der IEC 61499 (Übung 80)](https://www.youtube.com/watch?v=oZOWd_zKFcc)

## Einleitung
Diese Übung demonstriert die Verarbeitung eines digitalen Eingangssignals zu einem digitalen Ausgangssignal unter Verwendung von Plug-and-Socket-Verbindungen sowie DEMUX- und MUX-Funktionsbausteinen. Das System ermöglicht unterschiedliche Signalverarbeitungsmodi für verschiedene Anwendungsfälle.

## Verwendete Funktionsbausteine (FBs)

### Haupt-Funktionsbausteine:
- **DigitalInput_I1** (logiBUS_IXA): Liest digitale Eingangssignale von Input_I1
- **DigitalOutput_Q1** (logiBUS_QXA): Schreibt digitale Ausgangssignale zu Output_Q1
- **AX_DEMUX_3**: Verteilt Eingangssignale auf drei verschiedene Ausgänge
- **AX_MUX_3**: Kombiniert drei Eingangssignale zu einem Ausgangssignal
- **InputNumber_I1** (NumericValue_ID): Stellt numerische Eingabewerte bereit
- **C1** (F_DWORD_TO_UDINT): Konvertiert DWORD zu UDINT
- **C2** (F_UDINT_TO_UINT): Konvertiert UDINT zu UINT

### Sub-Bausteine:

#### Sub-Baustein: rastend
- **Typ**: FBs::Uebungen::Uebung_103::subapp::rastend
- **Funktionsweise**: Verarbeitet rastende (haltende) Signale

#### Sub-Baustein: tastend  
- **Typ**: FBs::Uebungen::Uebung_103::subapp::tastend
- **Funktionsweise**: Verarbeitet tastende (momentane) Signale

#### Sub-Baustein: tastend_TON_5s
- **Typ**: FBs::Uebungen::Uebung_103::subapp::tastend_TON_5s
- **Funktionsweise**: Verarbeitet tastende Signale mit 5-Sekunden-Zeitverzögerung

## Programmablauf und Verbindungen

Der Signalfluss beginnt beim DigitalInput_I1, der das Eingangssignal von Input_I1 liest. Das Signal wird an den AX_DEMUX_3 weitergeleitet, der es auf drei verschiedene Pfade verteilt:

1. **OUT0** → tastend-Subapplikation → AX_MUX_3 IN0
2. **OUT1** → rastend-Subapplikation → AX_MUX_3 IN1  
3. **OUT2** → tastend_TON_5s-Subapplikation → AX_MUX_3 IN2

Der AX_MUX_3 kombiniert die verarbeiteten Signale und leitet sie an DigitalOutput_Q1 weiter, der das Ergebnis an Output_Q1 ausgibt.

Zusätzlich verarbeitet InputNumber_I1 numerische Werte über Konvertierungsbausteine (C1, C2), die sowohl DEMUX als auch MUX mit Steuersignalen versorgen.

**Lernziele:**
- Verständnis von Plug-and-Socket-Verbindungen
- Umgang mit DEMUX/MUX-Bausteinen
- Signalverteilung und -kombination
- Integration von Subapplikationen

**Schwierigkeitsgrad**: Mittel

**Benötigte Vorkenntnisse**: Grundkenntnisse in 4diac-IDE, digitale Ein-/Ausgänge, Funktionsbausteine

**Start der Übung**: Das System wird automatisch aktiviert, sobald die Parameter QI auf TRUE gesetzt sind.

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit Signalverteilung und -kombination unter Verwendung von DEMUX- und MUX-Bausteinen. Die Integration verschiedener Signalverarbeitungsmodi (rastend, tastend, verzögert) in Subapplikationen zeigt eine flexible und modulare Programmstruktur, die für komplexere Steuerungsaufgaben grundlegend ist.