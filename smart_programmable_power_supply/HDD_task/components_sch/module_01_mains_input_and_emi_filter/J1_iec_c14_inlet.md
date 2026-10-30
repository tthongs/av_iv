# Component Schematic Specification: J1 (AC Mains Inlet Socket)

## 1. Component Metadata
* **Reference Designator**: `J1`
* **Component Type**: AC Chassis Appliance Inlet
* **Manufacturer**: Schurter Inc.
* **Primary MPN**: `6100.3300`
* **Alternate Manufacturer**: TE Connectivity / Corcom
* **Alternate MPN**: `1-6609987-1`
* **Package / Footprint**: IEC 60320-1 C14 Panel Mount with Solder / Faston Terminals
* **Subsystem**: Stage 1 (Mains AC Input & Protection)

## 2. Electrical Ratings & Constraints
* **Rated Voltage**: $250\,	ext{V}_{	ext{AC RMS}}$ (Operating span: $85\,	ext{V} - 265\,	ext{V}_{	ext{AC}}$)
* **Rated Current**: $10.0\,	ext{A}_{	ext{RMS}}$ (Max system operating current: $1.604\,	ext{A}_{	ext{RMS}}$ at $85\,	ext{V}_{	ext{AC}}$)
* **Dielectric Withstand**: $> 2000\,	ext{V}_{	ext{AC}}$ Line-to-Earth (1 min)
* **Insulation Resistance**: $> 100\,	ext{M}\Omega$ @ $500\,	ext{V}_{	ext{DC}}$
* **Flammability Rating**: UL 94V-0 thermoplastic housing

## 3. Schematic Pin Connections & Net Mapping
| Pin / Terminal # | Terminal Name | Schematic Net Name | Connected To | Wire / Trace Requirement |
| :---: | :--- | :--- | :--- | :--- |
| **L** | **Live** | `AC_LINE_IN` | Fuse `F1` (Input terminal of fuse clip `FC1`) | Direct heavy-gauge chassis wire ($18\,	ext{AWG}$) or $\ge 2.5\,	ext{mm}$ PCB trace (2oz Cu). |
| **N** | **Neutral** | `AC_NEUTRAL_IN` | Inrush Thermistor `NTC1` (Input terminal) | Direct heavy-gauge chassis wire ($18\,	ext{AWG}$) or $\ge 2.5\,	ext{mm}$ PCB trace (2oz Cu). |
| **E** | **Earth** | `EARTH_GND` | Chassis metal enclosure stud and Class Y1 ground return (`C_Y1`, `C_Y2`) | Direct chassis mechanical screw bond with star lock washer. Safety earth track. |

## 4. Schematic Symbol Representation
```
       [ J1: IEC 320-C14 INLET ]
             ┌─────────┐
    Line  [L]│─────────│─── Net: AC_LINE_IN ──────> To Fuse F1
             │         │
 Neutral  [N]│─────────│─── Net: AC_NEUTRAL_IN ───> To NTC1
             │         │
   Earth  [E]│─────────│─── Net: EARTH_GND ───────> Chassis Earth & Y-Caps
             └─────────┘
```

## 5. Schematic & PCB Layout Guidelines
1. **Creepage & Clearance**: Maintain $\ge 3.0\,	ext{mm}$ clearance between Live and Neutral terminals, and $\ge 4.0\,	ext{mm}$ between Live/Neutral and Earth chassis ground.
2. **Safety Marking**: Clearly silkscreen High-Voltage warning symbols `[!] CAUTION: HIGH VOLTAGE 85-265V AC` directly adjacent to `J1`.
3. **Chassis Earth Bonding**: Earth terminal must be mechanically bonded to the metal chassis using an M4 screw with a star washer to guarantee $< 0.1\,\Omega$ ground bond resistance.
