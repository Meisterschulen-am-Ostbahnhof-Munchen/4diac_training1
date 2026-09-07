# Bootfile-Erstellung und das OPC-UA-Profil

🇩🇪 Deutsch | 🇬🇧 [English](OPCUA_Bootfile_Workaround.en.md)

## Symptom

Beim Ausführen von **Create boot-files** in 4diac IDE auf einem Gerät, dessen
Attribut `Profile` auf `OPC UA` steht, kommt es zu einem
Verbindungs-/Device-Management-Fehler (der Device-Management-Interactor
versucht, die Steuerung zu erreichen) — obwohl das Erstellen einer Bootdatei
eigentlich ein rein lokaler Offline-Vorgang sein soll. Derselbe Export
funktioniert problemlos, wenn `Profile` auf `HOLOBLOC` gesetzt ist.

Betrifft z. B.
`Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`.

## Ursache

Bootdateien werden erzeugt, indem der normale Deployment-Prozess einmal
gegen einen internen Puffer statt gegen eine echte Verbindung ausgeführt
wird (`BootFileDeviceManagementCommunicationHandler`, ein
`AbstractFileManagementHandler`) und dieser Puffer anschließend auf die
Festplatte geschrieben wird. Welcher `IDeviceManagementInteractor` dabei
verwendet wird, ergibt sich aus dem Attribut `Profile` des Geräts:

* `HOLOBLOC` → `DefaultDevMgmInteractorProvider` → `DeploymentExecutor`,
  der den übergebenen Override-Communication-Handler korrekt verwendet und
  daher reinen Text schreibt, statt mit einem Gerät zu kommunizieren.
* `OPC UA` → `OPCUADevMgmtInteractorProvider` → `OPCUADeploymentExecutor`,
  der den Override-Handler ignoriert und immer einen echten `OpcUaClient`
  aufbaut. Dessen Konstruktor ruft sofort
  `DiscoveryClient.getEndpoints(...)` gegen die konfigurierte
  Management-Adresse des Geräts auf — es wird also immer eine erreichbare
  Steuerung vorausgesetzt, selbst für einen reinen Datei-Export.

Bootdateien selbst sind nur das klassische FORTE-Zeilenprotokoll; dieses
Format hängt nicht davon ab, welches Management-Protokoll das Gerät zur
Laufzeit tatsächlich verwendet.

## Workaround (4diac-IDE-Versionen ohne den Fix unten)

1. In den Geräte-Eigenschaften `Profile` vorübergehend auf `HOLOBLOC` setzen.
2. **Create boot-files** ausführen.
3. `Profile` für das echte Deployment/Monitoring wieder auf `OPC UA` setzen.

## Fix

Behoben im 4diac-ide-Quellcode (Branch `OPC-UA-Bootfile`):
`BootFileDeviceManagementCommunicationHandler.createBootFile` erzwingt beim
Aufruf des Deployment-Coordinators jetzt immer das Profil `HOLOBLOC`,
unabhängig vom konfigurierten `Profile` des Geräts. Der Bootdatei-Export
verwendet daher immer den dateifähigen Interactor, sodass für Geräte mit
`OPC UA`-Profil der manuelle Profilwechsel oben nicht mehr nötig ist und
keine Netzwerkverbindung zur Bootdatei-Erstellung erforderlich ist. Bis ein
4diac-IDE-Build mit diesem Fix hier installiert ist, den Workaround oben
verwenden.
