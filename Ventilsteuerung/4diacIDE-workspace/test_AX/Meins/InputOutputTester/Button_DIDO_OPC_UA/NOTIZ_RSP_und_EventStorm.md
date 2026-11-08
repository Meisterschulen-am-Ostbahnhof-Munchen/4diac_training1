# Notiz: RSP bei SUBSCRIBE_1 und der Event-Storm (Q1–Q12 OPC-UA-Test)

Schmierzettel für die Doku – Ergebnis einer Quellcode-Prüfung in
`4diac-forte` (Repo `LOGIBUS_integration_datapanel`, Pfad
`4diac-forte/core/src/cominfra/commfb.cpp`).

## Symptom

Beim Testen des OPC-UA-Schreibpfads für Q1–Q12
(`Button_IXA_TO_logiBUS_QXA_BG_OPC`) trat ein Event-Storm auf:
`SUBSCRIBE_1.IND` und `PUBLISH_1.REQ` feuerten ununterbrochen.

## Falsche erste Vermutung (verworfen)

Erste Annahme: `SUBSCRIBE_1` bräuchte ein explizit ausgelöstes `RSP`-Event
zur Quittierung jeder empfangenen Indikation, und der Storm käme daher,
dass diese Quittierung in der ursprünglichen Verdrahtung fehlte.

**Das ist falsch und durch den Quellcode widerlegt.**

## Tatsächlicher Befund (Quellcode-geprüft)

In `CCommFB::sendData()` (`commfb.cpp`), der Funktion, die durch das
`RSP`-Event ausgelöst wird (`scmSendNotificationEventID`):

```cpp
EComResponse CCommFB::sendData() {
  EComResponse resp = e_Nothing;
  if (true == QI()) {
    if (mCommServiceType != e_Subscriber) {
      // eigentliches Senden passiert nur hier
      ...
    }
  } else {
    resp = e_ProcessDataInhibited;
  }
  return resp;
}
```

Für `SUBSCRIBE_1` ist `mCommServiceType == e_Subscriber`. Die Bedingung
`!= e_Subscriber` ist damit **falsch**, der gesamte innere Block wird
übersprungen, `resp` bleibt `e_Nothing`. In `executeEvent()` löst
`e_Nothing` **keinen** `sendOutputEvent(...)` aus.

**`RSP` ist für `SUBSCRIBE_1` (Service-Typ Subscriber) ein kompletter
No-Op.** Das Event-Input-Paar `INIT`/`RSP` existiert nur, weil
`CCommFB` die gemeinsame Basisklasse für alle „Responder"-artigen
Dienst-FBs ist (z. B. `SERVER`, wo `RSP` eine echte Methodenantwort
auslöst) – bei `SUBSCRIBE` ist der Zweig tot.

## Echte Ursache des Event-Storms

Feedback-Loop: `SUBSCRIBE_1` beobachtet denselben OPC-UA-Knoten, den
`PUBLISH_1` (im selben Prozess/Adressraum) beschreibt. Jede eigene
Veröffentlichung erscheint für `SUBSCRIBE_1` wie eine externe Änderung
und löst erneut `IND` aus → erneutes `PUBLISH_1.REQ` → erneute
Veröffentlichung → usw.

## Angewendeter Fix

**Übergangsweise** (Commit `68cfb466`, klar als `INTERIM FIX`
gekennzeichnet): ein `AX_D_FF` (Adapter-Ebenen-Flipflop) auf beiden
Seiten des gemeinsamen `AX_OR_2` in `Button_IXA_TO_logiBUS_QXA_BG_OPC`,
um die unmittelbare Rückkopplung zu entkoppeln.

**Geplanter sauberer Fix**: die neuen Wrapper-Bausteine
`adapter::net::AX_PUBLISH_1` / `AX_SUBSCRIBE_1`
(`.lib/adapter-3.0.0/typelib/net/`), die intern ein echtes
ereignisbasiertes `iec61499::events::E_D_FF` statt der
Adapter-Ebenen-Krücke verwenden und `PUBLISH_1`/`SUBSCRIBE_1` inklusive
BOOL↔Adapter-Konvertierung sauber kapseln. Einbau in die
Composite-Bausteine steht noch aus.

## Quellen

- `4diac-forte/core/src/cominfra/commfb.cpp` – `CCommFB::sendData()`,
  `CCommFB::executeEvent()`
- `4diac-forte/core/src/cominfra/commfb.cpp` (Zeilen ~35–39) – Event-Namen
  je Rolle: Responder = `INIT`/`RSP` → `INITO`/`IND`
- `4diac-forte/stdfblib/net/src/GEN_SUBSCRIBE_fbt.cpp` – `evt_RSP()` →
  `scmSendNotificationEventID`
