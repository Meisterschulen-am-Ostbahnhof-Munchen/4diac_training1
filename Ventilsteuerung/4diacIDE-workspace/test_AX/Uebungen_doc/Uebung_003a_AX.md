Hier ist die Dokumentationsseite für die Übung `Uebung_003a_AX`, basierend auf den bereitgestellten XML-Daten.

# Uebung_003a_AX

<Bild der Übung, falls vorhanden>

* * * * * * * * * *

## Einleitung

Die Übung `Uebung_003a_AX` demonstriert die Verwendung von typisierten Sub-Applikationen (Typed SubApps), um digitale Eingänge auf digitale Ausgänge zu verschalten. Anstatt die Logik für jeden Kanal einzeln zu implementieren, wird ein wiederverwendbarer Sub-Baustein verwendet, der die Verbindung zwischen einem logiBUS-Eingang und einem logiBUS-Ausgang generisch herstellt.

Konkret werden in dieser Übung zwei Instanzen dieses Sub-Bausteins genutzt, um den Eingang `I1` auf den Ausgang `Q1` sowie den Eingang `I2` auf den Ausgang `Q2` zu legen.

## Verwendete Funktionsbausteine (FBs)

Die Hauptanwendung besteht aus Instanzen eines selbsterstellten Sub-Bausteins. Dieser kapselt die eigentliche Hardware-Zugriffslogik.

### Sub-Bausteine: Uebung_003a_AX_sub

Dieser Sub-Baustein dient dazu, einen konfigurierbaren Eingang direkt auf einen konfigurierbaren Ausgang durchzuschalten ("IX auf QX").

- **Typ**: SubAppType
- **Verwendete interne FBs**:
    - **IX**: `logiBUS::io::DI::logiBUS_IXA`
        - Parameter: `QI` = `TRUE`
        - Parameter: `PARAMS` = (Visible="false")
        - Dateneingang: `Input` (verbunden mit der Schnittstelle `Input` des Sub-Bausteins)
        - Adapterausgang: `IN` (verbunden mit `QX.OUT`)
    - **QX**: `logiBUS::io::DQ::logiBUS_QXA`
        - Parameter: `QI` = `TRUE`
        - Parameter: `PARAMS` = (Visible="false")
        - Dateneingang: `Output` (verbunden mit der Schnittstelle `Output` des Sub-Bausteins)
        - Adaptereingang: `OUT` (verbunden mit `IX.IN`)

- **Funktionsweise**:
  Der Sub-Baustein nimmt über seine Schnittstelle die Adressen bzw. Objekte für einen Eingang (`Input`) und einen Ausgang (`Output`) entgegen. Im Inneren werden zwei Hardware-Abstraktions-Bausteine verwendet: `IX` (für den Eingang) und `QX` (für den Ausgang).
  
  Der `IX`-Baustein liest den zugewiesenen physikalischen Eingang. Über eine Adapterverbindung (`IN` zu `OUT`) wird das Signal direkt an den `QX`-Baustein weitergeleitet, der den zugewiesenen physikalischen Ausgang schaltet. Dies ermöglicht eine transparente Weiterleitung des Signals ohne zusätzliche logische Verknüpfungen (AND, OR, etc.).

## Programmablauf und Verbindungen

Das Hauptnetzwerk der Übung `Uebung_003a_AX` instanziert den oben beschriebenen Sub-Baustein zweimal, um zwei unabhängige Signalpfade zu realisieren.

1.  **Instanz F1**:
    - Diese Instanz verbindet den Taster/Eingang `Input_I1` mit der Lampe/dem Ausgang `Output_Q1`.
    - Sobald `I1` aktiv ist (Signal High), wird `Q1` aktiviert.

2.  **Instanz F2**:
    - Diese Instanz verbindet den Taster/Eingang `Input_I2` mit der Lampe/dem Ausgang `Output_Q2`.
    - Sobald `I2` aktiv ist (Signal High), wird `Q2` aktiviert.

Die Übung zeigt somit, wie man durch Modularisierung (Erstellung des `Uebung_003a_AX_sub`) redundanten Code vermeidet und die Hauptansicht der Applikation übersichtlich hält.

## Zusammenfassung

Diese Übung vermittelt das Konzept der Wiederverwendbarkeit in 4diac. Durch die Erstellung eines generischen Sub-Bausteins (`Uebung_003a_AX_sub`), der die logiBUS-Kommunikation zwischen Eingang und Ausgang kapselt, kann die Hauptanwendung sehr einfach gestaltet werden. Es wird eine direkte 1:1-Zuordnung von zwei Eingängen auf zwei Ausgänge realisiert.