# Uebung_013: SR-Flip-Flop (Softkey)

* * * * * * * * * *

## Einleitung
Diese Übung demonstriert die Funktionsweise eines SR-Flip-Flops (Set-Reset-Flip-Flop) mit Softkey-Bedienung. Das SR-Flip-Flop ist ein grundlegender Speicherbaustein in der digitalen Schaltungstechnik, der zwei stabile Zustände einnehmen kann.

## Verwendete Funktionsbausteine (FBs)

### E_SR
- **Typ**: E_SR (SR-Flip-Flop)
- **Funktionsweise**: Der E_SR Baustein realisiert ein SR-Flip-Flop mit Ereignissteuerung. Er verfügt über Set(S)- und Reset(R)-Eingänge sowie einen Ausgang Q, der den gespeicherten Zustand ausgibt.

### Softkey_IE
- **Typ**: Softkey_IE (Softkey Input Event)
- **Verwendete Instanzen**:
  - **SoftKey_UP_F1**: Softkey F1 für Set-Operation
    - Parameter: u16ObjId = DefaultPool::SoftKey_F1
    - Parameter: InputEvent = SoftKeyActivationCode::SK_RELEASED
    - Ereignisausgang: IND
  - **SoftKey_UP_F2**: Softkey F2 für Reset-Operation
    - Parameter: u16ObjId = DefaultPool::SoftKey_F2
    - Parameter: InputEvent = SoftKeyActivationCode::SK_RELEASED
    - Ereignisausgang: IND

### logiBUS_QX
- **Typ**: logiBUS_QX (Digital Output)
- **Verwendete Instanzen**:
  - **DigitalOutput_Q1**: Digitaler Ausgang Q1
    - Parameter: QI = TRUE
    - Parameter: Output = logiBUS_DO::Output_Q1
    - Ereigniseingang: REQ
    - Dateneingang: OUT

## Programmablauf und Verbindungen

**Ereignisverbindungen:**
- SoftKey_UP_F1.IND → E_SR.S (Set-Eingang)
- SoftKey_UP_F2.IND → E_SR.R (Reset-Eingang)
- E_SR.EO → DigitalOutput_Q1.REQ

**Datenverbindungen:**
- E_SR.Q → DigitalOutput_Q1.OUT

**Funktionsweise:**
- Beim Drücken und Loslassen der Softkey-Taste F1 wird ein Set-Signal an den E_SR Baustein gesendet
- Beim Drücken und Loslassen der Softkey-Taste F2 wird ein Reset-Signal an den E_SR Baustein gesendet
- Der Ausgang Q des SR-Flip-Flops steuert den digitalen Ausgang Q1
- Das System behält seinen Zustand bei, bis ein gegenteiliges Signal empfangen wird

**Lernziele:**
- Verständnis der SR-Flip-Flop Funktionsweise
- Umgang mit Softkey-Inputs in 4diac
- Ereignisgesteuerte Programmierung
- Zustandsspeicherung in Funktionsbausteinen

**Schwierigkeitsgrad**: Einsteiger

## Zusammenfassung
Diese Übung vermittelt die grundlegende Funktionsweise eines SR-Flip-Flops mit Softkey-Bedienung. Der Baustein E_SR speichert den Zustand und gibt ihn über den digitalen Ausgang Q1 aus. Die Softkeys F1 und F2 dienen als Set- bzw. Reset-Eingänge und demonstrieren die ereignisgesteuerte Zustandsänderung des Flip-Flops.