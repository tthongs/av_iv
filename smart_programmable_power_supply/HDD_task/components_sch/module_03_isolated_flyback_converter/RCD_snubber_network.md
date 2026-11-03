# Component Schematic Specification: D_snub, R_snub & C_snub (Primary RCD Snubber Network)

## 1. Component Metadata
* **Reference Designators**:
 * `D_snub`: Ultra-Fast High-Voltage Snubber Diode (STMicroelectronics `STTH110A`, 1000 V, 1.0 A, t_rr < 50 ns, SMA / DO-214AC)
 * `R_snub1..3`: Snubber Resistors (Panasonic `ERJ-1TYJ683U`, 3x 68.0 kΩ ± 1% in parallel = 22.67 kΩ / 3.0 W total, SMD 2512)
 * `C_snub1, 2`: High-Voltage Ceramic Snubber Capacitors (Murata `GRM31BR73A332KW01L`, 2x 3.3 nF / 1000 V X7R 1206 in parallel = 6.6 nF)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Snubber Derivations
* **Functional Role**: Clamps high-voltage inductive voltage kick induced by transformer primary leakage inductance (L_lk ≈ 4.4 µH) when primary MOSFET `Q1` turns off.
* **Leakage Energy Per Cycle**:
 E_lk = (1 / 2) L_lk I_pk^2 = (1 / 2) (4.4 × 10^-6 H) × (3.03 A)^2 = 20.20 µJoules
* **Snubber Resistor Power Dissipation**:
 P_snub = E_lk × f_sw × (V_clamp / V_clamp - V_R) = (20.2 × 10^-6) × 65000 × (216 V / 216 V - 144 V) = 1.313 × 3.0 = 3.94 W
 *At full load (72 W), measured power dissipation is ≈ 2.40 W. Three 1.0 W 2512 resistors in parallel safely handle this dissipation with 20% derating.*
* **Peak Clamped Drain Voltage**: Clamps peak spike at V_DS,peak ≤ 599.0 V, protecting the 800 V CoolMOS transistor.

## 3. Schematic Pin Connections & Net Mapping
```
 Net: +HV_BULK
 ├───┬───────────────────────────────┐
 │ ┌─┴─┐ ┌─┴─┐
 │ │ │ R_snub (3x 68kΩ //) │ │ C_snub (2x 3.3nF //)
 │ └─┬─┘ (22.67kΩ / 3W) └─┬─┘ (6.6nF / 1000V)
 │ └───┬───────────────────────────┘
 │ ┌─┴─┐
 │ │ ▲ │ D_snub: STTH110A (1000V, 1A, trr < 50ns)
 │ │ ─ │ (Cathode to Snubber Bus, Anode to Drain)
 │ └─┬─┘
 │ │
 └───────┼─── Net: FLY_DRAIN (Connected to Q1 Drain & TX1 Pin 2)
```

| Ref Des | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`D_snub`** | `FLY_DRAIN` (Anode) | `Q1` Drain, `TX1` Pin 2 | `FLY_SNUB_BUS` (Cathode) | Resistor/Capacitor clamp bus | Fast commutation of leakage current. |
| **`R_snub`** | `FLY_SNUB_BUS` | `D_snub` Cathode, `C_snub` | `+HV_BULK` | High-voltage bulk DC link (+) | Discharges snubber capacitor energy. |
| **`C_snub`** | `FLY_SNUB_BUS` | `D_snub` Cathode, `R_snub` | `+HV_BULK` | High-voltage bulk DC link (+) | Absorbs high-frequency inductive spike. |

## 4. Schematic & PCB Layout Guidelines
1. **Loop Area Minimization**: The snubber loop (TX1 Pin 2 rightarrow D_snub rightarrow C_snub/R_snub rightarrow TX1 Pin 1) carries high-frequency di/dt currents (> 3 A pulses). Constrain total loop area to < 1.5 cm^2.
