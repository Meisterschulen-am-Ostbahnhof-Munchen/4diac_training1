Hier ist die Dokumentation für die Übung `Uebung_004a_AX` im gewünschten Format.

# Uebung_004a_AX

![Platzhalter für Bild der Übung]

* * * * * * * * * *

## Einleitung
Diese Übung implementiert eine Toggle-Flip-Flop-Schaltung (T-Flip-Flop), die speziell für die Verwendung mit Hardware-Eingangsereignissen konzipiert ist. Die Logik reagiert auf einen einfachen Tastendruck (Single Click) an einem digitalen Eingang und schaltet daraufhin einen digitalen Ausgang um. Besonderheit hierbei ist die Verwendung von Adapter-Verbindungen für die Ausgangssteuerung und spezifischen Event-Handlern für den Eingang.

## Verwendete Funktionsbausteine (FBs)

In dieser SubApplikation werden folgende Bausteine instanziiert und verschaltet:

### Sub-Bausteine: DigitalInput_CLK_I1
- **Typ**: `logiBUS::io::DI::logiBUS_IE`
- **Beschreibung**: Dieser Baustein dient als Schnittstelle für digitale Eingangsereignisse.
- **Verwendete interne Konfiguration**:
    - **Parameter**: `QI` = `TRUE` (Baustein ist aktiv)
    - **Parameter**: `Input` = `Input_I1` (Hardware-Zuordnung zum ersten Eingang)
    - **Parameter**: `InputEvent` = `BUTTON_SINGLE_CLICK` (Reagiert nur auf einfachen Klick)
- **Funktionsweise**: Er überwacht den Hardware-Eingang `I1`. Sobald das definierte Ereignis (Single Click) eintritt, wird am Ausgang `IND` ein Event gefeuert.

### Sub-Bausteine: E_T_FF
- **Typ**: `adapter::events::unidirectional::AX_T_FF`
- **Beschreibung**: Ein T-Flip-Flop (Toggle Flip-Flop), das über Adapter-Technologie kommuniziert.
- **Verwendete interne Konfiguration**:
    - **Ereigniseingang**: `CLK` (Clock/Takt)
    - **Adapterausgang**: `Q`
- **Funktionsweise**: Bei jedem Signal am `CLK`-Eingang wechselt der interne Zustand (True/False). Dieser Zustand wird über den Adapter-Port `Q` bereitgestellt.

### Sub-Bausteine: DigitalOutput_Q1
- **Typ**: `logiBUS::io::DQ::logiBUS_QXA`
- **Beschreibung**: Schnittstelle für digitale Ausgänge, die über Adapter angesteuert wird.
- **Verwendete interne Konfiguration**:
    - **Parameter**: `QI` = `TRUE`
    - **Parameter**: `Output` = `Output_Q1` (Hardware-Zuordnung zum ersten Ausgang)
    - **Adaptereingang**: `OUT`
- **Funktionsweise**: Empfängt den Zustand direkt über eine Adapterverbindung am Port `OUT` und schaltet den physischen Ausgang `Q1` entsprechend.

## Programmablauf und Verbindungen

Der Ablauf der Schaltung ist ereignisgesteuert und nutzt moderne Adapter-Konzepte zur Datenübertragung:

1.  **Eingangserkennung**: Der Baustein `DigitalInput_CLK_I1` überwacht den Eingang `Input_I1`.
2.  **Auslöser**: Wenn der Benutzer den Taster einmal drückt (`BUTTON_SINGLE_CLICK`), wird das `IND`-Event ausgelöst.
3.  **Verarbeitung**:
    - Das Event wird über eine **Event-Verbindung** vom `IND`-Ausgang des Eingangsbausteins an den `CLK`-Eingang des `E_T_FF` Bausteins geleitet.
4.  **Logik**: Das T-Flip-Flop (`E_T_FF`) wechselt seinen logischen Zustand (von Ein auf Aus oder umgekehrt).
5.  **Ausgabe**:
    - Der neue Zustand wird über eine **Adapter-Verbindung** vom Port `Q` des `E_T_FF` an den Port `OUT` des `DigitalOutput_Q1` übergeben.
    - Der Hardware-Ausgang `Output_Q1` wird entsprechend geschaltet.

**Lernziele:**
- Verständnis von Event-gesteuerten Eingängen (`logiBUS_IE`).
- Nutzung von `BUTTON_SINGLE_CLICK` zur Entprellung und Gestenerkennung.
- Einsatz von Adapter-Verbindungen (`AX`) zur Vereinfachung des Datenflusses zwischen Logik und IO.

## Zusammenfassung
Die `Uebung_004a_AX` zeigt eine effiziente Methode, um eine Stromstoßschalter-Funktion (Toggle) zu realisieren. Durch die Verwendung des `BUTTON_SINGLE_CLICK` Parameters wird sichergestellt, dass der Ausgang sauber schaltet, ohne durch Kontaktprellen mehrfach ausgelöst zu werden. Die Nutzung von Adapter-Verbindungen reduziert den sichtbaren Verdrahtungsaufwand für Datensignale.