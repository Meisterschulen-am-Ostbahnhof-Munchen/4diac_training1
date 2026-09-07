# Boot File Creation and the OPC UA Profile

🇩🇪 [Deutsch](OPCUA_Bootfile_Workaround.md) | 🇬🇧 English

## Symptom

Using **Create boot-files** in 4diac IDE on a device whose `Profile`
attribute is set to `OPC UA` fails with a connection/device-management error
(the device management interactor tries to reach the controller), even
though creating a boot file is meant to be a fully offline operation. The
same export works without any issue when `Profile` is set to `HOLOBLOC`.

Affects e.g. `Ventilsteuerung/4diacIDE-workspace/test_AX/sys/Training_AX/test_AX.sys`.

## Root cause

Boot files are exported by running the normal deployment process once
against an in-memory buffer instead of a live connection
(`BootFileDeviceManagementCommunicationHandler`, an
`AbstractFileManagementHandler`) and then writing that buffer to disk. Which
`IDeviceManagementInteractor` is used for that run is selected via the
device's `Profile` attribute:

* `HOLOBLOC` → `DefaultDevMgmInteractorProvider` → `DeploymentExecutor`,
  which correctly honors the override communication handler and therefore
  writes plain text instead of talking to a device.
* `OPC UA` → `OPCUADevMgmtInteractorProvider` → `OPCUADeploymentExecutor`,
  which ignores the override handler and always builds a real
  `OpcUaClient`. Its constructor immediately calls
  `DiscoveryClient.getEndpoints(...)` against the device's configured
  management address, i.e. it always requires a reachable controller, even
  for a plain file export.

Boot files themselves are just the classic FORTE line protocol; that format
does not depend on which management protocol the device uses at runtime.

## Workaround (4diac IDE versions without the fix below)

1. Open the device's properties and temporarily set `Profile` to `HOLOBLOC`.
2. Run **Create boot-files**.
3. Set `Profile` back to `OPC UA` for live deployment/monitoring.

## Fix

Fixed in the 4diac-ide source (`OPC-UA-Bootfile` branch):
`BootFileDeviceManagementCommunicationHandler.createBootFile` now forces the
`HOLOBLOC` profile when invoking the deployment coordinator, regardless of
the device's configured `Profile`. Boot file export therefore always uses
the file-capable interactor, so devices configured for `OPC UA` no longer
need the manual profile switch above, and no network connection is required
to create a boot file. Until a 4diac IDE build containing this fix is
installed here, use the workaround above.
