# logiBUS_AI_ID / logiBUS_AI_IDA - Offene Punkte

## TODO: Roh-Vollausschlag von `IN` (DWORD) noch nicht im Baustein/in der Doku vermerkt

`logiBUS_AI_ID.fbt` (und der Adapter-Wrapper `logiBUS_AI_IDA.fbt`) liefern den
Analogwert als `IN : DWORD` — aber weder die `Identification`/`Comment`-Texte
der beiden Bausteine noch die Hardware-Doku (`APIXON_Node-ISO_20.md`) nennen
bisher den tatsächlichen Roh-Vollausschlag (Bit-Breite/Maximalwert).

**Für das geplante AI-Sample (8 Analog-Eingänge, Prozent-Skalierung 0-100%)
wird dieser Wert als Skalierungs-Nenner gebraucht.**

### Wert bestätigt ✅: 0-4095 (12 bit), fix — kein Konfigurationsspielraum

Direkt bei Espressif nachgesehen (ESP-IDF, `components/soc/esp32p4/include/soc/soc_caps.h`):

```c
#define SOC_ADC_DIGI_MIN_BITWIDTH   (12)
#define SOC_ADC_DIGI_MAX_BITWIDTH   (12)
```

`MIN` und `MAX` sind auf dem ESP32-P4 identisch — im hier verwendeten
Continuous/DMA-Modus (`adc_continuous_*`) gibt es also gar keine Bandbreite
zur Auswahl, 12 bit ist der einzig mögliche Wert, nicht nur das Maximum.

Firmware-Beleg: `C:\git\hr\LOGIBUS_integration_datapanel\4diac-forte\logiBUS-modules\logiBUS-io\handle\esp32_analog_in\IOHandleESP32AnalogIN.cpp:31`
setzt `#define ADC_BIT_WIDTH SOC_ADC_DIGI_MAX_BITWIDTH` — genau dieser Handle
steht hinter `logiBUS_AI_ID`/`logiBUS_AI_IDA` (`logiBUS_AI_ID_fbt.cpp` ruft
`mapPin()` → `logiBUSAnalogInHandleDescriptor` → dieser Handle).

**Damit: `IN`-Rohwert liegt im Bereich 0-4095.**

Bonus (offizielle ESP-IDF-Doku, ADC Continuous Mode Driver): Umrechnung
Rohwert → Volt, falls für eine spätere Kalibrierungs-/Volt-Anzeige gebraucht:

```
Vout = Dout × Vmax / Dmax      (Dmax = 2^bitwidth = 4096)
```

`Vmax` hängt von der ADC-Dämpfung ab (`ADC_ATTEN_DB_12`, siehe
`IOHandleESP32AnalogIN.cpp:30`) — Vmax-Wert selbst noch nicht recherchiert,
erst relevant für die spätere Kalibrierungsfunktion (physikalische
Sensor-Grenzen, "Schritt 2" laut Nutzer).

Frühere Ableitung (jetzt durch obigen Fund bestätigt, nicht mehr nur
Vermutung): zwei unabhängige Übungen (`test_B/Uebungen/Uebung_034.SUB`,
`test_AX/Uebungen/Uebung_034_AD.SUB`) skalieren `AnalogInput_I7` mit ×2
(`F_SHL`/`AD_SHL`) auf `PWMOutput_Q4.OUT` (`logiBUS_QD_PWM`/`logiBUS_QDA_PWM`),
dessen Bereich empirisch als 0-8191 bekannt ist — rechnerisch exakt
konsistent mit einem nativen 0-4095-Eingangsbereich.

### Noch zu erledigen (im Baustein + in der Doku festhalten)

1. ~~Realen Wert bestätigen~~ ✅ erledigt (siehe oben).
2. **Im Baustein dokumentieren:** `Identification`/`Comment` von
   `logiBUS_AI_ID.fbt` und `logiBUS_AI_IDA.fbt` um den Wertebereich
   `IN = 0-4095 (12 bit, fix, kein Auswahlspielraum im Continuous-Mode)`
   ergänzen (analog zu anderen Bausteinen in diesem Repo, die ihren
   Wertebereich explizit nennen, z.B.
   `eclipse4diac::signalprocessing::FIELDBUS_SIGNAL::VALID_SIGNAL_W`).
3. **In der Hardware-Doku ergänzen:**
   `C:\git2\ms\visual-programming-languages-docs\docs\de\hw\logiBUS\APIXON_Node-ISO_20.md`,
   Abschnitt "Analoge Eingänge" — Vollausschlag-Rohwert (0-4095, 12 bit,
   ESP32-P4-ADC-Continuous-Mode-Fixwert) pro Kanal ergänzen (aktuell nur
   Pin-Zuordnung + ADC-Kanal-Namen, kein Wertebereich).

## Änderungshistorie

### 2026-08-30
- TODO angelegt im Rahmen der Planung des AI-Samples (8 Analog-Eingänge,
  Vorlage: DIDO-Sample, DO-Seite bleibt unverändert).
- Roh-Vollausschlag bestätigt (0-4095, 12 bit, fix) über ESP-IDF-Quellcode
  (`soc_caps.h`) und den echten Firmware-Treiber
  (`IOHandleESP32AnalogIN.cpp`) in `C:\git\hr\LOGIBUS_integration_datapanel`.
