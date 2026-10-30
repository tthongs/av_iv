# Component Schematic Specification: MCU Decoupling & Analog Power Filters

## 1. Subsystem Metadata
* **Subsystem**: Stage 6 (STM32G474 Power Integrity & Noise Decoupling Subsystem)
* **Supply Rails Covered**:
  * Digital Supply Domain: `+3V3_SEC` ($+3.30\,\text{V}_{\text{DC}}$)
  * Analog Supply Domain: `+3V3A_ANALOG` ($+3.30\,\text{V}_{\text{DC}}$ filtered)
  * Reference Voltage Domain: `VREF+` (Tied to `+3V3A_ANALOG`)

## 2. Decoupling Component Sizing & Bill of Materials
| Ref Des | Component Description | Value / Rating | Footprint | Primary MPN | Placement Location |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **`C_VDD1`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 19 (`VDD1`) / Pin 18 (`VSS1`) |
| **`C_VDD2`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 32 (`VDD2`) / Pin 31 (`VSS2`) |
| **`C_VDD3`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 48 (`VDD3`) / Pin 47 (`VSS3`) |
| **`C_VDD4`** | High-Frequency Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 64 (`VDD4`) / Pin 63 (`VSS4`) |
| **`C_VBAT`** | Battery Domain Bypass MLCC | $100\,\text{nF}, 16\,\text{V}, \text{X7R}$ | 0402 SMD | Murata `GRM155R71C104KA88D` | Pin 1 (`VBAT`) |
| **`C_BULK_MCU`**| MCU Bulk Reservoir MLCC | $4.7\,\mu\text{F}, 10\,\text{V}, \text{X7R}$ | 0805 SMD | Murata `GRM21BR71A475KA73L` | Adjacent to Pin 64 |
| **`FB1`** | Analog Domain Ferrite Bead | $120\,\Omega \text{ at } 100\,\text{MHz}, 1.5\,\text{A}$ | 0603 SMD | Murata `BLM18PG121SN1D` | Between `+3V3_SEC` and `+3V3A_ANALOG` |
| **`C_VDDA1`**| Analog High-Frequency Bypass| $10\,\text{nF}, 25\,\text{V}, \text{C0G}$ | 0603 SMD | Murata `GRM1885C1E103JA01D` | Pin 13 (`VDDA`) / Pin 12 (`VSSA`) |
| **`C_VDDA2`**| Analog Medium-Freq Bypass | $1.0\,\mu\text{F}, 16\,\text{V}, \text{X7R}$ | 0603 SMD | Murata `GRM188R71C105KA12D` | Pin 13 (`VDDA`) / Pin 12 (`VSSA`) |

## 3. Schematic Symbol Representation
```
                    [ MCU POWER DECOUPLING & ANALOG PI-FILTER ]

    Net: +3V3_SEC ──┬──────────────┬──────────────┬──────────────┬──────┐
                    │              │              │              │      │
                 [100nF]        [100nF]        [100nF]        [100nF] [4.7µF]
                 (Pin 19)       (Pin 32)       (Pin 48)       (Pin 64)  │
                    │              │              │              │      │
    Net: GND_SELV ──┴──────────────┴──────────────┴──────────────┴──────┘

    Net: +3V3_SEC ──[ FB1: BLM18PG121 ]──┬── Net: +3V3A_ANALOG (Pin 13 VDDA)
                                         │
                                      [10nF C0G]   [1.0µF X7R]
                                         │              │
    Net: AGND_SEC ───────────────────────┴──────────────┴────── (Pin 12 VSSA)
```
