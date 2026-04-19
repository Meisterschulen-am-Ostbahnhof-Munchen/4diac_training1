# Proposal: New Function Block `E_RTON` (Retentive Timer On-Delay)

## Context
In industrial automation, we often encounter processes that require timing logic which can be "paused" and "resumed" without losing the accumulated time. Standard IEC 61131-3 and IEC 61499 timer blocks like `TON` or `E_TON` are non-retentive: they reset their internal elapsed time immediately when the input signal (`IN`) goes `FALSE`.

While this is perfect for simple delays, it is insufficient for monitoring cumulative processes such as maintenance intervals, total run-time under specific conditions, or processes that are frequently interrupted by safety gates or pauses.

## The Proposal
I propose the addition of a **Retentive Timer On-Delay (`E_RTON`)** function block to the standard event-driven timer library.

### Core Logic
The `E_RTON` accumulates time as long as the enable signal is active. If the signal is removed, the timer "freezes" the current elapsed time and continues from that exact point once the signal returns.

- **Enable (`IN=TRUE`):** Timer runs and accumulates time.
- **Disable (`IN=FALSE`):** Timer pauses. Accumulated time is retained.
- **Target Reached:** Once accumulated time >= `PT`, the output `Q` becomes `TRUE`.
- **Reset (`R`):** The only way to clear the accumulated time and set `Q` back to `FALSE`.

### Interface Definition

#### Event Inputs
- `REQ`: Update/Service request (cycles the internal logic).
- `R`: Reset event. Clears accumulated time and resets output `Q`.

#### Event Outputs
- `CNF`: Confirmation that the internal state or output has been updated.

#### Input Variables
- `IN` (BOOL): Enable signal. If `TRUE`, time is accumulated.
- `PT` (TIME): Preset Time (the duration to reach).

#### Output Variables
- `Q` (BOOL): Output state. `TRUE` if accumulated time >= `PT`.
- `ET` (TIME): Elapsed Time. The currently accumulated duration.

## Use Cases
1. **Maintenance Monitoring:** Accumulate the actual operation time of a motor (only when it is running) and trigger a service alarm after 1000 hours.
2. **Batch Processing:** Monitor the duration of a heating phase that might be paused by an operator opening a lid.
3. **Totalizing Signals:** Measuring the cumulative time a sensor has been in a specific state over a long period.

## Implementation Note for IEC 61499
In an event-driven environment, `E_RTON` would ideally calculate the delta-time between `REQ` events using the system's time stamp or a dedicated clock tick, adding this delta to an internal `CV` (Current Value) only when `IN` is `TRUE`.

---
**Author:** Franz Höpfinger  
**Organization:** HR Agrartechnik GmbH / Meisterschulen am Ostbahnhof  
**Date:** April 2026
