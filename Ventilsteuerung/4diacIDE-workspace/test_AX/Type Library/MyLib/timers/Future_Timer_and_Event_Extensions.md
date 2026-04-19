# Roadmap: Future Timer and Event Extensions

This document outlines proposed functional blocks to enhance the event-driven capabilities of the library, focusing on safety, process monitoring, and architectural cleanliness.

---

## 1. Pulse Generation: `E_TRAIN` (Already available in 4diac IDE Nightly)
**Status:** Integrated in standard `iec61499::events` in newer 4diac versions.
**Concept:** Generates a specific number of pulses with a defined period.
- **Inputs:** `N` (UINT - Number of pulses), `DT` (TIME).
- **Use Case:** Acoustic error codes (e.g., "beep 3 times"), status LEDs, or step-by-step actuator movement.
- **AX-Variant Idea:** An `AX_TRAIN` could be created to output these pulses directly onto an AX adapter line.

## 2. Monitoring: `E_WATCHDOG`
**Concept:** Monitors the frequency of incoming events.
- **Inputs:** `REQ` (The event to monitor), `PT` (Maximum allowed time between events).
- **Outputs:** `ALARM` (Fires if `PT` expires without a `REQ`).
- **Use Case:** Monitoring communication heartbeats or cyclical sensor updates.
- **Benefit:** Dedicated error handling instead of using standard timers as workarounds.

## 3. Stability: `E_LIMIT_EVENT` (Event Throttle)
**Concept:** Limits the maximum rate of outgoing events.
- **Logic:** If events arrive faster than the defined rate, subsequent events are either dropped or delayed.
- **Use Case:** Debouncing mechanical switches or protecting the CPU from "event storms" caused by faulty sensors.
- **Benefit:** Increases system stability and predictability.

## 4. Maintenance: `E_RUNTIME`
**Concept:** A specialized version of a retentive timer.
- **Logic:** Accumulates time while `IN=TRUE`.
- **Outputs:** Direct `UDINT` values for `HOURS`, `MINUTES`, and `SECONDS`.
- **Use Case:** Service interval monitoring for machinery.
- **Benefit:** Ready-to-use HMI data without manual `TIME-to-UDINT` math.

## 5. Diagnostics: `E_DUR` (Duration Measurement)
**Concept:** Measures the exact time elapsed between two specific events.
- **Inputs:** `START_EV`, `STOP_EV`.
- **Output:** `DURATION` (TIME).
- **Use Case:** Measuring cycle times, network latency, or process speeds.
- **Benefit:** High-precision diagnostics for performance optimization.

## 6. Architecture: `AX_LOGIC` Family
**Concept:** Native adapter-based logic gates.
- **Blocks:** `AX_AND`, `AX_OR`, `AX_NOT`, `AX_XOR`.
- **Logic:** Performs boolean operations directly on `AX` adapter lines (Event + Data).
- **Use Case:** Combining interlock outputs or sensor signals within an AX-based system.
- **Benefit:** Dramatically reduces the number of converter blocks (`AX_X_TO_BOOL`, `AX_BOOL_TO_X`) needed in modern 4diac networks.

---

## Appendix: Excluded Concepts

### `AX_DELAY` (Decided against implementation)
During the design phase, the concept of a pure `AX_DELAY` block was evaluated and discarded for the following reasons:
1. **Data Consistency:** An `AX` adapter bundles an event with a state. Delaying the event while simply passing through the data leads to a "time-of-check vs. time-of-use" conflict. The receiver would process an old event with potentially new, inconsistent data.
2. **Alternative Patterns:** Most requirements for delaying AX-signals are actually state-based. These are already correctly handled by `AX_TON` or `AX_TOF` blocks, which ensure that the event and data remain synchronized according to timer logic.
3. **Architectural Purity:** To maintain the "Single Source of Truth" philosophy of 4diac adapters, pure event delays should remain on dedicated event lines, while logic delays should be handled by state-aware timer blocks.

---

## Conclusion
Adding these blocks will bridge the gap between basic delay functions and complex industrial requirements. While the standard library provides the foundation, these extensions focus on the **real-world challenges** of machine safety and diagnostic visibility.

**Author:** Franz Höpfinger  
**Date:** April 2026
