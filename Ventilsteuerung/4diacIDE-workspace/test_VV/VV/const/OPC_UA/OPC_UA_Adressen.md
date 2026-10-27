# OPC-UA-Adressen (`myOpcUaAddresses.gcf`)

Die OPC-UA-IDs für die Trainings `test_VV/sys/03_OPC_UA/Training_01` bis `_12`
werden in der GCF aus wenigen Grundwerten berechnet. Die Functions dafür stehen in
der Lib `MyLib_OPC`. Der 4diac-Export wertet sie aus, im Bootfile stehen die fertigen Strings.

## Stationen ändern: nur hier

```
PC_A : WSTRING := logiBUS::stations::Computers::C_11;
PC_B : WSTRING := logiBUS::stations::Computers::C_12;
```

- Die `.sys`-Dateien nutzen `PC_A`/`PC_B` als `MGR_ID`.
- Die OPC-UA-Endpunkte `PC_A_OPC`/`PC_B_OPC` werden daraus mit
  `MyLib_OPC::F_MGR_TO_OPC` abgeleitet (`192.168.1.12:61499` ->
  `opc.tcp://192.168.1.12:4840`).

Eine andere Station, etwa `C_13`, wirkt damit auf Deployment und alle Remote-IDs.

## Aufbau pro Signal

```
Q1_NODE         := "/Objects/DigitalOutput/Q1,1:s=Output_Q1";            // Knoten, einmal
Q1_LOCAL_READ   := MyLib_OPC::F_OPC_LOCAL("READ", Q1_NODE);               // Station, die den Knoten hat
Q1_REMOTE_WRITE := MyLib_OPC::F_OPC_REMOTE("WRITE", PC_B_OPC, Q1_NODE);   // andere Station
```

| Function | Ergebnis |
|---|---|
| `F_OPC_LOCAL(action, node)` | `opc_ua[ACTION;NODE]` |
| `F_OPC_REMOTE(action, endpoint, node)` | `opc_ua[ACTION;ENDPOINT#;NODE]` |

Zusammengehörige Aktionen (siehe 4diac-Doku `opcua.adoc`):

| Lokal | passender FB lokal | Remote | passender FB remote |
|---|---|---|---|
| `READ` | `AX_SUBSCRIBE_1` / `SUBSCRIBE_n` | `WRITE` | `CLIENT_n_0` |
| `CREATE_METHOD` | `SERVER_0` | `CALL_METHOD` | `CLIENT_0` |

- Der Name-Suffix `*_LOCAL_*`/`*_REMOTE_*` ist geblieben, damit die SubApps
  unverändert weiterlaufen.
- `SW2_*` bündelt zwei Knoten in einem String (mit `;` getrennt) für `SUBSCRIBE_2`/`CLIENT_2_0`.

## Hinweise

- `Comment=` in der GCF kurz halten, sonst schneidet der Resave der IDE lange
  Kommentare ab. Ausführliches gehört in diese Datei.
- Geprüft: Die Bootfiles von Training_01 (PC_A und PC_B) sind vor und nach der Umstellung byte-identisch.
