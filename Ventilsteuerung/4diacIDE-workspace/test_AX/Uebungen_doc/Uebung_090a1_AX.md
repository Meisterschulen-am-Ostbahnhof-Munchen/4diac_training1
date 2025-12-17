Hier ist die Dokumentation für die Übung `Uebung_090a1_AX` basierend auf den bereitgestellten Daten.

# Uebung_090a1_AX

![Uebung_090a1_AX](Uebung_090a1_AX.png)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Verwendung des `AX_MUX_2` Bausteins (Adapter Multiplexer). Ziel ist es, zwischen zwei verschiedenen Adapter-Eingangsquellen (`Input_I1` und `Input_I2`) umzuschalten und das ausgewählte Signal an einen Adapter-Ausgang (`Output_Q1`) weiterzuleiten. Die Umschaltung erfolgt gesteuert durch einen digitalen Steuereingang (`Input_I4`). Dies veranschaulicht, wie Adapter-Verbindungen basierend auf logischen Zuständen dynamisch geroutet werden können.

## Verwendete Funktionsbausteine (FBs)

In dieser Sub-Application werden verschiedene logiBUS-IO-Bausteine sowie Konvertierungs- und Adapter-Logikbausteine verwendet.

### Sub-Bausteine:

#### **F_MUX_2**
- **Typ**: `adapter::selection::unidirectional::AX_MUX_2`
- **Beschreibung**: Ein Adapter-Multiplexer, der einen von zwei Adapter-Eingängen (`IN1`, `IN2`) basierend auf einem Integer-Eingang (`K`) auf den Ausgang (`OUT`) durchschaltet.
- **Verwendete interne Verbindungen**:
    - **Dateneingang**: `K` (Selektor)
    - **Adaptereingang**: `IN1`, `IN2`
    - **Adapterausgang**: `OUT`
    - **Ereigniseingang**: `REQ` (Löst die Umschaltung aus)

#### **DigitalInput_I4**
- **Typ**: `logiBUS::io::DI::logiBUS_IX`
- **Beschreibung**: Ein digitaler Eingangsbaustein, der ereignisbasiert arbeitet. Er dient als Steuerquelle für die Umschaltung.
- **Parameter**: 
    - `QI` = `TRUE`
    - `Input` = `Input_I4`
- **Ereignisausgang**: `IND` (Signalisiert Zustandsänderung)
- **Datenausgang**: `IN` (Aktueller Zustand TRUE/FALSE)

#### **F_BOOL_TO_UINT_I4**
- **Typ**: `iec61131::conversion::F_BOOL_TO_UINT`
- **Beschreibung**: Konvertiert den booleschen Zustand des Eingangs `I4` in einen Integer-Wert (Unsigned Integer), da der Multiplexer einen numerischen Index zur Auswahl benötigt.
- **Funktionsweise**: 
    - `FALSE` -> `0`
    - `TRUE` -> `1`

#### **DigitalOutput_Q1**
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Beschreibung**: Ein digitaler Ausgangsbaustein mit Adapter-Schnittstelle.
- **Parameter**: 
    - `QI` = `TRUE`
    - `Output` = `Output_Q1`
- **Adaptereingang**: `OUT` (Empfängt das durchgeschaltete Signal)

#### **DigitalInput_I1**
- **Typ**: `logiBUS::io::DI::logiBUS_IXA`
- **Beschreibung**: Erster digitaler Eingang mit Adapter-Schnittstelle (Quelle 1).
- **Parameter**: 
    - `QI` = `TRUE`
    - `Input` = `Input_I1`
- **Adapterausgang**: `IN`

#### **DigitalInput_I2**
- **Typ**: `logiBUS::io::DI::logiBUS_IXA`
- **Beschreibung**: Zweiter digitaler Eingang mit Adapter-Schnittstelle (Quelle 2).
- **Parameter**: 
    - `QI` = `TRUE`
    - `Input` = `Input_I2`
- **Adapterausgang**: `IN`

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in einen Steuerpfad und einen Adapter-Pfad unterteilen:

1.  **Steuerpfad (Logik):**
    *   Der Baustein `DigitalInput_I4` überwacht den Hardware-Eingang `Input_I4`.
    *   Sobald sich der Zustand ändert, wird ein Event (`IND`) und der neue Datenwert (`IN`) gesendet.
    *   Der Baustein `F_BOOL_TO_UINT_I4` wandelt diesen booleschen Wert in eine Ganzzahl um (0 oder 1) und gibt diesen an den Eingang `K` des Multiplexers `F_MUX_2` weiter.
    *   Das `CNF`-Event der Konvertierung triggert den `REQ`-Eingang des Multiplexers, um die Umschaltung zu aktualisieren.

2.  **Adapter-Pfad (Routing):**
    *   Die Bausteine `DigitalInput_I1` und `DigitalInput_I2` stellen zwei unabhängige Adapter-Quellen dar.
    *   Diese sind mit den Eingängen `IN1` und `IN2` des Multiplexers `F_MUX_2` verbunden.
    *   Abhängig vom Wert an `K` (welcher von `Input_I4` bestimmt wird), verbindet der Multiplexer intern entweder `IN1` oder `IN2` mit seinem Ausgang `OUT`.
    *   Der Ausgang `OUT` ist mit dem `DigitalOutput_Q1` verbunden.

**Zusammenfassend:**
*   Wenn `Input_I4` aktiv ist (TRUE -> 1), wird (abhängig von der internen Logik des MUX, üblicherweise 1-basiert oder 0-basiert) einer der Eingänge (`I1` oder `I2`) auf `Q1` durchgeschaltet.
*   Diese Übung zeigt exemplarisch, wie man reine Datensignale (I4) nutzt, um komplexe Adapter-Verbindungen (LogiBUS Inputs zu Outputs) zu steuern.

## Zusammenfassung
Die Übung `Uebung_090a1_AX` ist ein grundlegendes Beispiel für das Routing von Adapter-Signalen in 4diac. Sie verdeutlicht die Trennung von Steuerlogik (über Standard-Events und Datentypen) und der eigentlichen Signalübertragung über Adapter-Schnittstellen (wie sie bei logiBUS verwendet werden). Durch den Einsatz des `AX_MUX_2` können Ressourcen flexibel zugewiesen werden.