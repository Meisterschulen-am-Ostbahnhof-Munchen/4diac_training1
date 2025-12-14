# Uebung_031: LED Strip

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung eines LED-Streifens mit Farbkonvertierung und Tastersteuerung. Die Anwendung ermöglicht die Umwandlung von HSV-Farbwerten in RGB-Werte und die anschließende Ansteuerung einzelner Pixel auf einem LED-Streifen.

## Verwendete Funktionsbausteine (FBs)

### DigitalInput_CLK_I1
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I1
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### DigitalInput_CLK_I2
- **Typ**: logiBUS_IE
- **Parameter**:
  - QI = TRUE
  - Input = logiBUS_DI::Input_I2
  - InputEvent = logiBUS_DI_Events::BUTTON_SINGLE_CLICK

### hsv2rgb
- **Typ**: hsv2rgb
- **Parameter**:
  - hue = 100
  - saturation = 100
  - value = 100

### strip_set_pixel
- **Typ**: strip_set_pixel
- **Parameter**:
  - index = LED_strip::Output_strip

## Programmablauf und Verbindungen

Das Programm verwendet zwei digitale Eingänge (I1 und I2) als Taster mit Einzelklick-Erkennung. Der Taster I1 löst über das IND-Ereignis die Farbkonvertierung im hsv2rgb-Baustein aus. Nach erfolgreicher Konvertierung (CNF-Ereignis) werden die RGB-Werte an den strip_set_pixel-Baustein weitergegeben.

**Ereignisverbindungen:**
- DigitalInput_CLK_I2.IND → strip_set_pixel.clear
- hsv2rgb.CNF → strip_set_pixel.set_pixel
- DigitalInput_CLK_I1.IND → hsv2rgb.REQ

**Datenverbindungen:**
- hsv2rgb.r → strip_set_pixel.red
- hsv2rgb.g → strip_set_pixel.green
- hsv2rgb.b → strip_set_pixel.blue

Der Taster I2 dient zum Löschen des LED-Streifens über den clear-Eingang. Die HSV-Parameter sind fest auf Werte von 100 voreingestellt, was eine spezifische Farbe erzeugt.

## Zusammenfassung
Diese Übung vermittelt praktische Erfahrungen mit Farbkonvertierung (HSV zu RGB) und der Ansteuerung von LED-Streifen. Sie zeigt die Verwendung von digitalen Eingängen zur Steuerung von Ausgabefunktionen und demonstriert die Datenübertragung zwischen verschiedenen Funktionsbausteinen in einem verteilten Steuerungssystem.