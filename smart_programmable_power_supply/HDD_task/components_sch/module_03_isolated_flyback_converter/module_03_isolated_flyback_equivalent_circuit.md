# Module 3: Galvanically Isolated Uniform 65 kHz Flyback Converter — Equivalent Electronic Circuit

## 1. Subsystem Architectural Overview
Module 3 is the core power transformation and safety isolation engine of the SPPS. It steps down the high-voltage DC bus link (+120.0 V to +375.0 V_DC) to a stable, regulated **+24.0 V_DC ± 1.0%** intermediate power bus (72.0 W continuous, 84.0 W peak), while providing certified **3000 V_AC RMS reinforced galvanic safety isolation** per IEC 62368-1.

## 2. Full Schematic-Level Equivalent Electronic Circuit Diagram

```
 [ MODULE 3: GALVANICALLY ISOLATED UNIFORM 65 kHz FLYBACK CONVERTER ]
=============================================================================================================================

 [PRIMARY HOT DOMAIN: ZONE 1] [SECONDARY SELV TOUCH-SAFE DOMAIN: ZONE 2]
 ─────────────────────────────────────────────────────────────┐ ┌──────────────────────────────────────────────────
 │ │
 Net: +HV_BULK (+120V to +375V DC) │ │
 ─────────────────────────┬───────────────────┐ │ │
 │ │ │ │
 │ RCD SNUBBER │ TX1: PQ26/20 │ │ D_SEC: MBR10100G
 ┌─┴─┐ ┌─┴─┐ │ │ 100V, 10A Schottky
 │ │ R_snub (3x) │ │ Primary │ │ (Mounted on Heatsink)
 │ │ 22.6kΩ / 3W │ │ Np = 36T │ │
 └─┬─┘ │ │ Lp = 220µH │ │
 │ C_snub │ │ │ │ FLY_SEC_ANODE
 ├───[||]──────────┤ ● │ │ │ ┌─── Net: [5,6]
 │ 6.6nF / 1kV └─┬─┘ │ │ │ │
 ┌─┴─┐ │ │ │ │ ┌─┴─┐
 │ ▲ │ D_snub │ │ │ │ │ ▲ │
 │ ─ │ STTH110A ├── Net: FLY_DRAIN │ │ │ ─ │
 └─┬─┘ 1000V, 1A │ │ │ │ └─┬─┘
 │ ┌─┴─┐ │ │ │ │ Net: +24V_UNFILT
 └─────────────────┤ D │ Q1: CoolMOS │ │ │ ├───┬───────────────●═══[ 2.2µH ]═══╗
 │ │ IPB80R290P7 │ │ │ │ ┌─┴─┐ L_post ║
 Net: FLY_GATE ──────[ 10Ω Gate Res ]───┤G │ 800V, 17A │ │ │ │ │ + │ C_SEC ║
 │ S │ │ │ │ │ │ │ 2x 470µF ║
 └──┬┘ │ │ │ │ └───┘ Panasonic FC ║
 │ │ │ │ │ │ ║
 ├── Net: FLY_CS│ │ │ └───┼───────────────────────────────╢
 ┌─┴─┐ │ │ │ │ ║
 │ │ R_CS │ │ │ │ Net: PGND_SEC ║
 │ │ 0.25Ω / 2W │ │ │ │ ║
 └─┬─┘ │ │ │ │ ║
 │ │ │ │ │ ║
 Net: PGND_HOT ────────────────────────────┴──────────────┘ │ │ Secondary │ Winding ║
 │ └───● [7,8] ──┴───────────────────────────────╢
 │ Ns = 6T (Furukawa TEX-E TIW) ║
 │ ║
 Auxiliary Bias Winding (Naux = 4T) │ ║
 ─────────────────────────────────────────────────────────────┐ │ ║
 │ │ ║
 ┌───● [3] Naux = 4T │ │ ║
 │ │ │ │ ║
 ┌─┴─┐ └─── [4] ──────────── Net: PGND_HOT │ │ ║
 │ ▲ │ D_AUX: UF4004 │ │ ║
 │ ─ │ │ │ ║
 └─┬─┘ │ │ ║
 ├─── Net: FLY_VCC (+14.0V DC Bias) │ │ ║
 ┌─┴─┐ │ │ ║
 │ + │ C_AUX: 47µF / 35V │ │ ║
 └───┘ │ │ ║
 │ │ │ ║
 Net: PGND_HOT ────┴──────────────────────────────────────────┘ │ ║
 │ ║
 Galvanic Feedback Optocoupler Isolation Barrier │ Net: +24V_BUS (+24.0V DC Rail, 72W) ║
 ───────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────╝
 │ (To Stage 4 Buck-Boost & Aux Regulators)
 Net: FLY_COMP ────────────────────────────[4] Collector │
 (To U1 Pin 1) │ OPTO1: EL817 │
 ┌─┴─────────────┐ │
 │ 5000V RMS │ │
 │ [1] Anode │ │
 └───────┬───────┘ │
 │ │
 ├───[ 1.5kΩ Res ]───┴─── Net: +24V_BUS
 │
 Net: PGND_HOT ────────────────────────────[3] [2] Cathode
 │ │
 Emitter ├─── Cathode
 ┌─┴─┐
 │ │ U2: TL431ACDBZR
 │ │ Precision Shunt
 │ │ Ref: 2.495V
 └─┬─┘
 │ Anode
 │
 Net: PGND_SEC ─────────────────────────────────────┴─────────────────────── Net: PGND_SEC

=============================================================================================================================
```

## 3. Subsystem Netlist & Interconnect Table
| Net Name | Origin Pin | Destination Pins | Voltage / Current | Description |
| :--- | :--- | :--- | :---: | :--- |
| `+HV_BULK` | `C_BULK1` (+) | `TX1` Primary (Pin 1), `R_snub`, `C_snub` | +120 - +375 V_DC | High-voltage bulk input link. |
| `FLY_DRAIN` | `TX1` Primary (Pin 2) | CoolMOS `Q1` Drain, `D_snub` Anode | 0 - 599 V_peak | Primary high-voltage switching node (65 kHz). |
| `FLY_GATE` | Controller `U1` Pin 5 | `Q1` Gate via 10 Ω damping resistor | 0 - 12 V PWM | Primary MOSFET gate drive signal. |
| `FLY_SOURCE`| `Q1` Source | Current sense resistors `R_CS1`, `R_CS2` | 0 - 0.76 V | Primary peak current waveform tap. |
| `FLY_CS` | Node above `R_CS` | Controller `U1` Pin 3 via 1 kΩ filter | 0 - 0.76 V | Current sense input to internal PWM comparator. |
| `FLY_VCC` | `D_AUX` Cathode | Controller `U1` Pin 6, 47 µF cap | +14.0 V_DC | Controller auxiliary operating supply rail. |
| `FLY_COMP` | Controller `U1` Pin 1 | Optocoupler `OPTO1` Collector (Pin 4) | 0.8 - 4.5 V | Feedback loop compensation node. |
| `FLY_SEC_ANODE`| `TX1` Secondary (Pins 5,6)| Schottky `D_SEC` Anode | -63 V to +24 V | Secondary switching flyback pulse input. |
| `+24V_UNFILT` | `D_SEC` Cathode | `C_SEC1/2` (+), Choke `L_post` Pin 1 | +24.0 V_DC | Pre-filter intermediate DC rail. |
| `+24V_BUS` | `L_post` Pin 2 | `C_SEC_CER` (+), TL431 Divider, Stage 4 In | +24.0 V_DC ± 1% | Clean intermediate rail (72 W rated throughput). |
| `PGND_SEC` | `TX1` Secondary (Pins 7,8)| `C_SEC` (-), TL431 Anode, Stage 4 Return | 0.0 V (SELV) | Secondary touch-safe quiet ground plane. |

## 4. Theory of Operation & Magnetics Sizing Proof
1. **Energy Storage Cycle (t_on)**: When `Q1` turns ON, bulk voltage V_bulk is impressed across the primary winding (L_p = 220 µH). Current ramps linearly:
 I_pri(t) = (V_bulk / L_p) t -> I_pk = (120 V × (0.45 × 15.38 µs) / 220 µH) = mathbf{3.03 A_peak}
 Energy stored in the PQ26/20 core per cycle is:
 E_stored = (1 / 2) L_p I_pk^2 = (1 / 2) (220 × 10^-6) (3.03)^2 = 1.01 mJoules
2. **Energy Delivery Cycle (t_off)**: When `Q1` turns OFF, winding polarities invert. Secondary diode `D_SEC` becomes forward-biased, discharging stored magnetic energy into secondary capacitors `C_SEC` at +24.0 V. Total throughput power:
 P_throughput = E_stored × f_sw = (1.01 × 10^-3 J) × 65000 Hz = 65.65 W dots 72.0 W continuous (101.9W max capacity)
3. **Closed-Loop Regulation**: If +24.0 V rises, the voltage at `TL431_REF` exceeds 2.495 V, causing the TL431 to sink current through the optocoupler LED. This turns on the phototransistor, pulling down `FLY_COMP` and truncating PWM on-time to restore exact regulation.

## 5. Laboratory Bring-Up & Test Points
* **`TP_DRAIN` (Flyback Drain Waveform)**: Probe with a 100:1 high-voltage probe. Verify clean 65 kHz square wave with peak voltage clamped below 600 V by the snubber network.
* **`TP_24V` (Intermediate Rail)**: Verify stable +24.0 V_DC ± 0.8% regulation with peak-to-peak ripple < 35 mV_pk-pk at 3.0 A full load.
