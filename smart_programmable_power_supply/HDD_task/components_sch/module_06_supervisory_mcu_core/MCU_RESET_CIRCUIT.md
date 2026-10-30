# Component Schematic Specification: MCU_RESET (STM32 NRST Supervisory Circuit)

## 1. Component Metadata
* **Subsystem**: Stage 6 (System Hardware Reset & Brown-Out Reset Protection)
* **Active Components**: Passive RC timing network with optional manual tactile push-button `SW_RST`.
* **Values**:
  * Pull-Up Resistor: $R_{\text{PU_NRST}} = 10.0\,\text{k}\Omega \pm 1\%$ (0603 SMD, Vishay `CRCW060310K0FKEA`)
  * Filter Capacitor: $C_{\text{NRST}} = 100.0\,\text{nF} \pm 10\%$ 50V X7R (0603 SMD, Murata `GRM188R71H104KA93D`)
  * Manual Reset Switch: Tactile SPST normally open SMD switch (C&K `PTS645SL43-2 LFS`)

## 2. Electrical Operation & Timing
* **Reset Threshold ($V_{\text{IL,max}}$)**: $< 0.3 \times V_{\text{DD}} = 0.99\,\text{V}$
* **Reset Release Threshold ($V_{\text{IH,min}}$)**: $> 0.7 \times V_{\text{DD}} = 2.31\,\text{V}$
* **Power-On Reset Time Constant ($\tau$)**:
  $$\tau = R_{\text{PU_NRST}} \times C_{\text{NRST}} = (10.0\,\text{k}\Omega) \times (100.0\,\text{nF}) = \mathbf{1.0\,\text{ms}}$$
  * Guarantees that the reset line remains held LOW during supply voltage ramp-up until $V_{\text{DD}}$ stabilizes well above the internal brown-out reset threshold ($V_{\text{BOR0}} = 1.71\,\text{V}$).
* **Manual Reset**: Pressing `SW_RST` grounds Pin 7 (`NRST`), discharging $C_{\text{NRST}}$ through an internal $40\,\Omega$ ESD clamp and triggering instantaneous CPU re-initialization.

## 3. Schematic Symbol Representation
```
                      [ STM32 NRST SUPERVISORY RESET CIRCUIT ]
                                  Net: +3V3_SEC
                                        │
                                      ┌─┴─┐
                                      │   │ R_PU_NRST (10.0 kΩ ±1%)
                                      └─┬─┘
                                        │
    MCU Pin 7 (NRST) ───────────────────┼────────── Net: MCU_NRST
                                        │
                                 ┌──────┴──────┐
                                 │             │
                              ┌──┴──┐       ┌──o  o──┐
                              │     │       │  SW_RST│ (Tactile Pushbutton)
                              └──┬──┘       └──o──o──┘
                                 │             │
    Net: GND_SELV    ────────────┴─────────────┴──────────────
                              C_NRST (100 nF)
```
