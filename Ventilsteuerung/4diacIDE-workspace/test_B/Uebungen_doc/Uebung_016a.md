# Uebung_016a: Background Colour umschalten -- 3-fach

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Umschaltung der Hintergrundfarbe eines Displays über drei verschiedene Softkeys. Bei Betätigung der Tasten F1, F2 und F3 wird jeweils eine andere Hintergrundfarbe aktiviert.

## Verwendete Funktionsbausteine (FBs)

### Softkey_IE
- **Typ**: Eingabebaustein für Softkeys
- **Parameter**:
  - QI = TRUE (aktiviert den Baustein)
  - u16ObjId = Spezifische Softkey-ID (F1, F2, F3)
  - InputEvent = SK_RELEASED (Tastenloslassen als Auslöser)

### F_SEL_E_3
- **Typ**: 3-fach Selektor-Baustein
- **Parameter**:
  - IN0 = COLOR_WHITE
  - IN1 = COLOR_GREEN  
  - IN2 = COLOR_RED
- **Funktionsweise**: Wählt basierend auf dem aktivierten REQ-Eingang den entsprechenden Farbwert aus

### Q_BackgroundColour
- **Typ**: Ausgabebaustein für Hintergrundfarbe
- **Parameter**:
  - u16ObjId = DefaultPool::SoftKey_F7 (Display-Objekt für Hintergrundfarbe)

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → F_SEL.REQ0 (löst weiße Farbe aus)
- SoftKey_UP_F2.IND → F_SEL.REQ1 (löst grüne Farbe aus) 
- SoftKey_UP_F3.IND → F_SEL.REQ2 (löst rote Farbe aus)
- F_SEL.CNF → Q_BackgroundColour.REQ (startet Farbänderung)

**Datenverbindungen:**
- F_SEL.OUT → Q_BackgroundColour.u8Colour (übergibt selektierte Farbe)

**Ablauf:**
1. Betätigung einer Softkey-Taste (F1, F2 oder F3)
2. F_SEL-Baustein selektiert entsprechende Farbe
3. Q_BackgroundColour setzt die Hintergrundfarbe auf dem Display

## Zusammenfassung
Diese Übung zeigt die grundlegende Steuerung von Display-Eigenschaften über Softkeys. Die dreifache Farbauswahl demonstriert die Verwendung von Selektionsbausteinen und die Zuordnung von Eingabeereignissen zu spezifischen Ausgabefunktionen.