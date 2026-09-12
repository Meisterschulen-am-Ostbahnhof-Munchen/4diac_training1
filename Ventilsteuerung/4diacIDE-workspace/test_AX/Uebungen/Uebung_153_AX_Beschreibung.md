# Übung 153 AX: Impulszähler & PID-Regler mit Adapter-Kopplung

## Thema: Drehzahl-/Frequenzregelung mit Impulszähler und PID-Regler

### Situationsbeschreibung

In landtechnischen Anwendungen (z. B. Säwellenantrieb, Düngerstreuer-Dosierscheibe, Lüfterdrehzahlsteuerung) muss eine Drehzahl oder Impulsfrequenz gemessen und über einen PID-Regler (`CTRL_PID`) auf einen Sollwert geregelt werden. Die Stellgröße wird als PWM-Signal an einem digitalen Leistungsausgang (`Output_Q1`) ausgegeben.

### Funktionsbeschreibung

- **Erfassung:** Über den Pulse-Input-Adapterbaustein `logiBUS_PI_IDA` an `PulseInput_I8` werden Zählimpulse zyklisch (getriggert durch `E_CYCLE` alle 200 ms via `I2` Start / `I3` Stopp) erfasst.
- **Signalaufbereitung:** Der Impulswert wird über `AD_D_TO_DWORD` -> `F_DWORD_TO_UDINT` -> `F_UDINT_TO_REAL` konvertiert und mit `FT_DERIV_10` differenziert, um die aktuelle Frequenz/Drehzahl (`ACT`) zu bestimmen.
- **Regelung:** Der PID-Regler `CTRL_PID` vergleicht den Istwert (`ACT`) mit dem Sollwert (`SET = 16.0`). Über Taster `I1` (via `AX_T_FF` und `AX_X_TO_BOOL`) kann zwischen Automatik- und Handbetrieb (`MAN`) umgeschaltet werden.
- **Stellgrößenausgabe:** Die Stellgröße `Y` des Reglers wird von `LREAL` über `F_LREAL_TO_UDINT` in die Adapterkette `AUDI_UDINT_TO_UDI` -> `AUDI_TO_AD` konvertiert und an den PWM-Ausgangbaustein `PWMOutput_Q1` (`logiBUS_QDA_PWM`) auf `Output_Q1` übergeben.

### Referenzlösung
`Uebung_153_AX.SUB` — validiert in 4diac IDE.
