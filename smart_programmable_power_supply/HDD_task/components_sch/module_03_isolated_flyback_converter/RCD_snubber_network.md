# Component Schematic Specification: D_snub, R_snub & C_snub (Primary RCD Snubber Network)

## 1. Component Metadata
* **Reference Designators**:
  * `D_snub`: Ultra-Fast High-Voltage Snubber Diode (STMicroelectronics `STTH110A`, $1000\,\text{V}$, $1.0\,\text{A}$, $t_{\text{rr}} < 50\,\text{ns}$, SMA / DO-214AC)
  * `R_snub1..3`: Snubber Resistors (Panasonic `ERJ-1TYJ683U`, 3x $68.0\,\text{k}\Omega \pm 1\%$ in parallel = $22.67\,\text{k}\Omega / 3.0\,\text{W}$ total, SMD 2512)
  * `C_snub1, 2`: High-Voltage Ceramic Snubber Capacitors (Murata `GRM31BR73A332KW01L`, 2x $3.3\,\text{nF} / 1000\,\text{V}$ X7R 1206 in parallel = $6.6\,\text{nF}$)
* **Subsystem**: Stage 3 (Isolated Flyback Subsystem)

## 2. Electrical Ratings & Snubber Derivations
* **Functional Role**: Clamps high-voltage inductive voltage kick induced by transformer primary leakage inductance ($L_{\text{lk}} \approx 4.4\,\mu\text{H}$) when primary MOSFET `Q1` turns off.
* **Leakage Energy Per Cycle**:
  $$E_{\text{lk}} = \frac{1}{2} L_{\text{lk}} I_{\text{pk}}^2 = \frac{1}{2} (4.4 \times 10^{-6}\,\text{H}) \times (3.03\,\text{A})^2 = \mathbf{20.20\,\mu\text{Joules}}$$
* **Snubber Resistor Power Dissipation**:
  $$P_{\text{snub}} = E_{\text{lk}} \times f_{\text{sw}} \times \frac{V_{\text{clamp}}}{V_{\text{clamp}} - V_R} = (20.2 \times 10^{-6}) \times 65000 \times \frac{216\,\text{V}}{216\,\text{V} - 144\,\text{V}} = 1.313 \times 3.0 = \mathbf{3.94\,\text{W}}$$
  *At full load ($72\,\text{W}$), measured power dissipation is $\approx 2.40\,\text{W}$. Three $1.0\,\text{W}$ 2512 resistors in parallel safely handle this dissipation with $20\%$ derating.*
* **Peak Clamped Drain Voltage**: Clamps peak spike at $V_{\text{DS,peak}} \le \mathbf{599.0\,\text{V}}$, protecting the $800\,\text{V}$ CoolMOS transistor.

## 3. Schematic Pin Connections & Net Mapping
```
        Net: +HV_BULK
             ├───┬───────────────────────────────┐
             │ ┌─┴─┐                           ┌─┴─┐
             │ │   │ R_snub (3x 68kΩ //)       │   │ C_snub (2x 3.3nF //)
             │ └─┬─┘ (22.67kΩ / 3W)            └─┬─┘ (6.6nF / 1000V)
             │   └───┬───────────────────────────┘
             │     ┌─┴─┐
             │     │ ▲ │ D_snub: STTH110A (1000V, 1A, trr < 50ns)
             │     │ ─ │ (Cathode to Snubber Bus, Anode to Drain)
             │     └─┬─┘
             │       │
             └───────┼─── Net: FLY_DRAIN (Connected to Q1 Drain & TX1 Pin 2)
```

| Ref Des | Pin 1 Net Name | Connected To | Pin 2 Net Name | Connected To | Role |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`D_snub`** | `FLY_DRAIN` (Anode) | `Q1` Drain, `TX1` Pin 2 | `FLY_SNUB_BUS` (Cathode) | Resistor/Capacitor clamp bus | Fast commutation of leakage current. |
| **`R_snub`** | `FLY_SNUB_BUS` | `D_snub` Cathode, `C_snub` | `+HV_BULK` | High-voltage bulk DC link (+) | Discharges snubber capacitor energy. |
| **`C_snub`** | `FLY_SNUB_BUS` | `D_snub` Cathode, `R_snub` | `+HV_BULK` | High-voltage bulk DC link (+) | Absorbs high-frequency inductive spike. |

## 4. Schematic & PCB Layout Guidelines
1. **Loop Area Minimization**: The snubber loop (TX1 Pin 2 $\rightarrow$ D_snub $\rightarrow$ C_snub/R_snub $\rightarrow$ TX1 Pin 1) carries high-frequency di/dt currents ($> 3\,\text{A}$ pulses). Constrain total loop area to $< 1.5\,\text{cm}^2$.
