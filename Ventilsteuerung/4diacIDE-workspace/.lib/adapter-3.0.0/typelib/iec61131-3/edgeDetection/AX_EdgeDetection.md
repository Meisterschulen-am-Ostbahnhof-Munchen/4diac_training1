# AX Edge Detection FBs

This document describes the relationship between the standard IEC 61131-3 Edge Detection Function Blocks and their AX-Adapter-based counterparts.

## 1. Overview

The standard FBs work with discrete Event and Boolean inputs/outputs (`REQ`/`CNF`, `CLK`/`Q`).
The AX FBs encapsulate this logic but interface exclusively via `AX` Adapters (Unidirectional), making them suitable for plug-and-play in AX-based adapter networks without manual event/data wiring.

## 2. Comparison

### Rising Edge (R_TRIG)

| Feature | `FB_R_TRIG` (Standard) | `AX_FB_R_TRIG` (Adapter) |
| :--- | :--- | :--- |
| **Package** | `iec61131::edgeDetection` | `adapter::iec61131::edgeDetection` |
| **Type Class** | `SimpleFB` | `BasicFB` |
| **Interface** | Events: `REQ`, `CNF`<br>Data: `CLK` (IN), `Q` (OUT) | Sockets: `CLK` (Type `AX`)<br>Plugs: `Q` (Type `AX`) |
| **Triggering** | Explicit `REQ` event. | Event `E1` arriving on `CLK` socket. |
| **Logic** | `Q := CLK AND NOT MEM;` | `Q.D1 := CLK.D1 AND NOT MEM;` |
| **Output** | `CNF` event + `Q` data. | `Q.E1` event + `Q.D1` data. |

### Falling Edge (F_TRIG)

| Feature | `FB_F_TRIG` (Standard) | `AX_FB_F_TRIG` (Adapter) |
| :--- | :--- | :--- |
| **Package** | `iec61131::edgeDetection` | `adapter::iec61131::edgeDetection` |
| **Type Class** | `SimpleFB` | `BasicFB` |
| **Interface** | Events: `REQ`, `CNF`<br>Data: `CLK` (IN), `Q` (OUT) | Sockets: `CLK` (Type `AX`)<br>Plugs: `Q` (Type `AX`) |
| **Triggering** | Explicit `REQ` event. | Event `E1` arriving on `CLK` socket. |
| **Logic** | `Q := NOT CLK AND NOT MEM;` | `Q.D1 := NOT CLK.D1 AND NOT MEM;` |
| **Output** | `CNF` event + `Q` data. | `Q.E1` event + `Q.D1` data. |

## 3. Usage Differences in Exercises

*   **Standard Exercise (`Uebung_177` / `Uebung_178`)**:
    *   Uses standard IO blocks (`logiBUS_IX`, `logiBUS_QX`).
    *   Requires explicit wiring of `IND` -> `REQ` (Events) and `IN` -> `CLK` (Data).
    *   Requires wiring of `CNF` -> `REQ` (next block) and `Q` -> `IN` (next block).

*   **AX Exercise (`Uebung_177_AX` / `Uebung_178_AX`)**:
    *   Uses Adapter IO blocks (`logiBUS_IXA`, `logiBUS_QXA`).
    *   Wiring is done via single `AdapterConnections` (Green lines).
    *   `IXA` Adapter -> `CLK` Socket on TRIG.
    *   `Q` Plug on TRIG -> `QXA` Adapter (or next block's socket).
    *   No separate Event/Data lines are needed for the trigger logic itself.