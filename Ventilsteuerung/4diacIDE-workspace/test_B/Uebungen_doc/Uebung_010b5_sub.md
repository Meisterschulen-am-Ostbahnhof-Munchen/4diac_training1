Hier ist die Dokumentation für die SubApplikation `Uebung_010b5_sub` basierend auf dem bereitgestellten XML-Code.

# Uebung_010b5_sub

![Bild der Übung Uebung_010b5_sub](img/Uebung_010b5_sub.png)

* * * * * * * * * *

## Einleitung

Die SubApplikation **Uebung_010b5_sub** stellt eine generische Verbindung zwischen einem ISOBUS-Softkey-Eingang (IX) und einem digitalen Ausgang (QX) her. Sie dient als wiederverwendbarer Baustein, um eine Softkey-Betätigung auf einem Universal Terminal (UT) direkt auf einen physischen oder logischen Ausgang zu mappen. Durch die Verwendung von Schnittstellen-Variablen für die Objekt-ID und die Ausgangs-Adresse ist der Baustein flexibel einsetzbar.

## Verwendete Funktionsbausteine (FBs)

Diese Übung besteht aus einer SubApplikation, die intern zwei spezifische Funktionsbausteine verschaltet, um die Signalweiterleitung zu realisieren.

### Sub-Bausteine: Uebung_010b5_sub

- **Typ**: SubAppType
- **Beschreibung**: Kapselt die Logik zur Weiterleitung eines Softkey-Signals an einen Digitalausgang.
- **Verwendete interne FBs**:

    - **Bausteinname**: QX
        - **Typ**: `logiBUS::io::DQ::logiBUS_QX`
        - **Parameter**: 
            - `QI` = `TRUE`
            - `PARAMS` = (leer/versteckt)
        - **Ereigniseingang**: `REQ` (verbunden mit IX.IND)
        - **Dateneingang**: 
            - `OUT` (verbunden mit IX.IN)
            - `Output` (verbunden mit SubApp-Eingang `Output`)
        - **Funktion**: Dieser Baustein steuert einen digitalen Ausgang im logiBUS-System an.

    - **Bausteinname**: IX
        - **Typ**: `isobus::UT::io::Softkey::Softkey_IX`
        - **Parameter**: 
            - `QI` = `TRUE`
        - **Ereignisausgang**: `IND` (verbunden mit QX.REQ)
        - **Dateneingang**: 
            - `u16ObjId` (verbunden mit SubApp-Eingang `u16ObjId`)
        - **Datenausgang**: `IN` (verbunden mit QX.OUT)
        - **Funktion**: Dieser Baustein liest den Status eines ISOBUS-Softkeys, identifiziert durch die `u16ObjId`.

- **Funktionsweise**: 
    Der interne Ablauf beginnt beim Baustein **IX**. Dieser überwacht einen durch die `u16ObjId` definierten Softkey. Sobald sich der Status ändert oder ein Ereignis eintritt, wird dies über den Ereignisausgang `IND` signalisiert und der aktuelle Wert über `IN` ausgegeben. Dieses Ereignis triggert den Baustein **QX** am Eingang `REQ`. Der Baustein **QX** übernimmt den Wert vom Softkey und schaltet den physikalischen Ausgang, der über den Eingang `Output` definiert wurde.

## Programmablauf und Verbindungen

Der Programmablauf innerhalb dieser SubApplikation ist ereignisgesteuert und linear:

1.  **Initialisierung**: Beide internen Bausteine (`IX` und `QX`) werden mit `QI = TRUE` initialisiert, sind also standardmäßig aktiv.
2.  **Eingangsparameter**:
    *   `u16ObjId` (UINT): Legt fest, welcher ISOBUS-Softkey überwacht werden soll (Standard: `ID_NULL`).
    *   `Output` (logiBUS_DO_S): Definiert, welcher digitale Ausgang (Q1..Q8) angesteuert werden soll.
3.  **Signalfluss**:
    *   Wenn der Softkey (definiert durch `u16ObjId`) betätigt wird, feuert der Baustein **IX** das Event `IND`.
    *   Gleichzeitig wird der Status des Softkeys am Ausgang `IN` bereitgestellt.
    *   Das Event `IND` ist direkt mit dem Eingang `REQ` des **QX**-Bausteins verbunden.
    *   Der Datenwert `IN` (Softkey-Status) wird an den Eingang `OUT` des **QX**-Bausteins übergeben.
    *   Der Baustein **QX** schreibt diesen Wert auf den durch `Output` gewählten Hardware-Ausgang.

**Lernziele:**
*   Verständnis von SubApp-Strukturen in 4diac.
*   Verknüpfung von ISOBUS-Eingängen (Softkeys) mit Hardware-Ausgängen.
*   Erstellung generischer, wiederverwendbarer Module durch Nutzung von Inputs für IDs und Adressen.

## Zusammenfassung

Die SubApplikation `Uebung_010b5_sub` ist ein kompakter und modularer Baustein, der eine direkte "Durchverdrahtung" von einem virtuellen ISOBUS-Softkey auf einen realen Schaltausgang ermöglicht. Durch die Parametrisierung von außen (Softkey-ID und Ausgangs-Adresse) muss die interne Logik bei geänderten Anforderungen nicht angepasst werden, was die Wiederverwendbarkeit im Projekt erhöht.