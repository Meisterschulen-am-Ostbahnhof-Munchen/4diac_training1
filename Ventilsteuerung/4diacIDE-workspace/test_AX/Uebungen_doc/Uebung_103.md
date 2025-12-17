Hier ist die Dokumentation für die Übung 103, basierend auf den bereitgestellten Daten.

# Uebung_103

![Uebung_103 Bild](Uebung_103.png)

* * * * * * * * * *

## Einleitung
Die **Uebung_103** demonstriert die dynamische Umschaltung von Steuerungslogiken mittels Adapter-Technologie. Ziel ist es, das Verhalten zwischen einem digitalen Eingang (`DigitalInput_I1`) und einem digitalen Ausgang (`DigitalOutput_Q1`) basierend auf einer numerischen Auswahl (`InputNumber_I1`) zu verändern. Dabei kommen Adapter-Multiplexer und -Demultiplexer zum Einsatz, um Signale durch verschiedene logische Sub-Applikationen zu leiten.

## Verwendete Funktionsbausteine (FBs)

In dieser Übung werden verschiedene Hauptbausteine zur Signalverarbeitung und Adapter-Steuerung verwendet:

*   **logiBUS::io::DI::logiBUS_IXA** (`DigitalInput_I1`): Repräsentiert den physischen digitalen Eingang (Hardware).
*   **logiBUS::io::DQ::logiBUS_QXA** (`DigitalOutput_Q1`): Repräsentiert den physischen digitalen Ausgang (Hardware).
*   **isobus::UT::io::NumericValue::NumericValue_ID** (`InputNumber_I1`): Liefert den Auswahlwert (ID) zur Steuerung des Programmablaufs.
*   **iec61131::conversion::F_DWORD_TO_UDINT** (`C1`): Konvertiert den Datentyp DWORD zu UDINT.
*   **iec61131::conversion::F_UDINT_TO_UINT** (`C2`): Konvertiert den Datentyp UDINT zu UINT (notwendig für die Selektor-Eingänge der MUX/DEMUX Bausteine).
*   **adapter::selection::unidirectional::AX_DEMUX_3** (`AX_DEMUX_3`): Ein Adapter-Demultiplexer, der eine eingehende Adapter-Verbindung auf einen von drei Ausgängen schaltet.
*   **adapter::selection::unidirectional::AX_MUX_3** (`AX_MUX_3`): Ein Adapter-Multiplexer, der eine von drei eingehenden Adapter-Verbindungen auf einen Ausgang schaltet.

### Sub-Bausteine (Instanziierte SubApps)

In dieser Übung werden drei spezifische Sub-Applikationen instanziiert, die die eigentliche Logik beinhalten. Da deren interner Aufbau hier nicht explizit vorliegt, wird ihre Funktion anhand ihres Namens und der Verwendung beschrieben.

### Sub-Baustein: tastend
*   **Typ**: `MyLib::sys::tastend`
*   **Verwendung**: Kanal 1 (Auswahlwert 1)
*   **Funktionsweise**: Dieser Baustein realisiert eine direkte Weitergabe des Signals (Tastfunktion). Der Ausgang ist aktiv, solange der Eingang aktiv ist.

### Sub-Baustein: rastend
*   **Typ**: `MyLib::sys::rastend`
*   **Verwendung**: Kanal 2 (Auswahlwert 2)
*   **Funktionsweise**: Dieser Baustein realisiert eine Speicherfunktion (z.B. Stromstoßschalter/Toggle-Funktion). Ein Impuls schaltet den Ausgang ein, der nächste schaltet ihn aus.

### Sub-Baustein: tastend_TON_5s
*   **Typ**: `MyLib::sys::tastend_TON_5s`
*   **Verwendung**: Kanal 3 (Auswahlwert 3)
*   **Funktionsweise**: Dieser Baustein kombiniert die Tastfunktion mit einem Zeitglied (TON - Timer On Delay). Vermutlich wird das Signal erst nach einer Verzögerung von 5 Sekunden durchgeschaltet.

## Programmablauf und Verbindungen

Der Ablauf der Übung lässt sich in drei Bereiche unterteilen: die Selektion, das Routing und die Logikverarbeitung.

1.  **Selektion des Betriebsmodus**:
    *   Der Baustein `InputNumber_I1` liefert einen numerischen Wert.
    *   Dieser Wert durchläuft eine Konvertierungskette (`C1` und `C2`), um von einem universellen Format in einen `UINT` (Unsigned Integer) gewandelt zu werden.
    *   Der resultierende Wert wird an die Eingänge `K` (Selektor) von `AX_DEMUX_3` und `AX_MUX_3` geleitet. Dieser Wert bestimmt, welcher Pfad (1, 2 oder 3) aktiv ist.

2.  **Signal-Routing mittels Adapter**:
    *   Das Signal vom digitalen Eingang (`DigitalInput_I1`) wird über eine Adapter-Verbindung an den Eingang des `AX_DEMUX_3` gelegt.
    *   Abhängig vom Selektor-Wert `K` leitet der Demultiplexer die Verbindung an einen der drei Sub-Bausteine (`tastend`, `rastend` oder `tastend_TON_5s`) weiter.
    *   Nach der Verarbeitung in der jeweiligen SubApp wird das Signal an den entsprechenden Eingang des `AX_MUX_3` geführt.
    *   Der Multiplexer wählt (ebenfalls gesteuert durch `K`) das Signal der aktiven SubApp aus und leitet es an den digitalen Ausgang (`DigitalOutput_Q1`) weiter.

3.  **Logische Pfade**:
    *   **K=1**: Der Pfad führt durch die SubApp `tastend`. Verhalten: Der Ausgang folgt direkt dem Eingang.
    *   **K=2**: Der Pfad führt durch die SubApp `rastend`. Verhalten: Der Eingang schaltet den Ausgang wechselweise an und aus.
    *   **K=3**: Der Pfad führt durch die SubApp `tastend_TON_5s`. Verhalten: Der Ausgang schaltet zeitverzögert (5s).

## Zusammenfassung
Die Übung 103 ist ein fortgeschrittenes Beispiel für die Nutzung von Adaptern in 4diac. Sie zeigt anschaulich, wie man Hardware-Eingänge und -Ausgänge flexibel mit unterschiedlichen Logik-Modulen verknüpfen kann, ohne die physische Verdrahtung zu ändern. Durch die Wahl einer Zahl am `InputNumber_I1` kann der Benutzer zur Laufzeit entscheiden, ob sich die Schaltung wie ein Taster, ein Schalter (rastend) oder ein Zeitschalter verhält.