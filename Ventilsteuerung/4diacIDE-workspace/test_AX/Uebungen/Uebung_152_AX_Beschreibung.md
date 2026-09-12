# Übung 152 AX: Impulszähler & PI-Regler mit Adapter-Kopplung

## Thema: Drehzahl-/Frequenzregelung mit Impulszähler und PI-Regler

### Situationsbeschreibung

In landtechnischen Anwendungen (z. B. Säwellenantrieb, Düngerstreuer-Dosierscheibe, Lüfterdrehzahlsteuerung) muss eine Drehzahl oder Impulsfrequenz gemessen und über einen PI-Regler (`CTRL_PI_AR`) auf einen Sollwert geregelt werden. Die Stellgröße wird als PWM-Signal an einem digitalen Leistungsausgang (`Output_Q1`) ausgegeben.

### Funktionsbeschreibung

- **Erfassung & Wandlung:** Über den Pulse-Input-Adapterbaustein `logiBUS_PI_IDA` an `PulseInput_I8` werden Zählimpulse zyklisch (getriggert durch `E_CYCLE` alle 200 ms via `I2` Start / `I3` Stopp) erfasst und über `AD_TO_AR_NUM` direkt in das REAL-Adapterformat (`AR`) konvertiert.
- **Signalaufbereitung:** Der `AR`-Adapter streamt an `FT_DERIV_10_AR` (`AR_IN`), wo das Signal differenziert wird, um die aktuelle Frequenz/Drehzahl (`AR_OUT`) zu bestimmen.
- **Regelung:** Der PI-Regler-Adapterwrapper `CTRL_PI_AR` vergleicht den Istwert (`AR_ACT`) mit dem Sollwert (`SET = 16.0`). Über Taster `I1` (via `AX_T_FF.Q`) wird direkt über den Adapter-Socket `AX_MAN` zwischen Automatik- und Handbetrieb umgeschaltet.
- **Stellgrößenausgabe:** Die Stellgröße `AR_Y` des Reglers wird über den Konvertierungsbaustein `AR_TO_AD_NUM` direkt an den PWM-Ausgabe-Baustein `PWMOutput_Q1` (`logiBUS_QDA_PWM`) auf `Output_Q1` übergeben.

### Referenzlösung

`Uebung_152_AX.SUB` — validiert in 4diac IDE.
