# Uebung_014: Container (visible/invisible)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Steuerung der Sichtbarkeit eines Containers über Softkeys auf einem Bedienpanel. Die Übung zeigt die Verwendung von Ereignisverarbeitung und Zustandssteuerung in 4diac.

## Verwendete Funktionsbausteine (FBs)

### Softkey_IE Bausteine
- **SoftKey_UP_F1**: Softkey-Interface für Funktionstaste F1
- **SoftKey_UP_F2**: Softkey-Interface für Funktionstaste F2

### E_SR Baustein
- **Typ**: E_SR (Set-Reset Flip-Flop)
- **Funktionsweise**: Verarbeitet Set- und Reset-Ereignisse und gibt einen stabilen Zustand Q aus

### Q_ObjHideShow Baustein
- **Typ**: Q_ObjHideShow
- **Funktionsweise**: Steuert die Sichtbarkeit eines grafischen Objekts auf dem Bedienpanel

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → E_SR.S (Set-Eingang)
- SoftKey_UP_F2.IND → E_SR.R (Reset-Eingang)  
- E_SR.EO → Q_ObjHideShow.REQ (Ausführungsanforderung)

**Datenverbindungen:**
- E_SR.Q → Q_ObjHideShow.qVisible (Sichtbarkeitsstatus)

**Parameterkonfiguration:**
- SoftKey_UP_F1: u16ObjId = "DefaultPool::SoftKey_F1", InputEvent = "SK_RELEASED"
- SoftKey_UP_F2: u16ObjId = "DefaultPool::SoftKey_F2", InputEvent = "SK_RELEASED"
- Q_ObjHideShow: u16ObjId = "DefaultPool::Container_B"

**Funktionsweise:**
- F1-Taste setzt den Flip-Flop und macht den Container sichtbar
- F2-Taste resetet den Flip-Flop und versteckt den Container
- Der E_SR Baustein sorgt für einen stabilen Zustand zwischen den Tastendrücken

## Zusammenfassung
Diese Übung vermittelt grundlegende Konzepte der Ereignisverarbeitung und Zustandssteuerung in 4diac. Sie zeigt, wie Softkey-Ereignisse verarbeitet und zur Steuerung grafischer Elemente verwendet werden können. Die Verwendung des E_SR Bausteins demonstriert eine einfache Speicherfunktion für binäre Zustände.